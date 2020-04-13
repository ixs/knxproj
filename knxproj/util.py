"""Provide the base attributes of an KNX element."""

import xml.etree.ElementTree as ET
from collections.abc import Iterable
from typing import Optional

import attr
from attr.validators import instance_of

# The ETS namespace depend on the ETS version.
# Right now only ETS 5.7 is supported.
# The xml structure between ETS 5.6 and 5.7 changed.
ETS_NAMESPACES = {
    "ets56": "http://knx.org/xml/project/14",
    "ets57": "http://knx.org/xml/project/20",
}


def postfix(prefix: str, sep: str = "_") -> str:
    """Add a postfix, default to '_' to the prefix."""
    return "".join((prefix, sep))


def to_list(in_) -> list:
    """Convert an instance to a list if its not a list."""
    if isinstance(in_, list):
        return in_

    if isinstance(in_, Iterable) and not isinstance(in_, str):
        return list(in_)

    return [in_]


@attr.s
class KNXBase:
    """Class with all common knx information."""

    id_ = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=instance_of(str))


@attr.s
class KNXAddress(KNXBase):
    """KNXBase w/ address."""

    address = attr.ib(converter=int, validator=instance_of(int))


@attr.s(auto_attribs=True)
class FinderXml:
    """Create a namespaced xml findall."""

    # Should be an ets namespace
    # i.e. "ets56" or "ets57"
    namespace: Optional[str] = None

    def __call__(
        self, xml: ET.Element, keyword: str, expected_count: Optional[int] = None
    ):
        """Find all elements in an xml.

        If an expected count is given iit is asserted that exaclty n elements are found.

        If expected count == 1, only that element is returned, no list.
        """
        # Adapt to namespace
        if self.namespace:
            keyword_ns = f"{self.namespace}:{keyword}"
        else:
            keyword_ns = keyword

        # Find all items
        items = xml.findall(keyword_ns, namespaces=ETS_NAMESPACES)
        if expected_count:
            assert len(items) == expected_count

        if expected_count == 1:
            return items[0]

        return items
