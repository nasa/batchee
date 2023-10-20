from uuid import uuid4

import pystac
from harmony.adapter import BaseHarmonyAdapter
from harmony.util import bbox_to_geometry
from pystac import Item
from pystac.item import Asset

from batcher.harmony.util import (
    _get_netcdf_urls,
    _get_output_bounding_box,
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

    def process_catalog(self, catalog: pystac.Catalog):
        """Converts a list of STAC catalogs into a list of lists of STAC catalogs."""
        try:
            result = catalog.clone()
            result.id = str(uuid4())
            result.clear_children()

            # Get all the items from the catalog, including from child or linked catalogs
            items = list(self.get_all_catalog_items(catalog))

            # Quick return if catalog contains no items
            if len(items) == 0:
                return result

            # # --- Get granule filepaths (urls) ---
            netcdf_urls: list[str] = _get_netcdf_urls(items)

            # --- Map each granule to an index representing the batch to which it belongs ---
            batch_indices: list[int] = get_batch_indices(netcdf_urls)
            sorted(set(batch_indices), key=batch_indices.index)

            # --- Construct a dictionary with a separate key for each batch ---
            grouped: dict[int, list[Item]] = {}
            for k, v in zip(batch_indices, items):
                grouped.setdefault(k, []).append(v)

            # --- Construct a STAC Catalog that holds multiple Items (which represent each TEMPO scan),
            #   and each Item holds multiple Assets (which represent each granule).
            result.clear_items()

            for batch_id, batch_items in grouped.items():
                batch_urls: list[str] = _get_netcdf_urls(batch_items)
                bounding_box = _get_output_bounding_box(batch_items)
                properties = _get_output_date_range(batch_items)

                # Construct a new pystac.Item with every granule in the batch as a pystac.Asset
                output_item = Item(
                    str(uuid4()), bbox_to_geometry(bounding_box), bounding_box, None, properties
                )

                for idx, item in enumerate(batch_items):
                    output_item.add_asset(
                        "data",
                        Asset(
                            batch_urls[idx],
                            title=batch_urls[idx],
                            media_type="application/x-netcdf4",
                            roles=["data"],
                        ),
                    )

                result.add_item(output_item)

            return result

        except Exception as service_exception:
            self.logger.error(service_exception, exc_info=1)
            raise service_exception