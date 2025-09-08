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
"""A Harmony CLI wrapper around batchee"""

from argparse import ArgumentParser

import harmony_service_lib

from batchee.harmony.service_adapter import ConcatBatching as HarmonyAdapter


def main(config: harmony_service_lib.util.Config = None) -> None:
    """Parse command line arguments and invoke the service to respond to them.

    Parameters
    ----------
    config : harmony.util.Config
        harmony.util.Config is injectable for tests

    Returns
    -------
    None
    """
    parser = ArgumentParser(
        prog="Pre-concatenate-batching",
        description="Run the pre-concatenate-batching service",
    )
    harmony_service_lib.setup_cli(parser)
    args = parser.parse_args()
    if harmony_service_lib.is_harmony_cli(args):
        harmony_service_lib.run_cli(parser, args, HarmonyAdapter, cfg=config)
    else:
        parser.error("Only --harmony CLIs are supported")


if __name__ == "__main__":
    main()
