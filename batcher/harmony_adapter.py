from typing import Optional

from harmony.adapter import BaseHarmonyAdapter
from pystac import Catalog, Item
from pystac.item import Asset

from batcher.tempo_filename_parser import get_unique_day_scan_categories

VALID_EXTENSIONS = (".nc4", ".nc")
VALID_MEDIA_TYPES = ["application/x-netcdf", "application/x-netcdf4"]


def _is_netcdf_asset(asset: Asset) -> bool:
    """Check that a `pystac.Asset` is a valid NetCDF-4 granule. This can be
    ascertained via either the media type or by checking the extension of
    granule itself if that media type is absent.

    """
    return asset.media_type in VALID_MEDIA_TYPES or (
        asset.media_type is None and asset.href.lower().endswith(VALID_EXTENSIONS)
    )


def _get_item_url(item: Item) -> Optional[str]:
    """Check the `pystac.Item` for the first asset with the `data` role and a
    valid input format. If there are no matching assets, return None

    """
    return next(
        (
            asset.href
            for asset in item.assets.values()
            if "data" in (asset.roles or []) and _is_netcdf_asset(asset)
        ),
        None,
    )


def _get_netcdf_urls(items: list[Item]) -> list[str]:
    """Iterate through a list of `pystac.Item` instances, from the input
    `pystac.Catalog`. Extract the `pystac.Asset.href` for the first asset
    of each item that has a role of "data". If there are any items that do
    not have a data asset, then raise an exception.

    """
    catalog_urls = [_get_item_url(item) for item in items]

    if None in catalog_urls:
        raise RuntimeError("Some input granules do not have NetCDF-4 assets.")

    return catalog_urls  # type: ignore[return-value]


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
            raise RuntimeError(
                "Invoking Batcher without a STAC catalog is not supported"
            )

        return self.message, self.process_catalog(self.catalog)

    def process_items_many_to_one(self):
        """Converts a list of STAC catalogs into a list of lists of STAC catalogs."""
        try:
            items: list[Catalog] = list(self.get_all_catalog_items(self.catalog))
            netcdf_urls: list[str] = _get_netcdf_urls(items)

            batch_indices: list[int] = get_unique_day_scan_categories(netcdf_urls)
            unique_category_indices: list[int] = sorted(
                set(batch_indices), key=batch_indices.index
            )

            grouped: dict[int, list[Catalog]] = {}
            for k, v in zip(batch_indices, items):
                grouped.setdefault(k, []).append(v)
            catalogs: list[list[Catalog]] = [
                grouped[k] for k in unique_category_indices
            ]

            return catalogs

        except Exception as service_exception:
            self.logger.error(service_exception, exc_info=1)
            raise service_exception
