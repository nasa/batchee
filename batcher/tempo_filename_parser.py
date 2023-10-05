"""Holds the logic for grouping together data files based on their filenames."""
import logging
import re
from argparse import ArgumentParser
from pathlib import Path

tempo_granule_filename_pattern = re.compile(
    r"^.*TEMPO_"
    r"(?P<product_type>[1-9A-Z]+)"
    r"(?P<proxy>(?:-PROXY)*)_"
    r"(?P<processing_level>L[0-9])_"
    r"(?P<version_id>V[0-9]+)_"
    r"(?P<day_in_granule>[0-9]{8})T"
    r"(?P<time_in_granule>[0-9]{6})Z_"
    r"(?P<daily_scan_id>S[0-9]{3})"
    r"(?P<granule_id>G[0-9]{2}).*\.nc"
)


def get_batch_indices(filenames: list) -> list[int]:
    """
    Returns
    -------
    list[int]
        batch index for each filename in the original list, e.g. [0, 0, 0, 1, 1, 1, ...]
    """
    # Make a new list with days and scans, e.g. [('20130701', 'S009'), ('20130701', 'S009'), ...]
    day_and_scans: list[tuple[str, str]] = []
    for name in filenames:
        matches = tempo_granule_filename_pattern.match(name)
        if matches:
            match_dict = matches.groupdict()
            day_and_scans.append((match_dict["day_in_granule"], match_dict["daily_scan_id"]))

    # Unique day-scans are determined (while keeping the same order). Each will be its own batch.
    unique_day_scans: list[tuple[str, str]] = sorted(set(day_and_scans), key=day_and_scans.index)

    # Map each day/scan to an integer
    batch_mapper: dict[tuple[str, str], int] = {
        day_scan: idx for idx, day_scan in enumerate(unique_day_scans)
    }

    # Generate a new list with the integer representation for each entry in the original list
    return [batch_mapper[day_scan] for day_scan in day_and_scans]


def main() -> list[list[str]]:
    """Main CLI entrypoint"""

    parser = ArgumentParser(
        prog="batchee", description="Simple CLI wrapper around the granule batcher module."
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

    input_filenames = [str(Path(f).resolve()) for f in args.file_names]

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
