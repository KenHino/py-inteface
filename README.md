# py-interface
Tutorial for python interface with static language (Rust, C++) backend

## Procedures (Python, [uv](https://docs.astral.sh/uv/))

1. Install uv
    ```bash
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    ```bash
    $ uv --version
    uv 0.5.9
    ```

1. Start Python project
    ```bash
    $ uv init --lib --name fibonacci .
    ```
    ```bash
    $ cat pyproject.toml
    ```
    ```toml
    [project]
    name = "fibonacci"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    ```
    ```bash
    $ tree src
    src
    └── fibonacci
        ├── __init__.py
        └── py.typed

    2 directories, 2 files
    ```

1. Add developping requirements
    ```bash
    $ uv add pytest ruff mypy pre-commit --dev
    ```

    ```bash
    $ cat .pre-commit-config.yaml
    ```
    ```yaml
    repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
        - id: no-commit-to-branch
            args: [--branch, main]
        - id: check-added-large-files
            args: ['--maxkb=500']
        - id: check-docstring-first
        - id: check-yaml
        - id: check-toml
        - id: end-of-file-fixer
        - id: trailing-whitespace

    - repo: local
        hooks:
        - id: format
            name: format
            entry: uv run ruff format src/fibonacci
            language: system
            pass_filenames: false
            files: "^(srt/fibonacci/)"

        - id: fix-lint
            name: fix-lint
            entry: uv run ruff check --fix src/fibonacci
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/)"

        - id: typecheck
            name: mypy
            entry: uv run mypy src/fibonacci
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/)"

        - id: pytest
            name: pytest
            entry: uv run pytest
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/|tests/)"
    ```
    ```bash
    $ uv run pre-commit install
    ```

2. Add modules
    ```bash
    $ cat src/fibonacci/config.py
    ```
    ```python
    class Config:
        backend = "py"
    config = Config()
    ```

    ```bash
    $ cat src/fibonacci/fibonacci.py
    ```
    ```python
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
    ```

    ```bash
    $ cat src/fibonacci/__init__.py
    ```
    ```python
    from .fibonacci import fibonacci

    __all__ = ["fibonacci"]
    ```

3. Add tests
    ```bash
    $ mkdir tests
    ```
    ```bash
    $ cat tests/test_fibonacci.py
    ```
    ```python
    import pytest
    from fibonacci import fibonacci

    n_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    answer = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    @pytest.mark.parametrize("n, answer", zip(n_list, answer))
    def test_fibonacci(n, answer):
        assert fibonacci(n) == answer
    ```
    ```bash
    $ uv run pytest
    ==================================== test session starts =====================================
    platform linux -- Python 3.12.2, pytest-8.3.4, pluggy-1.5.0
    rootdir: /mnt/c/Users/hinom/GitHub/py-interface
    configfile: pyproject.toml
    collected 11 items

    tests/test_fibonacci.py ...........                                                    [100%]

    ===================================== 11 passed in 0.11s =====================================
    ```

## Procedures (Rust, [PyO3](https://github.com/PyO3/pyo3), [maturin](https://github.com/PyO3/maturin))

0. Clean up the `src`, `uv.lock` and `pyproject.toml`.
    ```bash
    $ rm -rf uv.lock pyproject.toml
    $ cp -r src src.bak # backup
    ```

1. Start Rust project
    ```bash
    $ uv init --lib . --name fibonacci --build-backend maturin
    $ uv add ipython mypy pre-commit pytest ruff --dev
    ```
    ```bash
    $ cat pyproject.toml
    ```
    ```toml
    [project]
    name = "fibonacci"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [tool.maturin]
    module-name = "fibonacci._core"
    python-packages = ["fibonacci"]
    python-source = "src"

    [build-system]
    requires = ["maturin>=1.0,<2.0"]
    build-backend = "maturin"

    [dependency-groups]
    dev = [
        "ipython>=8.30.0",
        "mypy>=1.13.0",
        "pre-commit>=4.0.1",
        "pytest>=8.3.4",
        "ruff>=0.8.3",
    ]
    ```
    ```bash
    $ tree src
    src
    ├── fibonacci
    │   ├── __init__.py
    │   ├── _core.pyi
    │   └── py.typed
    └── lib.rs
    ```
    ```bash
    $ uv run maturin develop --uv
    ```
    ```bash
    $ cat .pre-commit-config.yaml
    ```
    ```yaml
    repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.5.0
        hooks:
        - id: no-commit-to-branch
            args: [--branch, main]
        - id: check-added-large-files
            args: ['--maxkb=500']
        - id: check-docstring-first
        - id: check-yaml
        - id: check-toml
        - id: end-of-file-fixer
        - id: trailing-whitespace

    - repo: local
        hooks:
        - id: format
            name: format
            entry: uv run ruff format src/fibonacci
            language: system
            pass_filenames: false
            files: "^(srt/fibonacci/)"

        - id: fix-lint
            name: fix-lint
            entry: uv run ruff check --fix src/fibonacci
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/)"

        - id: typecheck
            name: mypy
            entry: uv run mypy src/fibonacci
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/)"

        - id: pytest
            name: pytest
            entry: uv run pytest
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/|tests/)"

        - id: rustfmt
            name: rustfmt
            description: Check if all files follow the rustfmt style
            entry: cargo fmt --all -- --color always
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/|tests/)"

        - id: clippy
            name: clippy
            description: Check if all files pass clippy
            entry: cargo clippy --all-targets --all-features -- -D warnings
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/|tests/)"

        - id: rusttest
            name: rusttest
            description: Run all tests
            entry: cargo test --all-targets --all-features
            language: system
            pass_filenames: false
            files: "^(src/fibonacci/|tests/)"
    ```

2. Add modules
    ```bash
    $ cat src/fibonacci/__init__.py
    ```
    ```python
    from .fibonacci import fibonacci
    from .config import config

    __all__ = ['fibonacci', 'config']
    ```
    ```bash
    $ cat src/fibonacci/_core.pyi
    ```
    ```python
    from __future__ import annotations

    def fibonacci(n: int) -> int: ...
    ```
    ```bash
    $ cat src/fibonacci/fibonacci.py
    ```
    ```python
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
    ```
    ```bash
    $ cat src/fibonacci/config.py
    ```
    ```python
    class Config:
        backend = "py"


    config = Config()
    ```
    ```bash
    $ cat src/lib.rs
    ```
    ```rust
    use pyo3::prelude::*;


    #[pyfunction]
    fn fibonacci(n: u64) -> u64 {
        if n == 0 {
            return 0;
        } else if n == 1 {
            return 1;
        }

        return fibonacci(n - 1) + fibonacci(n - 2);
    }

    /// A Python module implemented in Rust. The name of this function must match
    /// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
    /// import the module.
    #[pymodule]
    fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
        Ok(())
    }
    ```
    ```bash
    $ uv run maturin develop --uv
    ```
    ```bash
    $ tree src
    src
    ├── fibonacci
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-312.pyc
    │   │   ├── config.cpython-312.pyc
    │   │   └── fibonacci.cpython-312.pyc
    │   ├── _core.abi3.so
    │   ├── _core.pyi
    │   ├── config.py
    │   ├── fibonacci.py
    │   └── py.typed
    └── lib.rs

    3 directories, 10 files
    ```

3. Testing
    ```bash
    $ cat tests/test_fibonacci.py
    ```
    ```python
    import pytest
    from fibonacci import fibonacci, config

    n_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    answer = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    @pytest.mark.parametrize("n, answer", zip(n_list, answer))
    def test_fibonacci(n, answer):
        config.backend = 'py'
        assert fibonacci(n) == answer
        config.backend = 'rs'
        assert fibonacci(n) == answer
    ```
    ```bash
    $ uv run pytest
    ```
    ```bash
    $ uv run ipython
    ```
    ```ipython
    Python 3.12.2 (main, Feb 25 2024, 04:38:01) [Clang 17.0.6 ]
    Type 'copyright', 'credits' or 'license' for more information
    IPython 8.30.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from fibonacci import config, fibonacci

    In [2]: config.backend = 'py'

    In [3]: %timeit fibonacci(30)
    74.2 ms ± 547 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)

    In [4]: config.backend = 'rs'

    In [5]: %timeit fibonacci(30)
    5.62 ms ± 36.2 μs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    ```


## Procedures (C++, [pybind11](https://github.com/pybind/pybind11), [scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/getting_started.html))

The easiest way is obeying
```bash
$ uv init . --lib --build-backend scikit
```

1. Install dependencies
    ```bash
    $ sudo apt install build-essential clang
    ```
    `clang` may be required for `scikit-build-core` in default settings.

1. Start C++ project
    ```bash
    $ cat pyproject.toml
    ```
    ```toml
    [project]
    name = "fibonacci"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [tool.scikit-build]
    minimum-version = "build-system.requires"
    build-dir = "build/{wheel_tag}"

    [build-system]
    requires = ["scikit-build-core>=0.10", "pybind11"]
    build-backend = "scikit_build_core.build"  # C++ only (using CMakeLists.txt)
    ```

    ```bash
    $ cat CMakeLists.txt
    ```
    ```cmake
    # CMakeLists.txt for scikit-build example project not work with setuptools

    cmake_minimum_required(VERSION 3.15)
    project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

    set(PYBIND11_FINDPYTHON ON)
    find_package(pybind11 CONFIG REQUIRED)

    pybind11_add_module(_cpp_core MODULE src/lib.cpp)
    install(TARGETS _cpp_core DESTINATION ${SKBUILD_PROJECT_NAME})
    ```

1. Implementing something...
    ```bash
    $ cat src/lib.cpp
    ```
    ```cpp
    #include <pybind11/pybind11.h>

    // fibonacci sequence
    uint64_t fibonacci(uint64_t n) {
    if (n == 1) {
        return 1;
    }
    else if (n == 0) {
        return 0;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
    }

    namespace py = pybind11;

    PYBIND11_MODULE(_cpp_core, m) {
    m.doc() = "pybind11 hello module";

    m.def("fibonacci", &fibonacci, R"pbdoc(
        A function that returns the n-th number in the fibonacci sequence.
    )pbdoc");
    }
    ```

    ```bash
    $ cat src/fibonacci/fibonacci.py
    ```
    ```python
    from .config import config
    try:
        from fibonacci._core import fibonacci as _fibonacci_rs
    except ModuleNotFoundError:
        print("Rust backend not found")
    try:
        from fibonacci._cpp_core import fibonacci as _fibonacci_cpp
    except ModuleNotFoundError:
        print("C++ backend not found")


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
    ```



## Procedures (C++ + Rust, setuptools)

1. Setup project
    ```bash
    $ cat pyproject.toml
    ```
    ```toml
    [project]
    name = "fibonacci"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [build-system]
    requires = ["pybind11", "setuptools>=75.0.0", "setuptools-rust", "wheel", "ninja"]
    build-backend = "setuptools.build_meta"  # Both (using setup.py + setuptools-rust, MANIFEST.in)

    [tool.setuptools.packages]
    # Pure Python packages/modules
    find = { where = ["src"] }

    [[tool.setuptools-rust.ext-modules]]
    # Private Rust extension module to be nested into the Python package
    target = "fibonacci._core"  # The last part of the name (e.g. "_lib") has to match lib.name in Cargo.toml,
                                # but you can add a prefix to nest it inside of a Python package.
    path = "Cargo.toml"      # Default value, can be omitted
    binding = "PyO3"         # Default value, can be omitted
    ```

    ```bash
    $ cat setup.py
    ```
    ```python
    # Available at setup time due to pyproject.toml
    from pybind11.setup_helpers import Pybind11Extension, build_ext
    from setuptools import setup


    # The main interface is through Pybind11Extension.
    # * You can add cxx_std=11/14/17, and then build_ext can be removed.
    # * You can set include_pybind11=false to add the include directory yourself,
    #   say from a submodule.
    #
    # Note:
    #   Sort input source files if you glob sources to ensure bit-for-bit
    #   reproducible builds (https://github.com/pybind/python_example/pull/53)

    ext_modules = [
        Pybind11Extension(
            "fibonacci._cpp_core",
            ["src/lib.cpp"],
            # Example: passing in the version to the compiled code
        ),
    ]

    setup(
        name="fibonacci",
        ext_modules=ext_modules,
        # Currently, build_ext only provides an optional "highest supported C++
        # level" feature, but in the future it may provide more features.
        cmdclass={"build_ext": build_ext},
        zip_safe=False,
    )
    ```

    ```bash
    $ cat MANIFEST.in
    ```
    ```plaintext
    include Cargo.toml
    recursive-include src *.rs
    ```


```bash
$ uv run ipython
```
```ipython
Python 3.12.2 (main, Feb 25 2024, 04:38:01) [Clang 17.0.6 ]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.30.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from fibonacci import config, fibonacci

In [2]: config.backend = 'py'

In [3]: %timeit fibonacci(30)
77 ms ± 761 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)

In [4]: config.backend = 'rs'

In [5]: %timeit fibonacci(30)
5.86 ms ± 36.4 μs per loop (mean ± std. dev. of 7 runs, 100 loops each)

In [6]: config.backend = 'cpp'

In [7]: %timeit fibonacci(30)
1.64 ms ± 19.9 μs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```

Why C++ is much faster than Rust?



## References
- [setuptools-rust](https://github.com/PyO3/setuptools-rust)
