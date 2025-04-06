import pytest

from ttbuilder.common.activity import Activity
from ttbuilder.common.train_id import TrainId


def test_activity_type_syntax():
    n = Activity.Type.DETACH_ENGINE_REAR
    assert n.value == (4, "DER")
    assert n.xml_code == 4
    assert n.label == "DER"


activities = [
    (Activity.next("1A20"), "N:1A20"),
    (Activity.join("1A21"), "J:1A21"),
    (Activity.divide_rear("1A22"), "DR:1A22"),
    (Activity.divide_front("1A23"), "DF:1A23"),
    (Activity.detach_engine_rear("1A24"), "DER:1A24"),
    (Activity.detach_engine_front("1A25"), "DEF:1A25"),
    (Activity.drop_coaches_rear("1A26"), "DCR:1A26"),
    (Activity.drop_coaches_front("1A27"), "DCF:1A27"),
    (Activity.platform_share("1A28"), "PS:1A28"),
    # (Activity.crew_change("1A29"), "CC:1A29"),
]


@pytest.mark.parametrize("activity,text", activities)
def test_activity_to_str(activity, text):
    assert str(activity) == text


@pytest.mark.parametrize(
    "activity,xml_str",
    [
        (
            Activity.next(TrainId(id="0A00")),
            "<Activity><Activity>0</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity.next(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>0</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity.join(TrainId(id="0A00")),
            "<Activity><Activity>3</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity.divide_rear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>1</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity.divide_front(TrainId(id="0A00")),
            "<Activity><Activity>2</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity.detach_engine_rear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>4</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity.detach_engine_front(TrainId(id="0A00")),
            "<Activity><Activity>5</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity.drop_coaches_rear(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>6</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity.drop_coaches_front(TrainId(id="0A00")),
            "<Activity><Activity>7</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity.platform_share(TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>9</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        # (
        #     Activity.crew_change(TrainId(id="0A00")),
        #     "<Activity><Activity>10</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        # ),
    ],
)
def test_activity_to_xml(xt, activity, xml_str):
    expected = xt.fromstr(xml_str)
    xt.assert_equivalent(expected, activity.xml())
