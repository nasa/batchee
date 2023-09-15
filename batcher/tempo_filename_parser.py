"""Holds the logic for grouping together data files based on their filenames."""
import re
from typing import Dict, List, Tuple

example_filenames = [
    "TEMPO_HCHO_L2_V01_20130701T212354Z_S009G05.nc",
    "TEMPO_HCHO_L2_V01_20130701T212953Z_S009G06.nc",
    "TEMPO_HCHO_L2_V01_20130701T213553Z_S009G07.nc",
    "TEMPO_HCHO_L2_V01_20130701T215955Z_S010G01.nc",
    "TEMPO_HCHO_L2_V01_20130701T220554Z_S010G02.nc",
    "TEMPO_HCHO_L2_V01_20130701T221154Z_S010G03.nc",
]

tempo_granule_filename_pattern = re.compile(
    r"TEMPO_"
    r"(?P<product_type>[1-9A-Z]+)"
    r"(?P<proxy>(?:-PROXY)*)_"
    r"(?P<processing_level>L[0-9])_"
    r"(?P<version_id>V[0-9]+)_"
    r"(?P<day_in_granule>[0-9]{8})T"
    r"(?P<time_in_granule>[0-9]{6})Z_"
    r"(?P<daily_scan_id>S[0-9]{3})"
    r"(?P<granule_id>G[0-9]{2}).*\.nc"
)


def get_unique_day_scan_categories(filenames: list) -> List[int]:
    """
    Returns
    -------
    list[int]
        category integer for each filename in the original list, e.g. [0, 0, 0, 1, 1, 1, ...]
    """
    # Make a new list with days and scans, e.g. [('20130701', 'S009'), ('20130701', 'S009'), ...]
    day_and_scans: List[Tuple[str, str]] = []
    for name in filenames:
        matches = tempo_granule_filename_pattern.match(name)
        if matches:
            match_dict = matches.groupdict()
            day_and_scans.append((match_dict["day_in_granule"], match_dict["daily_scan_id"]))

    # Unique categories are determined, while keeping the same order
    unique_day_scans: List[Tuple[str, str]] = sorted(set(day_and_scans), key=day_and_scans.index)

    # Map each day/scan to an integer
    category_mapper: Dict[Tuple[str, str], int] = {
        day_scan: idx for idx, day_scan in enumerate(unique_day_scans)
    }

    # Generate a new list with the integer representation for each entry in the original list
    return [category_mapper[day_scan] for day_scan in day_and_scans]


print(get_unique_day_scan_categories(example_filenames))
