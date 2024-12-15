#include <pybind11/pybind11.h>

// fibonacci sequence
uint64_t fibonacci(uint64_t n) {
  if (n == 0) {
    return 0;
  } else if (n == 1) {
    return 1;
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
