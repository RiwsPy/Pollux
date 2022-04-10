from .. import Works_cross
from ...crossings import Crossings
from ...highways import Highways


def test_works_cross_init():
    w = Works_cross()
    assert w.teams == []
    assert w.copyrights == set()
    assert w.db_name == ''
    assert w.COPYRIGHT == ''
    assert w.features == []


def test_works_add():
    w = Works_cross([Crossings], [Highways])
    assert w.db_name == Crossings.filename + '|' + Highways.filename
