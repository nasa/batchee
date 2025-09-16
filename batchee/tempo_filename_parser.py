# Copyright 2024 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration. All Rights Reserved.
#
# This software calls the following third-party software, which is subject to the terms and
# conditions of its licensor, as applicable.  Users must license their own copies;
# the links are provided for convenience only.
#
# Harmony-service-lib-py
# https://www.apache.org/licenses/LICENSE-2.0
# https://github.com/nasa/harmony-service-lib-py?tab=License-1-ov-file
#
# pystac
# https://github.com/stac-utils/pystac/blob/main/LICENSE
# https://www.apache.org/licenses/LICENSE-2.0
#
# Python Standard Library (version 3.10)
# https://docs.python.org/3/license.html#psf-license
#
# The Batchee: Granule batcher service to support concatenation platform is licensed under the
# Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
"""Holds the logic for grouping together data files based on their filenames."""

import logging
import re
from argparse import ArgumentParser
from datetime import datetime
from zoneinfo import ZoneInfo

default_logger = logging.getLogger(__name__)

tempo_granule_filename_pattern = re.compile(
    r"^.*TEMPO_"
    r"(?P<product_type>[1-9A-Z]+)"
    r"(?P<proxy>(?:-PROXY)*)_"
    r"(?P<processing_level>L[0-9])_"
    r"(?P<nrt>NRT_)?"
    r"(?P<version_id>V[0-9]+)_"
    r"(?P<day_in_granule>[0-9]{8})T"
    r"(?P<time_in_granule>[0-9]{6})Z_"
    r"(?P<daily_scan_id>S[0-9]{3})"
    r"(?P<granule_id>G[0-9]{2}).*\.nc"
)


def get_day_in_us_central(
    day_in_granule: str, time_in_granule: str, assume_tz=ZoneInfo("UTC")
) -> str:
    """
    Convert a datetime to US Central time (US/Central) and return
    a timezone-aware datetime.

    Parameters
    ----------
    day_in_granule: str
        The day from granule filename
    time_in_granule: str
        The time from granule filename
    assume_tz : timezone, optional (default: UTC)
        this is the timezone in which `day_in_granule` and `time_in_granule`
        should be interpreted before converting to Central.

    Returns
    -------
    str
        The day for datetime converted to US/Central
    """

    dt = datetime.strptime(day_in_granule + time_in_granule, "%Y%m%d%H%M%S")
    dt = dt.replace(tzinfo=assume_tz)

    dt_central = dt.astimezone(ZoneInfo("America/Chicago"))
    return dt_central.strftime("%Y%m%d")


def get_batch_indices(filenames: list, logger: logging.Logger = default_logger) -> list[int]:
    """
    Returns
    -------
    list[int]
        batch index for each filename in the original list, e.g. [0, 0, 0, 1, 1, 1, ...]
    """
    logger.info(f"get_batch_indices() starting --- with {len(filenames)} filenames")

    # Make a new list with days and scans, e.g. [('20130701', 'S009'), ('20130701', 'S009'), ...]
    day_and_scans: list[tuple[str, str]] = []
    for name in filenames:
        matches = tempo_granule_filename_pattern.match(name)
        if matches:
            match_dict = matches.groupdict()
            day_in_central = get_day_in_us_central(
                match_dict["day_in_granule"], match_dict["time_in_granule"]
            )
            day_and_scans.append((day_in_central, match_dict["daily_scan_id"]))

    # Unique day-scans are determined (while keeping the same order). Each will be its own batch.
    unique_day_scans: list[tuple[str, str]] = sorted(set(day_and_scans), key=day_and_scans.index)

    logger.info(f"unique_day_scans==={unique_day_scans}.")

    # Map each day/scan to an integer
    batch_mapper: dict[tuple[str, str], int] = {
        day_scan: idx for idx, day_scan in enumerate(unique_day_scans)
    }

    # Generate a new list with the integer representation for each entry in the original list
    return [batch_mapper[day_scan] for day_scan in day_and_scans]


def main() -> list[list[str]]:
    """Main CLI entrypoint"""

    parser = ArgumentParser(
        prog="batchee",
        description="Simple CLI wrapper around the granule batchee module.",
    )
    parser.add_argument(
        "file_names",
        nargs="+",
        help="A space-separated list of filenames for which batches will be determined.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose output to stdout; useful for debugging",
        action="store_true",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    input_filenames = args.file_names

    batch_indices = get_batch_indices(input_filenames)
    unique_category_indices: list[int] = sorted(set(batch_indices), key=batch_indices.index)
    logging.info(f"batch_indices = {batch_indices}")

    # --- Construct a STAC object based on the batch indices ---
    grouped: dict[int, list[str]] = {}
    for k, v in zip(batch_indices, input_filenames):
        grouped.setdefault(k, []).append(v)
    grouped_names: list[list[str]] = [grouped[k] for k in unique_category_indices]

    return grouped_names


if __name__ == "__main__":
    main()
