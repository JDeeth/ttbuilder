import pytest

from ttbuilder.train.power_type import PowerType


@pytest.mark.parametrize(
    "pt,expected",
    [
        (PowerType.NONE, ""),
        (PowerType.AC_OVERHEAD, "O"),
        (PowerType.DC_3RAIL, "3"),
        (PowerType.DC_4RAIL, "4"),
        (PowerType.DIESEL, "D"),
        (PowerType.DC_OVERHEAD, "V"),
        (PowerType.TRAMWAY, "T"),
        (PowerType.SIM_1, "X1"),
        (PowerType.SIM_2, "X2"),
        (PowerType.SIM_3, "X3"),
        (PowerType.SIM_4, "X4"),
        (PowerType.DC_3RAIL | PowerType.AC_OVERHEAD | PowerType.DC_OVERHEAD, "O3V"),
        (PowerType.DC_3RAIL | PowerType.AC_OVERHEAD | PowerType.DC_3RAIL, "O3"),
    ],
)
def test_power_type_xml_values_are_correct(pt, expected):
    assert pt.xml_value == expected


def test_power_type_bitwise_and():
    acdc = PowerType.AC_OVERHEAD | PowerType.DC_3RAIL
    assert PowerType.AC_OVERHEAD & acdc
    assert not PowerType.DIESEL & acdc
