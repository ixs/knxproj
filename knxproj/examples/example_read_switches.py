"""Read a knxproj and display all group addresses and devices."""

import logging
import sys
from pathlib import Path

from knxproj.devices import dev2vendor
from knxproj.devices.devices import Switch
from knxproj.knxproj import KnxprojLoader


def main(knxproj_path):
    """Log all provided group addresses and devices."""

    # Generic, non-vendor specific
    _, devices = KnxprojLoader(knxproj_path=Path(knxproj_path)).run()

    # Get in the vendor specifics
    devices = [dev2vendor(dev) for dev in devices]

    logging.info("Switches:")
    for dev in devices:
        if isinstance(dev, Switch):
            dev.doc()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1])
