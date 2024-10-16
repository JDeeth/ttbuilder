import pytest

from ttbuilder.train.weight import Weight


@pytest.mark.parametrize(
    "weight,expected",
    [
        (Weight.LIGHT, 1),
        (Weight.NORMAL, 0),
        (Weight.HEAVY, 2),
    ],
)
def test_train_weight_xml_values_are_correct(weight, expected):
    assert weight.xml_value == expected
