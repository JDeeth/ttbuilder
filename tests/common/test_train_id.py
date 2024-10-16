import pytest

from common import TrainId


@pytest.mark.parametrize(
    "params,expected_xml",
    [
        ({"id": "1A01"}, "<AssociatedTrain>1A01</AssociatedTrain>"),
        ({"id": "2A04", "uid": "ZDC316"}, "<AssociatedUID>ZDC316</AssociatedUID>"),
    ],
)
def test_train_id(xml_test_tools, params, expected_xml):
    xt = xml_test_tools
    expected = xt.fromstr(expected_xml)

    train = TrainId(**params)

    xt.assert_equivalent(expected, train.xml())
