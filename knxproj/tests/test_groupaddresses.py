"""Test groupadresses."""
# pylint: disable=redefined-outer-name, unused-argument

from copy import copy

import pytest

from ..groupaddresses import GroupAddress, GroupRange
from .util import (  # noqa: F401  # pylint:disable=unused-import
    get_groupaddress,
    get_groupaddress_factory,
    get_grouprange,
    param_bools,
    xml_knx,
)


def test_grouprange(get_grouprange):
    """Ensure that Groupranges validate their limits."""

    # Valid group range
    assert isinstance(get_grouprange, GroupRange)

    for limits in [(1,), ("eins", 2), (1, "zwei"), (2, 1)]:
        with pytest.raises(AssertionError):
            GroupRange("foo", "bar", limits)


def test_groupaddress(get_groupaddress):
    """Ensure that GroupAddresses are
    - constructed as intended
    - properly translate their GA to the x/y/z format

    """

    # Valid GroupAddress
    assert isinstance(get_groupaddress, GroupAddress)

    # Fix assumptions on group range
    addr = copy(get_groupaddress)
    addr.mittelgruppe = GroupRange(id_="", name="", limits=(0, 512))
    addr.hauptgruppe = GroupRange(id_="", name="", limits=(0, 65536))

    for input_, excpected in (
        (0, "0/0/0"),
        (1, "0/0/1"),
        (255, "0/0/255"),
        (256, "0/0/256"),
    ):
        addr.address = input_
        assert addr.get_ga_str() == excpected


def test_factory_range(get_groupaddress_factory, xml_knx):
    """Test the Grouprange factory."""
    range_ = get_groupaddress_factory.grouprange(xml_knx)

    assert isinstance(range_, GroupRange)

    assert xml_knx.attrib["RangeStart"] == range_.limits[0]
    assert xml_knx.attrib["RangeEnd"] == range_.limits[1]
    assert xml_knx.attrib["Id"] == range_.id_


def test_factory_address(get_groupaddress_factory, xml_knx, get_grouprange):
    """Test the Groupaddress factory."""
    haupt = copy(get_grouprange)
    mittel = copy(get_grouprange)

    address = get_groupaddress_factory.groupaddress(
        xml_knx, hauptgruppe=haupt, mittelgruppe=mittel
    )

    assert isinstance(address, GroupAddress)
    assert xml_knx.attrib["DatapointType"] == address.dtype
    assert xml_knx.attrib["Name"] == address.name

    # Expect to fail
    del xml_knx.attrib["DatapointType"]
    with pytest.raises(KeyError):
        get_groupaddress_factory.groupaddress(
            xml_knx, hauptgruppe=haupt, mittelgruppe=mittel
        )
