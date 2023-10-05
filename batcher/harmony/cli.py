"""A Harmony CLI wrapper around the concatenate-batcher"""
import sys
from argparse import ArgumentParser

import harmony

from batcher.harmony.service_adapter import ConcatBatching as HarmonyAdapter


def main(argv, **kwargs):
    """Main Harmony CLI entrypoint

    Parses command line arguments and invokes the appropriate method to respond to them

    Returns
    -------
    None
    """

    config = None
    # Optional: harmony.util.Config is injectable for tests
    if "config" in kwargs:
        config = kwargs.get("config")

    parser = ArgumentParser(
        prog="Pre-concatenate-batching", description="Run the pre-concatenate-batching service"
    )
    harmony.setup_cli(parser)

    args = parser.parse_args(argv[1:])
    if harmony.is_harmony_cli(args):
        harmony.run_cli(parser, args, HarmonyAdapter, cfg=config)
    else:
        parser.error("Only --harmony CLIs are supported")


if __name__ == "__main__":
    main(sys.argv)
