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
import sys

from bagofholding.parameters import helpers

logger = logging.getLogger(__name__) # pylint: disable=C0103

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "bagofholding")

COMMON_PARAMETERS = [
        { # --loglevel=LEVEL, -l=LEVEL; LEVEL => warning
            "options": [ "--loglevel", "-l" ],
            "default": "warning",
            "metavar": "LEVEL",
            "choices": ["debug", "info", "warning", "error", "critical"],
            "help": \
                    "The logging level (corresponds to the levels in the " \
                    "python logging module).  LEVEL defaults to warning.",
            },
        { # --noop
            "options": [ "--noop" ],
            "action": "store_true",
            "default": False,
            "help": \
                    "Show what actions would occur but don't apply any " \
                    "changes.  Works like a dry run mode and forces info " \
                    "level logging.  Overrides --force if it is specified.",
            },
        { # --configuration=DIR, -f=DIR; DIR => ~/.config/bagofholding
            "options": [ "--configuration", "-f" ],
            "default": CONFIG_DIR,
            "metavar": "DIR",
            "help": \
                    "The configuration directory to use for various " \
                    "settings.  DIR defaults to ~/.config/bagofholding",
            },
        ]

DEFAULTS = {}
DEFAULTS.update(helpers.extract_defaults(COMMON_PARAMETERS))

logger.debug("DEFAULTS: %s", DEFAULTS)

class BagOfHoldingParameters(object): # pylint: disable=R0903,R0924
    def __init__(self, *args, **kwargs):
        """Initialize the collapsed parameters for Singularity.

        ### Arguments

        Argument | Description
        -------- | -----------
        args     | The arguments to pass to the internal ArgumentParser.
        kwargs   | The arguments to pass to the internal ArgumentParser.

        ### Description

        Reads the parameters from the command line and configuration file and
        presents them as attributes of this class.  Will resolve parameters in
        the following order:

        1. Arguments on the command line
        2. Arguments specified in a configuration file
        3. Argument defaults

        """

        if "_arguments" not in self.__dict__:
            from singularity.parameters.arguments import SingularityArguments
            self._arguments = SingularityArguments(*args, **kwargs)

    def __getitem__(self, key):
        """Retrieve item at key from "dict"

        TODO Clean up this code and make it more readable.

        """

        short = key

        logger.debug("getting key: %s", key)

        if key.count(".") > 0:
            section, short = key.split(".", 1) # pylint: disable=W0612

        default = "" 
        if short in DEFAULTS:
            default = DEFAULTS[short]
        logger.debug("default: %s", default)

        argument = ""
        if key in self._arguments:
            argument = self._arguments[key]
        logger.debug("argument: %s", argument)

        # TODO Collapse dictionaries into one reference.
        # TODO Check for string length seems unnecessary.
        if len(str(default)) and str(default) in sys.argv[0] or argument != default: # pylint: disable=C0301
            logger.debug("Selected value: %s", argument)
            return argument

        logger.debug("Selected value: %s", default or None) 
        return default or None

PARAMETERS = BagOfHoldingParameters()

