from ..position import Position


def test_create():
    assert Position([0.0, 0.0]) == [0.0, 0.0]


def test_add():
    a = Position([1.0, 0.0])
    b = Position([0.0, 2.3])
    assert a + b == [1.0, 2.3]


def test_truediv():
    a = Position([1.0, 2.0])
    assert a / 2 == [0.5, 1.0]


def test_distance():
    a = Position([0.0, 0.0])
    b = Position([1.0, 1.0])
    assert a.distance(b) == 157249.38127194397
