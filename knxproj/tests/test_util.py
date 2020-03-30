"""Test the knxproj."""
from xml.etree import ElementTree as ET

import pytest

from ..util import ETS_NAMESPACES, FinderXml, postfix, to_list
from .util import (  # noqa: F401  # pylint:disable=unused-import
    get_groupaddress,
    param_bools,
    param_none_numbers,
    xml_knx,
)

# pylint: disable=redefined-outer-name,protected-access


@pytest.mark.parametrize("expected_count", [None, 0, 1, 10])
@pytest.mark.parametrize("namespace", [None, "ets56", "ets57"])
def test_finder_xml(namespace, expected_count):
    """Test the finder function with namespace variation."""
    # Setup xml
    xml = ET.Element("KNX")
    if namespace:
        xml.attrib["xmlns"] = ETS_NAMESPACES[namespace]
    # Add keyword / value
    keyword = "Foo"
    payload = {"Bar": "Baz"}
    if expected_count is None:
        counts = range(1)
    else:
        counts = range(expected_count)
    for _ in counts:
        for key, value in payload.items():
            ET.SubElement(xml, keyword).attrib[key] = value
    xml_string = ET.tostring(xml, encoding="utf-8").decode("utf-8")

    # Setup finder
    finder = FinderXml(namespace=namespace)
    assert callable(finder)

    # Find
    result = finder(
        ET.fromstring(xml_string), keyword=keyword, expected_count=expected_count
    )

    # TODO: Fix special treatment of 1 finding
    if expected_count == 1:
        result = to_list(result)
    assert isinstance(result, list)

    for res in result:
        assert res.attrib == payload


def test_postfix():
    """Test that the separator is properly attended."""
    assert postfix("foo") == "foo_"
    assert postfix("foo", "+") == "foo+"


def test_to_list():
    """Test the "to_list" function."""
    in_ = 12
    actual = to_list(in_)
    assert [in_] == actual
    assert isinstance(actual, list)

    in_ = [12]
    assert in_ == to_list(in_)

    in_ = "ab"
    assert [in_] == to_list(in_)

    in_ = (12, 34)
    assert [12, 34] == to_list(in_)


if __name__ == "__main__":
    pytest.main(["-x"])
