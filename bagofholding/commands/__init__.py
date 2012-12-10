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
import os
import re
import itertools
import sys
import inspect
import importlib

logger = logging.getLogger(__name__)


class BagOfHoldingCommand(object):
    def __init__(self):
        """Initialize any common properties of BagOfHoldingCommands."""
        pass

    @property
    def name(self):
        """Name of this command

        This should match what will be used on the command line.  The name this
        command is referred to as.

        """

        name = self.__class__.__name__.replace("Command", "").lower()
        logger.debug("probable name: %s", name)
        return name

    @property
    def aliases(self):
        """Aliases this command should respond to."""

        return []

    def add_arguments(self, parser):
        """Add any command line arguments this subcommand needs."""
        pass

    def run(self):
        """Do what this command should actually do."""
        raise NotImplementedError("class {0} does not implement \
            'run(self)'".format(self.__class__.__name__))


# TODO Switch this to an egg hook ...
class BagOfHoldingCommands(object):
    """Dictionary style object for interacting with the commands.

    Provides all commands that can be found in the various locations mapped to
    the specified names.

    """

    def __init__(self):
        self._commands = {}

        mydir = os.path.abspath(os.path.dirname(__file__))
        self.path = [
                mydir,
                re.sub(r"usr/", r"usr/local/", mydir),
                os.path.join(PARAMETERS["main.configuration"], "plugins"),
                ]

        logger.debug("path: %s", self.path)

        for directory in self.path:
            logger.info("searching %s ...", directory)

            if not os.access(directory, os.R_OK):
                continue

            if directory not in sys.path:
                sys.path.insert(0, directory)

            walk = list(os.walk(directory))

            filenames = []
            filenames.extend(itertools.chain(*[[os.path.join(file_[0], name)
                for name in file_[1]] for file_ in walk if len(file_[1])]))
            filenames.extend(itertools.chain(*[[os.path.join(file_[0], name)
                for name in file_[1]] for file_ in walk if len(file_[1])]))
            filenames = list(set([filename.replace(directory + "/", "")
                for filename in filenames]))

            logger.debug("files found: %s", filenames)

            module_names = list(set([re.sub(r"\.py.?", "",
                filename).replace("/", ".") for filename in filenames
                if not re.search(r"(/|^)_", filename)]))

            logger.debug("module names: %s", module_names)

            modules = []

            for module_name in module_names:
                try:
                    modules.append(importlib.import_module(module_name))
                    logger.info("module, %s, imported", module_name)
                except ImportError:
                    logger.warning("module, %s, NOT imported", module_name)
                    continue

            for module in modules:
                for object_ in [class_() for name, class_ in
                    inspect.getmembers(module, inspect.isclass) if
                    issubclass(class_, BagOfHoldingCommand) and
                    class_ != BagOfHoldingCommand]:
                        logger.debug("object, %s, found", object_)
                        self._commands[object_.name] = object_

    def __len__(self):
        return len(self._commands)

    def __getitem__(self, key):
        return self._commands[key]

    def __iter__(self):
        for item in self._commands.iteritems():
            yield item

    def __contains__(self, item):
        return item in self._commands
