# Copyright (C) 2012 by Alex Brandt <alunduil@alunduil.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

import logging
import copy

logger = logging.getLogger(__name__)


def extract_defaults(parameters):
    """Extract the defaults for the argument dictionaries.

    Creates a dictionary mapping argument name to default value.

    Arguments
    ---------

    :parameters: The list of dictionaries we call parameters

    Examples
    --------

    TODO Add Examples

    """
    return dict([(item["options"][0][2], item["default"])
        for item in parameters if "default" in item])


def extract_options(parameters):
    """Extract the options for add_argument from the argument dictionaries.

    Creates a dictionary of arguments that are legal for add_argument out of
    the argument dictionary in this module.

    Arguments
    ---------

    :parameters: The list of dictionaries we call parameters

    Examples
    --------

    TODO Add Examples

    """

    parameters = copy.deepcopy(parameters)

    return dict([(item["options"][0][2:],
        {"args": item.pop("options"), "kwargs": item}) for item in parameters])
