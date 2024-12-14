from .config import config
from fibonacci._core import fibonacci as _fibonacci_rs


def fibonacci(n: int) -> int:
    if config.backend == "py":
        return _fibonacci_py(n)
    elif config.backend == "rs":
        return _fibonacci_rs(n)
    else:
        raise NotImplementedError(f"Unknown backend: {config.backend}")


def _fibonacci_py(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return _fibonacci_py(n - 1) + _fibonacci_py(n - 2)
