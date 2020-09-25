# Copyright 2020 Axis Communications AB.
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
"""IUT provider prepare module."""
import logging
from copy import deepcopy


class Prepare:  # pylint:disable=too-few-public-methods
    """Prepare and add preparation configuration for ETR to use to item under test (IUT)."""

    logger = logging.getLogger("IUTProvider - Prepare")

    def __init__(self, jsontas, prepare_ruleset):
        """Initialize IUT preparation handler.

        :param jsontas: JSONTas instance used to evaluate the ruleset.
        :type jsontas: :obj:`jsontas.jsontas.JsonTas`
        :param prepare_ruleset: JSONTas ruleset for preparing IUTs.
        :type prepare_ruleset: dict
        """
        self.prepare_ruleset = prepare_ruleset
        self.jsontas = jsontas
        self.dataset = self.jsontas.dataset

    def prepare(self, iuts):
        """Prepare IUTs.

        :param iuts: IUTs to prepare.
        :type iuts: list
        :return: Prepared IUTs.
        :rtype: list
        """
        if not self.prepare_ruleset:
            self.logger.info("No defined preparation rule.")
            return iuts

        for iut in reversed(iuts):
            self.logger.info("Preparing IUT %r", iut)
            self.dataset.add("iut", iut.as_dict)
            response = self.jsontas.run(self.prepare_ruleset)
            if isinstance(response, dict):
                iut.update(**response)
                self.logger.info("Prepared")
            else:
                self.logger.error("Unable to prepare %r Reason %r.", iut, response)
                iuts.remove(iut)
        self.dataset.add("iuts", deepcopy(iuts))
        return iuts
