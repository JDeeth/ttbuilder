from version import Version


def test_major_only():
    v = Version(3)
    assert v.text == "3"


def test_major_minor():
    v = Version(5, 15)
    assert v.text == "5.15"


def test_full():
    v = Version(1, 34, 2)
    assert v.text == "1.34.2"
