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
"""Log area provider utilizing JSONTas."""
import logging
import time
from .list import List
from .checkout import Checkout
from .checkin import Checkin
from ..exceptions import (
    NoLogAreaFound,
    LogAreaNotAvailable,
    LogAreaCheckoutFailed,
    NotEnoughLogAreasAvailable,
)


class JSONTasProvider:
    """Log area provider using JSONTas."""

    logger = logging.getLogger("LogAreaProvider")

    def __init__(self, etos, jsontas, ruleset):
        """Initialize log area provider.

        :param etos: ETOS library instance.
        :type etos: :obj:`etos_lib.etos.Etos`
        :param jsontas: JSONTas instance used to evaluate the rulesets.
        :type jsontas: :obj:`jsontas.jsontas.JsonTas`
        :param ruleset: JSONTas ruleset for handling log areas.
        :type ruleset: dict
        """
        self.etos = etos
        self.jsontas = jsontas
        self.etos.config.set("logs", [])
        self.ruleset = ruleset
        self.id = self.ruleset.get("id")  # pylint:disable=invalid-name
        self.logger.info("Initialized log area provider %r", self.id)

    def checkout(self, available_log_areas):
        """Checkout a number of log areas from an log area provider.

        :param available_log_areas: Log areas to checkout.
        :type available_log_areas: list
        :return: Checked out log areas.
        :rtype: list
        """
        checkout_log_areas = Checkout(self.jsontas, self.ruleset.get("checkout"))
        return checkout_log_areas.checkout(available_log_areas)

    def list(self, amount):
        """List log areas in order to find out which are available or not.

        :param amount: Number of log areas to list.
        :type amount: int
        :return: Available log areas in the log area provider.
        :rtype: list
        """
        list_log_areas = List(self.id, self.jsontas, self.ruleset.get("list"))
        return list_log_areas.list(amount)

    def checkin_all(self):
        """Check in all checked out log areas."""
        checkin_log_areas = Checkin(self.jsontas, self.ruleset.get("checkin"))
        checkin_log_areas.checkin_all()

    def checkin(self, log_area):
        """Check in a single log area, returning it to the log area provider.

        :param log_area: Log area to checkin.
        :type log_area: :obj:`environment_provider.logs.log_area.LogArea`
        """
        checkin_log_areas = Checkin(self.jsontas, self.ruleset.get("checkin"))
        checkin_log_areas.checkin(log_area)

    def wait_for_and_checkout_log_areas(self, minimum_amount=0, maximum_amount=100):
        """Wait for and checkout log areas from an log area provider.

        :raises: LogAreaNotAvailable: If there are no available log areas after timeout.

        :param minimum_amount: Minimum amount of log areas to checkout.
        :type minimum_amount: int
        :param maximum_amount: Maximum amount of log areas to checkout.
        :type maximum_amount: int
        :return: List of checked out log areas.
        :rtype: list
        """
        timeout = time.time() + self.etos.config.get("WAIT_FOR_LOG_AREA_TIMEOUT")
        first_iteration = True
        while time.time() < timeout:
            if first_iteration:
                first_iteration = False
            else:
                time.sleep(5)
            try:
                available_log_areas = self.list(maximum_amount)
                self.logger.info("Available log areas:")
                for log_area in available_log_areas:
                    self.logger.info(log_area)
                if len(available_log_areas) < minimum_amount:
                    self.logger.critical(
                        "Not enough available log areas in log area provider!"
                    )
                    raise NotEnoughLogAreasAvailable(self.id)

                checked_out_log_areas = self.checkout(available_log_areas)
                self.logger.info("Checked out log areas:")
                for log_area in checked_out_log_areas:
                    self.logger.info(log_area)
                if len(checked_out_log_areas) < minimum_amount:
                    raise LogAreaNotAvailable(self.id)
                break
            except NoLogAreaFound:
                self.logger.critical("Log area does not exist in log area provider!")
                checked_out_log_areas = []
                break
            except LogAreaNotAvailable:
                self.logger.warning("Log area not available yet.")
                continue
            except LogAreaCheckoutFailed as checkout_failed:
                self.logger.critical(
                    "Checkout of log area failed with reason %r!", checkout_failed
                )
                self.checkin_all()
                checked_out_log_areas = []
                break
        else:
            self.logger.error(
                "Log area did not become available in %rs",
                self.etos.config.get("WAIT_FOR_LOG_AREA_TIMEOUT"),
            )
            checked_out_log_areas = []
        if len(checked_out_log_areas) < minimum_amount:
            raise LogAreaNotAvailable(self.id)
        return checked_out_log_areas
