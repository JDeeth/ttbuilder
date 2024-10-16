import pytest

from ttbuilder.train.speed_class import SpeedClass


@pytest.mark.parametrize(
    "sc,expected",
    [
        (SpeedClass.EPS_E, 1),
        (SpeedClass.EPS_D, 2),
        (SpeedClass.HST, 4),
        (SpeedClass.EMU, 8),
        (SpeedClass.DMU, 16),
        (SpeedClass.SPRINTER, 32),
        (SpeedClass.CS_67, 64),
        (SpeedClass.MGR, 128),
        (SpeedClass.TGV_373, 256),
        (SpeedClass.LOCO_H, 512),
        (SpeedClass.METRO, 1024),
        (SpeedClass.WES_442, 2048),
        (SpeedClass.TRIPCOCK, 4096),
        (SpeedClass.STEAM, 8192),
        (SpeedClass.SIM_1, 16777216),
        (SpeedClass.SIM_2, 33554432),
        (SpeedClass.SIM_3, 67108864),
        (SpeedClass.SIM_4, 134217728),
        (SpeedClass.TGV_373 | SpeedClass.EMU | SpeedClass.HST, 4 + 8 + 256),
    ],
)
def test_speedclass_xml_values_are_correct(sc, expected):
    assert sc.xml_value == expected
