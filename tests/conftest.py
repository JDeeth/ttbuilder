import copy
import pytest

from xmldiff import main as xd
from lxml import etree

from ttbuilder.text_parser.tt_parser import TTParser


class XMLTestTools:
    """Collection of test methods packaged for a Pytest fixture"""

    @staticmethod
    def sort(data):
        data = copy.deepcopy(data)
        for parent in data.xpath("//*[./*]"):
            parent[:] = sorted(
                parent, key=lambda x: x.tag if isinstance(x.tag, str) else ""
            )
        return data

    @staticmethod
    def strip_empty_str(data):
        data = copy.deepcopy(data)
        for x in data.xpath("//*"):
            if x.text == "":
                x.text = None
        return data

    @classmethod
    def unordered_diff(cls, left, right):
        left = cls.sort(left)
        right = cls.sort(right)
        result = xd.diff_trees(left, right)
        return result

    @classmethod
    def agnostic_diff(cls, left, right, ignore_uid=False):
        left = cls.strip_empty_str(left)
        right = cls.strip_empty_str(right)
        result = cls.unordered_diff(left, right)
        if ignore_uid:
            result = [x for x in result if "UID" not in str(x)]
        return result

    @classmethod
    def fromfile(cls, path: str, **parser_args):
        parser_args.setdefault("remove_blank_text", True)
        parser = etree.XMLParser(**parser_args)
        return etree.parse(path, parser=parser)

    @classmethod
    def fromstr(cls, xml_text: str, **parser_args):
        parser_args.setdefault("remove_blank_text", True)
        parser = etree.XMLParser(**parser_args)
        return etree.XML(xml_text, parser=parser)

    @classmethod
    def pretty(cls, xml):
        return etree.tostring(xml, pretty_print=True, encoding="unicode")

    @classmethod
    def assert_equivalent(cls, left, right, ignore_uid=False):
        assert cls.agnostic_diff(left, right, ignore_uid) == []


@pytest.fixture
def xml_test_tools():
    return XMLTestTools()


def xfail(*args, reason=None):
    """Wraps a pytest.mark.parametrize param as xfail"""
    if reason:
        mark = pytest.mark.xfail(reason=reason)
    else:
        mark = pytest.mark.xfail
    return pytest.param(*args, marks=mark)


@pytest.fixture(name="ttparser", scope="session")
def fixture_ttparser():
    return TTParser()
