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
from uuid import uuid4

import pystac
from harmony_service_lib.adapter import BaseHarmonyAdapter
from harmony_service_lib.util import bbox_to_geometry
from pystac import Item
from pystac.item import Asset

from batchee.harmony.util import (
    _get_item_url,
    _get_netcdf_urls,
    _get_output_date_range,
)
from batchee.tempo_filename_parser import get_batch_indices


class ConcatBatching(BaseHarmonyAdapter):
    """
    A harmony-service-lib wrapper around the concatenate-batchee module.
    This wrapper does not support Harmony calls that do not have STAC catalogs
    as support for this behavior is being depreciated in harmony-service-lib
    """

    def __init__(self, message, catalog=None, config=None):
        """
        Constructs the adapter

        Parameters
        ----------
        message : harmony.Message
            The Harmony input which needs acting upon
        catalog : pystac.Catalog
            A STAC catalog containing the files on which to act
        config : harmony.util.Config
            The configuration values for this runtime environment.
        """
        super().__init__(message, catalog=catalog, config=config)

    def invoke(self):
        """
        Primary entrypoint into the service wrapper. Overrides BaseHarmonyAdapter.invoke
        """
        if not self.catalog:
            # Message-only support is being depreciated in Harmony, so we should expect to
            # only see requests with catalogs when invoked with a newer Harmony instance
            # https://github.com/nasa/harmony-service-lib-py/blob/21bcfbda17caf626fb14d2ac4f8673be9726b549/harmony/adapter.py#L71
            raise RuntimeError("Invoking Batchee without a STAC catalog is not supported")

        return self.message, self.process_catalog(self.catalog)

    def process_catalog(self, catalog: pystac.Catalog) -> list[pystac.Catalog]:
        """Converts a list of STAC catalogs into a list of lists of STAC catalogs."""
        self.logger.info("process_catalog() started.")
        try:
            # Get all the items from the catalog, including from child or linked catalogs
            items = list(self.get_all_catalog_items(catalog))

            self.logger.info(f"length of items==={len(items)}.")

            # Quick return if catalog contains no items
            if len(items) == 0:
                result = catalog.clone()
                result.id = str(uuid4())
                result.clear_children()
                return result

            # # --- Get granule filepaths (urls) ---
            netcdf_urls: list[str] = _get_netcdf_urls(items)
            self.logger.info(f"netcdf_urls==={netcdf_urls}.")

            # --- Map each granule to an index representing the batch to which it belongs ---
            batch_indices: list[int] = get_batch_indices(netcdf_urls, self.logger)
            sorted(set(batch_indices), key=batch_indices.index)
            self.logger.info(f"batch_indices==={batch_indices}.")

            # --- Construct a dictionary with a separate key for each batch ---
            grouped: dict[int, list[Item]] = {}
            for k, v in zip(batch_indices, items):
                grouped.setdefault(k, []).append(v)

            # --- Construct a list of STAC Catalogs (which represent each TEMPO scan),
            #   and each Catalog holds multiple Items (which represent each granule).
            catalogs = []
            for batch_id, batch_items in grouped.items():
                self.logger.info(f"constructing new pystac.Catalog for batch_id==={batch_id}.")
                # Initialize a new, empty Catalog
                batch_catalog = catalog.clone()
                batch_catalog.id = str(uuid4())
                batch_catalog.clear_children()
                batch_catalog.clear_items()

                for idx, item in enumerate(batch_items):
                    # Construct a new pystac.Item for each granule in the batch
                    output_item = Item(
                        str(uuid4()),
                        bbox_to_geometry(item.bbox),
                        item.bbox,
                        None,
                        _get_output_date_range([item]),
                    )
                    output_item.add_asset(
                        "data",
                        Asset(
                            _get_item_url(item),
                            title=_get_item_url(item),
                            media_type="application/x-netcdf4",
                            roles=["data"],
                        ),
                    )
                    batch_catalog.add_item(output_item)

                self.logger.info("STAC catalog creation for batch_id==={batch_id} complete.")
                catalogs.append(batch_catalog)

            self.logger.info("All STAC catalogs are complete.")

            return catalogs

        except Exception as service_exception:
            self.logger.error(service_exception, exc_info=1)
            raise service_exception
