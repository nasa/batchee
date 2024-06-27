import json
import sys
from os import environ
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

import pytest

import batcher.harmony.cli


@pytest.mark.usefixtures("pass_options")
class TestBatching:
    __test_path = Path(__file__).parent.resolve()
    __data_path = __test_path.joinpath("data")
    __harmony_path = __data_path.joinpath("harmony")

    def test_service_invoke(self, temp_output_dir):
        in_message_path = self.__harmony_path.joinpath("message.json")
        in_message_data = in_message_path.read_text()

        # test with both paged catalogs and un-paged catalogs
        for in_catalog_name in ["catalog.json", "catalog0.json"]:

            in_catalog_path = self.__harmony_path.joinpath("source", in_catalog_name)

            test_args = [
                batcher.harmony.cli.__file__,
                "--harmony-action",
                "invoke",
                "--harmony-input",
                in_message_data,
                "--harmony-source",
                str(in_catalog_path),
                "--harmony-metadata-dir",
                str(temp_output_dir),
                "--harmony-data-location",
                temp_output_dir.as_uri(),
            ]

            test_env = {
                "ENV": "dev",
                "OAUTH_CLIENT_ID": "",
                "OAUTH_UID": "",
                "OAUTH_PASSWORD": "",
                "OAUTH_REDIRECT_URI": "",
                "STAGING_PATH": "",
                "STAGING_BUCKET": "",
            }

            with patch.object(sys, "argv", test_args), patch.dict(environ, test_env):
                batcher.harmony.cli.main()

            # Open the outputs
            out_batch_catalog_path = temp_output_dir.joinpath("batch-catalogs.json")
            out_batch_catalogs = json.loads(out_batch_catalog_path.read_text())

            # Go through each batched catalog
            batched_files = {0: [], 1: [], 2: []}
            for batch_index, catalog in enumerate(out_batch_catalogs):
                out_catalog_path = temp_output_dir.joinpath(catalog)
                out_catalog = json.loads(out_catalog_path.read_text())

                for item_meta in out_catalog["links"]:
                    if item_meta["rel"] == "item":
                        item_path = temp_output_dir.joinpath(item_meta["href"]).resolve()

                        # -- Item Verification --
                        item = json.loads(item_path.read_text())
                        properties = item["properties"]
                        assert item["bbox"]
                        assert properties["start_datetime"]
                        assert properties["end_datetime"]

                        # -- Asset Verification --
                        data = item["assets"]["data"]

                        # Sanity checks on metadata
                        assert data["type"] == "application/x-netcdf4"
                        assert data["roles"] == ["data"]

                        batched_files[batch_index].append(Path(urlsplit(data["href"]).path).stem)

            # -- batch file list verification --
            files_dict = {
                0: [
                    "TEMPO_NO2_L2_V03_20240601T120101Z_S012G01",
                    "TEMPO_NO2_L2_V03_20240601T120107Z_S012G02",
                ],
                1: [
                    "TEMPO_NO2_L2_V03_20240601T120202Z_S013G01",
                    "TEMPO_NO2_L2_V03_20240601T120209Z_S013G02",
                ],
                2: [
                    "TEMPO_NO2_L2_V03_20240601T120303Z_S014G01",
                    "TEMPO_NO2_L2_V03_20240601T120310Z_S014G02",
                ],
            }

            assert batched_files == files_dict
