import pytest

from ttbuilder.common.str_helper import pascal_case, xml_escape


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
        (""""a" 'b' & £5""", "&quot;a&quot; &apos;b&apos; &amp; &#x00A3;5"),
    ],
)
def test_xml_escape(test_input, expected):
    assert xml_escape(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("", ""),
        ("a", "A"),
        ("1", "1"),
        ("1a", "1a"),
        ("aa_bb", "AaBb"),
        ("aaa_bbb_ccc", "AaaBbbCcc"),
        ("aa_11_bb", "Aa11Bb"),
    ],
)
def test_pascal(test_input, expected):
    assert pascal_case(test_input) == expected
