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
import argparse

from bagofholding import information
from bagofholding.parameters import helpers
from bagofholding.commands import COMMANDS

logger = logging.getLogger(__name__) # pylint: disable=C0103

class BagOfHoldingArguments(object): # pylint: disable=R0924,R0903
    def __init__(self, parse = True, *args, **kwargs):
        """Initialize the BagOfHolding argument parser.

        Reads the parameters from the command line and presenets them as
        attributes of this class.

        Arguments
        ---------

        :args: The arguments to pass to the internal ArgumentParser
        :kwargs: The arguments to pass to the internal ARgumentParser

        """

        self._parser = argparse.ArgumentParser(*args, **kwargs)
        
        version = \
                "%(prog)s-{i.VERSION}\n" \
                "\n" \
                "Copyright {i.COPY_YEAR} by {i.AUTHOR} <{i.AUTHOR_EMAIL}> " \
                "and contributors.  This is free software; see the source " \
                "for copying conditions.  There is NO warranty; not even " \
                "for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

        self._parser.add_argument("--version",
                action = "version",
                version = version.format(i = information))

        from bagofholding.parameters import COMMON_PARAMETERS

        common = argparse.ArgumentParser(add_help = False)
        for name, options in helpers.extract_options(COMMON_PARAMETERS).iteritems(): # pylint: disable=C0301
            logger.debug("adding option, %s, with args -> (%s) and kwargs -> (%s)", name, options["args"], options["kwargs"]) # pylint: disable=C0301
            common.add_argument(*options["args"], **options["kwargs"]) # pylint: disable=W0142,C0301

        subparsers = self._parser.add_subparsers(
                title = "Available subcommands:",
                dest = "subcommand")

        self.parsers = {}

        for name, command in COMMANDS:
            self.parsers[command.name] = subparsers.add_parser(
                    command.name,
                    aliases = command.aliases,
                    parents = [common])
            command.add_arguments(self.parsers[command.name])

        if parse:
            self.parsed_arguments = self._parser.parse_args()

        self.parsers["main"] = self._parser

    def __getitem__(self, key):
        if key.count("."):
            section, key = key.split(".", 1) # pylint: disable=W0612
        return getattr(self.parsed_arguments, key)

    def __contains__(self, key):
        if key.count("."):
            section, key = key.split(".", 1) # pylint: disable=W0612
        return hasattr(self.parsed_arguments, key)

