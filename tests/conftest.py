import copy
import pytest

from xmldiff import main as xd
from lxml import etree


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
    def agnostic_diff(cls, left, right):
        left = cls.strip_empty_str(left)
        right = cls.strip_empty_str(right)
        result = cls.unordered_diff(left, right)
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


@pytest.fixture
def xml_test_tools():
    return XMLTestTools()
