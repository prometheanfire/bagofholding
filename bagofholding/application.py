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

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from bagofholding import information
from bagofholding.parameters import PARAMETERS
from bagofholding.commands import COMMANDS


class BagOfHoldingApplication(object):
    def __init__(self):
        epilog = \
                "Copyright (C) (i.COPY_YEAR} by {i.AUTHOR} Licensed under a " \
                "{i.LICENSE} License"

        BagOfHoldingParameters(
                description=information.DESCRIPTION,
                epilog=epilog.format(i=information))

        logging.getLogger().setLevel(
                getattr(logging, PARAMETERS["main.loglevel"].upper()))

    def run(self):
        """Run the requested subcommand."""

        logger.debug("running %s", PARAMETERS["subcommand"])

        COMMANDS[PARAMETERS["subcommand"]].run()
