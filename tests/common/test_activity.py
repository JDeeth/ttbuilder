import pytest

from common import Activity, ActivityType, TrainId


def test_activity_type_syntax():
    n = ActivityType.DETACH_ENGINE_REAR
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


@pytest.mark.parametrize("activity,text", activities)
def test_activity_from_str(text, activity):
    assert Activity.from_str(text) == activity


def test_invalid_str_makes_null_activity():
    assert not Activity.from_str("X:0A00")


def test_can_provide_uid():
    activity = Activity.from_str("N:1A23/BCD456")
    assert activity.associated_train_id.id == "1A23"
    assert activity.associated_train_id.uid == "BCD456"


@pytest.mark.parametrize(
    "activity,xml_str",
    [
        (
            Activity(ActivityType.NEXT, TrainId(id="0A00")),
            "<Activity><Activity>0</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity(ActivityType.NEXT, TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>0</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity(ActivityType.JOIN, TrainId(id="0A00")),
            "<Activity><Activity>3</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity(ActivityType.DIVIDE_REAR, TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>1</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity(ActivityType.DIVIDE_FRONT, TrainId(id="0A00")),
            "<Activity><Activity>2</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity(ActivityType.DETACH_ENGINE_REAR, TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>4</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity(ActivityType.DETACH_ENGINE_FRONT, TrainId(id="0A00")),
            "<Activity><Activity>5</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity(ActivityType.DROP_COACHES_REAR, TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>6</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        (
            Activity(ActivityType.DROP_COACHES_FRONT, TrainId(id="0A00")),
            "<Activity><Activity>7</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        ),
        (
            Activity(ActivityType.PLATFORM_SHARE, TrainId(id="0A00", uid="ABC123")),
            "<Activity><Activity>9</Activity><AssociatedUID>ABC123</AssociatedUID></Activity>",
        ),
        # (
        #     Activity(ActivityType.CREW_CHANGE, TrainId(id="0A00")),
        #     "<Activity><Activity>10</Activity><AssociatedTrain>0A00</AssociatedTrain></Activity>",
        # ),
    ],
)
def test_activity_to_xml(xml_test_tools, activity, xml_str):
    xt = xml_test_tools
    expected = xt.fromstr(xml_str)
    xt.assert_equivalent(expected, activity.xml())
