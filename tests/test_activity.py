import pytest

from activity import Activity, ActivityType


@pytest.mark.parametrize(
    "activity,text",
    [
        (Activity.next("1A20"), "N:1A20"),
    ],
)
def test_activity_to_str(activity, text):
    assert str(activity) == text
