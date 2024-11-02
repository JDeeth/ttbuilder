import pytest
from ttbuilder.common import activity


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
def test_activity_from_str_with_parser(text, act, ttparser):
    assert ttparser.parse_activity(text) == act


def test_can_provide_uid(ttparser):
    act = ttparser.parse_activity("N:1A23/BCD456")
    assert act.associated_train_id.id == "1A23"
    assert act.associated_train_id.uid == "BCD456"
