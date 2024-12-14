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
