"""Generic device types."""
from abc import ABC, abstractclassmethod, abstractmethod

import attr

from ..topology import Device


@attr.s
class Switch(Device, ABC):
    """Abstract switch class."""

    @abstractclassmethod
    def from_device(cls, device, *args, **kwargs):
        """Create a switch from a generic device."""

    @abstractmethod
    def doc(self):
        """Print documentation."""
