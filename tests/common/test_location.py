from ttbuilder.common.location import Location


def test_location_is_truthy():
    assert Location(tiploc="SODOR")
    assert not Location(tiploc="")
