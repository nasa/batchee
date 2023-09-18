from batcher.tempo_filename_parser import get_unique_day_scan_categories

example_filenames = [
    "TEMPO_HCHO_L2_V01_20130701T212354Z_S009G05.nc",
    "TEMPO_HCHO_L2_V01_20130701T212953Z_S009G06.nc",
    "TEMPO_HCHO_L2_V01_20130701T213553Z_S009G07.nc",
    "TEMPO_HCHO_L2_V01_20130701T215955Z_S010G01.nc",
    "TEMPO_HCHO_L2_V01_20130701T220554Z_S010G02.nc",
    "TEMPO_HCHO_L2_V01_20130701T221154Z_S010G03.nc",
]


def test_grouping():
    results = get_unique_day_scan_categories(example_filenames)

    assert results == [0, 0, 0, 1, 1, 1]
