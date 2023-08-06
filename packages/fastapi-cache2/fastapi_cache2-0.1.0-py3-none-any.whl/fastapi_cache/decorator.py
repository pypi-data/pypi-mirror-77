from functools import wraps
from typing import Callable, Optional, Type

from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import Coder, FastAPICache, JsonCoder


def default_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key


def cache(
    expire: int = None,
    coder: Type[Coder] = JsonCoder,
    key_builder: Callable = default_key_builder,
    namespace: Optional[str] = "",
):
    """
    cache all function
    :param namespace:
    :param expire:
    :param coder:
    :param key_builder:
    :return:
    """

    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            backend = FastAPICache.get_backend()
            cache_key = key_builder(func, namespace, *args, **kwargs)
            ret = await backend.get(cache_key)
            if ret is not None:
                return coder.decode(ret)

            ret = await func(*args, **kwargs)
            await backend.set(cache_key, coder.encode(ret), expire)
            return ret

        return inner

    return wrapper


def cache_response(
    expire: int = None,
    coder: Type[Coder] = JsonCoder,
    key_builder: Callable = default_key_builder,
    namespace: Optional[str] = "",
):
    """
    cache fastapi response
    :param namespace:
    :param expire:
    :param coder:
    :param key_builder:
    :return:
    """

    def wrapper(func):
        @wraps(func)
        async def inner(request: Request, *args, **kwargs):
            if request.method != "GET":
                return await func(request, *args, **kwargs)

            backend = FastAPICache.get_backend()
            cache_key = key_builder(func, namespace, request, *args, **kwargs)
            ttl, ret = await backend.get_with_ttl(cache_key)
            if_none_match = request.headers.get("if-none-match")
            if ret is not None:
                response = kwargs.get("response")
                if response:
                    response.headers["Cache-Control"] = f"max-age={ttl}"
                    etag = f"W/{hash(ret)}"
                    if if_none_match == etag:
                        response.status_code = 304
                        return response
                    response.headers["ETag"] = etag
                return coder.decode(ret)

            ret = await func(request, *args, **kwargs)
            await backend.set(cache_key, coder.encode(ret), expire)
            return ret

        return inner

    return wrapper
