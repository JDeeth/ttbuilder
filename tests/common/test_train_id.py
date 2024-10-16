import pytest

from ttbuilder.common.train_id import TrainId


def test_train_id_from_str():
    assert TrainId.from_str("1A01") == TrainId(id="1A01")
    assert TrainId.from_str("1A01/ABC234") == TrainId(id="1A01", uid="ABC234")


def test_train_id_to_str():
    assert str(TrainId(id="1A01")) == "1A01"
    assert str(TrainId(id="1A01", uid="ABC234")) == "1A01/ABC234"


@pytest.mark.parametrize(
    "train_id,expected_xml",
    [
        (TrainId(id="1A01"), "<AssociatedTrain>1A01</AssociatedTrain>"),
        (TrainId(id="2A04", uid="ZDC316"), "<AssociatedUID>ZDC316</AssociatedUID>"),
    ],
)
def test_train_id_to_activity_xml(xml_test_tools, train_id, expected_xml):
    xt = xml_test_tools
    expected = xt.fromstr(expected_xml)
    xt.assert_equivalent(expected, train_id.activity_xml())
