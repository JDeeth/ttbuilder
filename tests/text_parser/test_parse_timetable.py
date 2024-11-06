from ttbuilder.common.ttime import TTime
from ttbuilder.simsig.local_timetable import LocalTimetable

TEST_1M45 = """\
1M45
22:30 Peterborough-Carlisle (Parcels)
DRBY.4  00:40
STSNJN  00/47h [1H]
NSJDRBY 00/48½
BURTNOT 00/53
"""


def test_timetable_from_str(ttparser):
    tt: LocalTimetable = ttparser.parse_timetable(TEST_1M45)
    assert tt.train_id.id == "1M45"
    assert tt.origin == "Peterborough"
    assert tt.destination == "Carlisle"
    assert tt.origin_dep == TTime.stopping(22, 30)
    assert tt.train_type == "Parcels"
    # this will need to be converted to a defined train type

    assert len(tt.timing_points) == 4
    drby = tt.timing_points[0]
    assert drby.location.tiploc == "DRBY"
    assert drby.location.platform == "4"
    assert drby.depart == TTime.stopping(0, 40)
