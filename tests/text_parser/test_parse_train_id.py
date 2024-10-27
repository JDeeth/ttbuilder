import pytest
from ttbuilder.common.train_id import TrainId


@pytest.mark.parametrize(
    "text,train_id_args",
    [
        ("1A01", {"id": "1A01"}),
        ("1A01/ABC234", {"id": "1A01", "uid": "ABC234"}),
    ],
)
def test_train_id_from_str_with_parser(text, train_id_args, ttime_parser):
    assert ttime_parser.parse(text) == TrainId(**train_id_args)
