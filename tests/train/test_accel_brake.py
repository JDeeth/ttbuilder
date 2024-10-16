import pytest

from train.accel_brake import AccelBrake


@pytest.mark.parametrize(
    "ab,value",
    [
        (AccelBrake.VERY_LOW, 0),
        (AccelBrake.LOW, 1),
        (AccelBrake.MEDIUM, 2),
        (AccelBrake.HIGH, 3),
        (AccelBrake.VERY_HIGH, 4),
    ],
)
def test_accel_brake(ab, value):
    assert ab.value == value
