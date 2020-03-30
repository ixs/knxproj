"""Read a knxproj and display all group addresses and devices."""

import logging
import sys
from pathlib import Path

from knxproj.knxproj import KnxprojLoader


def main(knxproj_path):
    """Log all provided group addresses and devices."""

    group_addresses, devices = KnxprojLoader(knxproj_path=Path(knxproj_path)).run()

    logging.info("Group addresses:")
    for group_addr in group_addresses:
        logging.info("\t%s", group_addr)

    logging.info("Devices:")
    for dev in devices:
        logging.info("\t%s", dev)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
