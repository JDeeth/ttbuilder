from ttbuilder.train.power_type import PowerType
from ttbuilder.train.train_category import TrainCategory

PARCELS = """\
Parcels
220m, 90mph, Diesel, DC_Overhead"""


def test_train_type_from_str(ttparser):
    tc: TrainCategory = ttparser.parse_train_category(PARCELS)
    assert tc.description == "Parcels"
    assert tc.length_m == 220
    assert tc.max_speed_mph == 90
    assert tc.power_type == PowerType.DIESEL | PowerType.DC_OVERHEAD
    # missing: accel, weight, speed class, freight linespeeds, dwell times
