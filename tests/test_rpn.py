import pytest

from rpn import Engine


TABLE = [
    ('-3 9 6 2 2 -8 2 -10 + -7 4 / 9 * cos sign', -1),
    ('-10 -1 5 1 -1 3 -7 8 9 -2 -8 * fact', 20922789888000),
    ('2 -3 -2 5 / -7 * 6 -3 -5 5 -2 <= 6 0 -4 swap', 0),
    ('10 2 * -4 0 9 -6 2 9 -4 3 -4 -9 4 repeat +', -5),
    ('8 10 x= x x * log', 2.0),
]


@pytest.mark.parametrize('expr,result', TABLE)
def test_rpn(expr, result):
    engine = Engine()
    engine.evaluate(expr)
    assert engine.result() == result
