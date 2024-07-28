from helper import Version, xml_escape
import pytest


def test_version_major_only():
    v = Version(3)
    assert v.text == "3"


def test_version_major_minor():
    v = Version(5, 15)
    assert v.text == "5.15"


def test_version_full():
    v = Version(1, 34, 2)
    assert v.text == "1.34.2"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("", ""),
        ("a", "a"),
        ("A", "A"),
        ("1", "1"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&apos;"),
        ("£", "&#x00A3;"),
        ('"Hello,", he lied.', "&quot;Hello,&quot;, he lied."),
    ],
)
def test_xml_escape(test_input, expected):
    assert xml_escape(test_input) == expected
