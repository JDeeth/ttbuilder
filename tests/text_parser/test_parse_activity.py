import pytest
from ttbuilder.common.activity import Activity


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
def test_activity_from_str_with_parser(text, activity, ttparser):
    assert ttparser.parse_activity(text) == activity


def test_invalid_str_makes_null_activity():
    assert not Activity.from_str("X:0A00")


def test_can_provide_uid(ttparser):
    activity = ttparser.parse_activity("N:1A23/BCD456")
    assert activity.associated_train_id.id == "1A23"
    assert activity.associated_train_id.uid == "BCD456"
