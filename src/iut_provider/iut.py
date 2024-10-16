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
"""IUT provider data module."""
from copy import deepcopy


class Iut:
    """Item under test (IUT) data object."""

    _iut_dictionary = None

    def __init__(self, **iut):
        """Take a dictionary as input and setattr on instance.

        :param iut: Dictionary to set attributes from.
        :type iut: dict
        """
        self._iut_dictionary = iut
        for key, value in iut.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        """Set IUT parameters to dict and object.

        :param name: Name of parameter to set.
        :type name: str
        :param value: Value of parameter.
        :type value: any
        """
        if self._iut_dictionary is not None:
            self._iut_dictionary[name] = value
        super().__setattr__(name, value)

    def update(self, **dictionary):
        """Update IUT dictionary with new data.

        :param dictionary: Dictionary to update attributes from.
        :type dictionary: dict
        """
        self._iut_dictionary.update(**dictionary)
        for key, value in dictionary.items():
            setattr(self, key, value)

    @property
    def as_dict(self):
        """Represent IUT as dictionary.

        :return: IUT dictionary.
        :rtype: dict
        """
        iut_dictionary = deepcopy(self._iut_dictionary)
        if iut_dictionary.get("identity") and not isinstance(
            iut_dictionary.get("identity"), str
        ):
            iut_dictionary["identity"] = iut_dictionary["identity"].to_string()
        return iut_dictionary

    def __repr__(self):
        """Represent IUT as string.

        :return: IUT identity as a string or Unknown.
        :rtype: str
        """
        try:
            return self._iut_dictionary.get("identity").to_string()
        except:  # noqa pylint:disable=bare-except
            return "Unknown"
