from .config import config
try:
    from fibonacci._core import fibonacci as _fibonacci_rs
except ModuleNotFoundError:
    print("Rust backend not found")
    def _fibonacci_rs(n: int) -> int:
        raise NotImplementedError("Rust backend not found")
try:
    from fibonacci._cpp_core import fibonacci as _fibonacci_cpp
except ModuleNotFoundError:
    print("C++ backend not found")
    def _fibonacci_cpp(n: int) -> int:
        raise NotImplementedError("C++ backend not found")


def fibonacci(n: int) -> int:
    if config.backend == "py":
        return _fibonacci_py(n)
    elif config.backend == "rs":
        return _fibonacci_rs(n)
    elif config.backend == "cpp":
        return _fibonacci_cpp(n)
    else:
        raise NotImplementedError(f"Unknown backend: {config.backend}")


def _fibonacci_py(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return _fibonacci_py(n - 1) + _fibonacci_py(n - 2)
