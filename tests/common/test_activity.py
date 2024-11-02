import pytest

from ttbuilder.common import activity
from ttbuilder.common.train_id import TrainId


def test_activity_type_syntax():
    n = activity.Type.DETACH_ENGINE_REAR
    assert n.value == (4, "DER")
    assert n.xml_code == 4
    assert n.label == "DER"


activities = [
    (activity.Next("1A20"), "N:1A20"),
    (activity.Join("1A21"), "J:1A21"),
    (activity.DivideRear("1A22"), "DR:1A22"),
    (activity.DivideFront("1A23"), "DF:1A23"),
    (activity.DetachEngineRear("1A24"), "DER:1A24"),
    (activity.DetachEngineFront("1A25"), "DEF:1A25"),
    (activity.DropCoachesRear("1A26"), "DCR:1A26"),
    (activity.DropCoachesFront("1A27"), "DCF:1A27"),
    (activity.PlatformShare("1A28"), "PS:1A28"),
]


@pytest.mark.parametrize("act,text", activities)
def test_activity_to_str(act, text):
    assert str(act) == text


@pytest.mark.parametrize(
    "act,xml_str",
    [
        (
            activity.Next(TrainId(id="0A00")),
            "<Activity><Activity>0</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            activity.Next(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>0</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            activity.Join(TrainId(id="0A00")),
            "<Activity><Activity>3</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            activity.DivideRear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>1</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            activity.DivideFront(TrainId(id="0A00")),
            "<Activity><Activity>2</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            activity.DetachEngineRear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>4</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            activity.DetachEngineFront(TrainId(id="0A00")),
            "<Activity><Activity>5</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            activity.DropCoachesRear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>6</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            activity.DropCoachesFront(TrainId(id="0A00")),
            "<Activity><Activity>7</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            activity.PlatformShare(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>9</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
    ],
)
def test_activity_to_xml(xml_test_tools, act, xml_str):
    xt = xml_test_tools
    expected = xt.fromstr(xml_str)
    xt.assert_equivalent(expected, act.xml())
