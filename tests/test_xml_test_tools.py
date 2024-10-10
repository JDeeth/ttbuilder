from lxml import etree


def test_sort(xml_test_tools):
    unsorted = etree.XML("<root><d/><b/><c/><a><a3/><a2>hi</a2><a1/></a></root>")
    sorted = "<root><a><a1/><a2>hi</a2><a3/></a><b/><c/><d/></root>"
    assert etree.tostring(xml_test_tools.sort(unsorted)).decode() == sorted


def test_sort_does_not_mutate_in_place(xml_test_tools):
    xml_str = "<root><B/><A/></root>"
    unsorted = etree.XML(xml_str)
    xml_test_tools.sort(unsorted)
    assert etree.tostring(unsorted).decode() == xml_str


def test_strip(xml_test_tools):
    # all <X></X> should be replaced with <X/>
    initial = etree.Element("root")
    etree.SubElement(initial, "A")
    etree.SubElement(initial, "B").text = ""
    c = etree.SubElement(initial, "C")
    etree.SubElement(c, "C1")
    etree.SubElement(c, "C2").text = ""

    stripped = xml_test_tools.strip_empty_str(initial)
    assert (
        etree.tostring(initial).decode()
        == "<root><A/><B></B><C><C1/><C2></C2></C></root>"
    )
    assert etree.tostring(stripped).decode() == "<root><A/><B/><C><C1/><C2/></C></root>"


def test_xml_unordered_diff(xml_test_tools):
    unsorted = etree.Element("root")
    etree.SubElement(unsorted, "C")
    b = etree.SubElement(unsorted, "B")
    etree.SubElement(b, "B3")
    etree.SubElement(b, "B1")
    etree.SubElement(b, "B2").text = "hi"
    etree.SubElement(unsorted, "A")

    sorted = etree.Element("root")
    etree.SubElement(sorted, "A")
    b = etree.SubElement(sorted, "B")
    etree.SubElement(b, "B1")
    etree.SubElement(b, "B2").text = "hi"
    etree.SubElement(b, "B3")
    etree.SubElement(sorted, "C")

    assert xml_test_tools.unordered_diff(sorted, unsorted) == []


def test_agnostic_diff(xml_test_tools):
    left = etree.Element("root")
    etree.SubElement(left, "A")
    b = etree.SubElement(left, "B")
    etree.SubElement(b, "B1")
    etree.SubElement(b, "B2").text = ""
    etree.SubElement(left, "C").text = ""

    right = etree.Element("root")
    b = etree.SubElement(right, "B")
    etree.SubElement(b, "B2")
    etree.SubElement(b, "B1").text = ""
    etree.SubElement(right, "A")
    etree.SubElement(right, "C")

    assert xml_test_tools.agnostic_diff(left, right) == []
    xml_test_tools.assert_equivalent(left, right)


def test_ignore_uid_change_diff(xml_test_tools):
    left = etree.Element("root")
    etree.SubElement(left, "ID").text = "2A01"
    etree.SubElement(left, "UID").text = "AAA111"

    right = etree.Element("root")
    etree.SubElement(right, "ID").text = "2A01"
    etree.SubElement(right, "UID").text = "BBB222"

    assert xml_test_tools.agnostic_diff(left, right, ignore_uid=True) == []
    xml_test_tools.assert_equivalent(left, right, ignore_uid=True)
