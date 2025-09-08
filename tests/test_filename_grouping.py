import sys
from unittest.mock import patch

import batchee.tempo_filename_parser
from batchee.tempo_filename_parser import get_batch_indices, get_day_in_us_central

example_filenames = [
    "TEMPO_NO2_L2_V03_20240731T235252Z_S016G04.nc",
    "TEMPO_NO2_L2_V03_20240731T235929Z_S016G05.nc",
    "TEMPO_NO2_L2_V03_20240801T000606Z_S016G06.nc",
    "TEMPO_NO2_L2_V03_20240801T001302Z_S017G01.nc",
    "TEMPO_NO2_L2_V03_20240801T001942Z_S017G02.nc",
    "TEMPO_NO2_L2_V03_20240801T002619Z_S017G03.nc",
    "TEMPO_NO2_L2_V03_20240801T233313Z_S016G01.nc",
    "TEMPO_NO2_L2_V03_20240801T233953Z_S016G02.nc",
    "TEMPO_NO2_L2_V03_20240801T234630Z_S016G03.nc",
]

example_nrt_filenames = [
    "TEMPO_NO2_L2_NRT_V02_20250711T183227Z_S010G04.nc",
    "TEMPO_NO2_L2_NRT_V02_20250711T183904Z_S010G05.nc",
    "TEMPO_NO2_L2_NRT_V02_20250711T184541Z_S010G06.nc",
    "TEMPO_NO2_L2_NRT_V02_20250711T185856Z_S010G08.nc",
    "TEMPO_NO2_L2_NRT_V02_20250712T000606Z_S016G03.nc",
    "TEMPO_NO2_L2_NRT_V02_20250712T001927Z_S016G05.nc",
    "TEMPO_NO2_L2_NRT_V02_20250712T161248Z_S008G01.nc",
    "TEMPO_NO2_L2_NRT_V02_20250712T162608Z_S008G03.nc",
    "TEMPO_NO2_L2_NRT_V02_20250712T170552Z_S008G09.nc",
]


def test_timezone_conversion():
    utcdates = [filename.split("_")[4] for filename in example_filenames]
    days_in_central = [get_day_in_us_central(utcdt[0:8], utcdt[9:15]) for utcdt in utcdates]
    assert days_in_central == [
        "20240731",
        "20240731",
        "20240731",
        "20240731",
        "20240731",
        "20240731",
        "20240801",
        "20240801",
        "20240801",
    ]


def test_grouping():
    results = get_batch_indices(example_filenames)

    assert results == [0, 0, 0, 1, 1, 1, 2, 2, 2]


def test_nrt_grouping():
    results = get_batch_indices(example_nrt_filenames)

    assert results == [0, 0, 0, 0, 1, 1, 2, 2, 2]


def test_main_cli():
    test_args = [batchee.tempo_filename_parser.__file__, "-v"]
    test_args.extend(example_filenames)

    with patch.object(sys, "argv", test_args):
        grouped_names = batchee.tempo_filename_parser.main()

    assert grouped_names == [example_filenames[0:3], example_filenames[3:6], example_filenames[6:9]]
