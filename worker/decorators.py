from functools import wraps
import traceback
import random
from typing import Callable, Any
import asyncio

import loguru


def exception_handler(func: Callable):
    """
    Decorator that handles exceptions and returns an empty string on failure.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in function {func.__name__} with {args} & {kwargs}: {e}")
            traceback.print_exc()
            return ""
    return wrapper


def get_unique_object(func: Callable):
    """
    This decorator maintains a list of used objects and ensures that the
    wrapped function. returns a unique object each time it is called until
    all objects have been used. Once all objects have been used,
    the list of used objects is cleared and the process starts again.

    Args:
        func (callable): A function that returns a list of objects.

    Returns:
        Callable: A wrapped function that returns a tuple containing a unique object from
                  the list and the list of used objects.
    """
    used_objects = []

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal used_objects
        objects = func(*args, **kwargs)

        if len(used_objects) != len(objects):
            random.shuffle(objects)
            result = next((
                obj for obj in objects if obj not in used_objects),
                None
            )
            used_objects.append(result)
            loguru.logger.info(
                f"Total Objects Left: {len(objects)-len(used_objects)}"
            )
            return result
        else:
            used_objects.clear()
            return wrapper(*args, **kwargs)

    return wrapper


def async_timeout(timeout: float):
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(
                    f"Function '{func.__name__}' exceeded {timeout} seconds timeout."
                )
        return wrapper
    return decorator
