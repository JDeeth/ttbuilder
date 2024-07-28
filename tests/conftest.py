import copy
import pytest

from xmldiff import main as xd


class XMLTestTools:
    @staticmethod
    def sort(data):
        data = copy.deepcopy(data)
        for parent in data.xpath("//*[./*]"):
            parent[:] = sorted(parent, key=lambda x: x.tag)
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


@pytest.fixture
def xml_test_tools():
    return XMLTestTools()
