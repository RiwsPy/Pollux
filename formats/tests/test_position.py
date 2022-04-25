from ..position import Position, Relation


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


def test_round():
    a = Position([1.23456, 9.8765])
    expected_value = [1.23, 9.88]
    assert a.round(2) == expected_value

    b = Position([1, 2])
    expected_value = [1, 2]
    assert b.round(2) == expected_value


def test_to_position():
    a = Relation([[0, 0], [1, 2]])
    expected_value = [0.5, 1]
    assert a.to_position() == expected_value

    b = Relation([[[0, 0], [1, 2]]])
    expected_value = [0.5, 1]
    assert b.to_position() == expected_value
