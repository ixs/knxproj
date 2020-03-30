"""Read a knxproj and dump it to a json file."""

import json
import logging
import sys
from collections import OrderedDict
from pathlib import Path

from knxproj.knxproj import KnxprojLoader


def main(knxproj_path, json_path="knx_mapping.json"):
    """Dump a dictionary that links group_addresses to data types."""

    # If a path is provided, take it.
    try:
        knxproj_path = sys.argv[1]
    except IndexError:
        pass

    group_addresses, _ = KnxprojLoader(knxproj_path=Path(knxproj_path)).run()

    # Iterate over group addresses and create mapping
    groupaddress_to_dtype = {}
    for group_address in group_addresses:
        groupaddress_to_dtype[group_address.get_ga_str()] = {
            "dtype": group_address.dtype,
            "name": group_address.name,
        }

    ordered_by_address = OrderedDict(sorted(groupaddress_to_dtype.items()))

    with open(json_path, "w", encoding="utf-8") as file_:
        json.dump(ordered_by_address, file_, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1])
