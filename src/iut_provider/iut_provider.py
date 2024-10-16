# Copyright 2020-2022 Axis Communications AB.
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
"""IUT provider module."""
from abc import abstractmethod
from .utilities.external_provider import ExternalProvider
from .utilities.jsontas_provider import JSONTasProvider


class IutProvider:
    """Item under test (IUT) provider."""

    def __new__(cls, etos, jsontas, ruleset):
        """Check which type of provider and return an appropriate one."""
        if ruleset.get("type", "jsontas") == "external":
            return ExternalProvider(etos, jsontas, ruleset)
        else:
            return JSONTasProvider(etos, jsontas, ruleset)

    @abstractmethod
    def checkin(self, iut):
        """Check in a single IUT, returning it to the IUT provider.

        :param iut: IUT to checkin.
        :type iut: :obj:`environment_provider.iut.iut.Iut`
        """

    @abstractmethod
    def checkin_all(self):
        """Check in all checked out IUTs."""

    @abstractmethod
    def wait_for_and_checkout_iuts(self, minimum_amount, maximum_amount):
        """Wait for and checkout IUTs from an IUT provider.

        :raises: IutNotAvailable: If there are no available IUTs after timeout.

        :param minimum_amount: Minimum amount of IUTs to checkout.
        :type minimum_amount: int
        :param maximum_amount: Maximum amount of IUTs to checkout.
        :type maximum_amount: int
        :return: List of checked out IUTs.
        :rtype: list
        """
