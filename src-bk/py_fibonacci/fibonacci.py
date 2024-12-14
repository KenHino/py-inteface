from .config import config


def fibonacci(n: int) -> int:
    if config.backend == "py":
        return _fibonacci_py(n)
    else:
        raise NotImplementedError


def _fibonacci_py(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return _fibonacci_py(n - 1) + _fibonacci_py(n - 2)
