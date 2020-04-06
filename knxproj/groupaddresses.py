"""Classes and helpers related to the KNX groupaddresses."""

import logging
from xml.etree.ElementTree import Element as xml_element

import attr
from attr.validators import instance_of

from .util import KNXAddress, KNXBase, postfix


@attr.s
class GroupRange(KNXBase):
    """KNX group range, covers "Hauptgruppe" and "Mittelgruppe"."""

    limits = attr.ib(validator=instance_of(tuple))

    @limits.validator
    def range_validate(self, _, value):
        # pylint: disable=no-self-use
        """Validate the range.

        The range must consist of a tuple of ints, where
        the first element is smaller than the second.
        """
        assert len(value) == 2
        start = value[0]
        end = value[1]

        assert isinstance(start, int)
        assert isinstance(end, int)
        assert start < end


@attr.s
class GroupAddress(KNXAddress):
    """KNX GA."""

    dtype = attr.ib(validator=instance_of(str))
    mittelgruppe: GroupRange = attr.ib(validator=instance_of(GroupRange))
    hauptgruppe: GroupRange = attr.ib(validator=instance_of(GroupRange))

    def get_ga_str(self) -> str:
        """Create a/b/c groupaddress out of the integer."""
        mg_start = self.mittelgruppe.limits[0]
        hg_start = self.hauptgruppe.limits[0]
        return "/".join(
            (
                f"{(hg_start/2048):.0f}",
                f"{((mg_start-hg_start)/256):.0f}",
                f"{(self.address-mg_start):.0f}",
            )
        )


@attr.s
class Factory:
    """Factory to create items from xml."""

    prefix = attr.ib(converter=postfix)

    def groupaddress(
        self, xml: xml_element, hauptgruppe: GroupRange, mittelgruppe: GroupRange
    ) -> GroupAddress:
        """Create a group adress from a xml."""
        try:
            dtype = xml.attrib["DatapointType"]
        except KeyError:
            logging.error("All Datapoints need an assigned DatapointType.")
            logging.error("'%s' has no dtype.", xml.attrib["Name"])
            # Warning: This can lead to problems down the chain
            dtype = "unknown"

        return GroupAddress(
            id_=xml.attrib["Id"].replace(self.prefix, ""),
            address=xml.attrib["Address"],
            name=xml.attrib["Name"],
            puid=xml.attrib["Puid"],
            dtype=dtype,
            hauptgruppe=hauptgruppe,
            mittelgruppe=mittelgruppe,
        )

    def grouprange(self, xml: xml_element) -> GroupRange:
        """Create a Grouprange from a xml."""
        start = int(xml.attrib["RangeStart"])
        end = int(xml.attrib["RangeEnd"])

        return GroupRange(
            id_=xml.attrib["Id"].replace(self.prefix, ""),
            name=xml.attrib["Name"],
            puid=xml.attrib["Puid"],
            limits=(start, end),
        )
