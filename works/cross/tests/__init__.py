from .. import Works_cross


def test_works_cross_init():
    w = Works_cross()
    assert w.teams == []
