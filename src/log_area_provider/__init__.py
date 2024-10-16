# Copyright 2022 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""ETOS log area provider module."""
import pathlib
from .log_area_provider import LogAreaProvider

__all__ = ["LogAreaProvider", "log_area_provider_schema"]

LOG_AREA_PROVIDER_SCHEMA = (
    pathlib.Path(__file__).parent.resolve().joinpath("./schemas/jsontas_schema.json")
)
EXTERNAL_LOG_AREA_PROVIDER_SCHEMA = (
    pathlib.Path(__file__).parent.resolve().joinpath("./schemas/external_schema.json")
)


def log_area_provider_schema(ruleset):
    """Get log area provider schema for json validation.

    :param ruleset: Ruleset to get a log area provider schema for.
    :type ruleset: dict
    """
    if ruleset.get("log", {}).get("type", "jsontas") == "external":
        return EXTERNAL_LOG_AREA_PROVIDER_SCHEMA
    else:
        return LOG_AREA_PROVIDER_SCHEMA
