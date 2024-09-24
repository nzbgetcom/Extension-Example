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
import sys
import unittest
import shutil
import os
import subprocess
import pathlib
from os.path import dirname

ROOT_DIR = dirname(__file__)
TEST_DIR = f"{ROOT_DIR}/__"

POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95

def get_python():
    if os.name == "nt":
        return "python"
    return "python3"

def set_defaults():
    os.environ["NZBPO_OPTIONSELECT"] = "One"
    os.environ["NZBPO_OPTIONSTRING"] = "String value"
    os.environ["NZBPO_OPTIONNUMBER"] = "5"
    os.environ["NZBPP_DIRECTORY"] = TEST_DIR
    shutil.rmtree(TEST_DIR, True)
    os.mkdir(TEST_DIR)

def run_script():
    sys.stdout.flush()
    proc = subprocess.Popen(
        [get_python(), ROOT_DIR + "/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )
    out, err = proc.communicate()
    ret_code = proc.returncode
    return (out.decode(), int(ret_code), err.decode())

class Tests(unittest.TestCase):
    def test_status(self):
        set_defaults()
        [_, code, _] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        status_path=f"{TEST_DIR}/_status.txt"
        self.assertTrue(pathlib.Path(status_path).is_file())
        with open(status_path) as status:
            lines = [line.rstrip('\n') for line in status]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[1], "Options: OptionSelect: One, OptionString: String value, OptionNumber: 5")

if __name__ == "__main__":
    unittest.main()
