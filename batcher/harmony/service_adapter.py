from uuid import uuid4

import pystac
from harmony.adapter import BaseHarmonyAdapter
from harmony.util import bbox_to_geometry
from pystac import Item
from pystac.item import Asset

from batcher.harmony.util import (
    _get_item_url,
    _get_netcdf_urls,
    _get_output_date_range,
)
from batcher.tempo_filename_parser import get_batch_indices


class ConcatBatching(BaseHarmonyAdapter):
    """
    A harmony-service-lib wrapper around the concatenate-batcher module.
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
                        f"data_{idx}",
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
