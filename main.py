#
# Example post-processing script for NZBGet
#
# Copyright (C) 2024 phnzb <pavel@nzbget.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import sys
from datetime import datetime

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95


print("[DETAIL] Script successfully started")
sys.stdout.flush()

# Options passed to script as environment variables
# Check required options
required_options = (
    "NZBPO_OPTIONSELECT",
    "NZBPO_OPTIONSTRING",
    "NZBPO_OPTIONNUMBER"
)
for optname in required_options:
    if optname not in os.environ:
        print(f"[ERROR] Option {optname[6:]} is missing in configuration file. Please check script settings")
        sys.exit(POSTPROCESS_ERROR)

# Check if the script is executed from settings page with a custom command
command = os.environ.get("NZBCP_COMMAND")
test_mode = command == "Test"
if command is not None and not test_mode:
    print("[ERROR] Invalid command " + command)
    sys.exit(POSTPROCESS_ERROR)

OptionSelect = os.environ["NZBPO_OPTIONSELECT"]
OptionString = os.environ["NZBPO_OPTIONSTRING"]
OptionNumber = int(os.environ["NZBPO_OPTIONNUMBER"])

if test_mode:
    print(f"[DETAIL] Script successfully invoked with params: OptionSelect: {OptionSelect}, OptionString: {OptionString}, OptionNumber: {OptionNumber}")
else:
    if not os.path.exists(os.environ["NZBPP_DIRECTORY"]):
        print("Destination directory doesn\'t exist, exiting")
        sys.exit(POSTPROCESS_NONE)
    with open(f"{os.environ['NZBPP_DIRECTORY']}/_status.txt", "w", encoding="utf-8") as status:
        now = datetime.now()
        status.writelines([
            f"Completed at: {now}\n",
            f"Options: OptionSelect: {OptionSelect}, OptionString: {OptionString}, OptionNumber: {OptionNumber}\n"
        ])
        print("[INFO] Example extension successfully completed")

# All OK, returning exit status 'POSTPROCESS_SUCCESS' (int <93>) to let NZBGet know
# that our script has successfully completed.
sys.exit(POSTPROCESS_SUCCESS)
