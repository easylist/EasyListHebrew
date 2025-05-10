#!/usr/bin/env python3
# coding: utf-8

# This file is part of Adblock Plus <http://adblockplus.org/>,
# Copyright (C) 2006-2013 Eyeo GmbH
#
# Adblock Plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Adblock Plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adblock Plus.  If not, see <http://www.gnu.org/licenses/>.

#############################################################################
# This is a reference script to add checksums to downloadable               #
# subscriptions. The checksum will be validated by Adblock Plus on download #
# and checksum mismatches (broken downloads) will be rejected.              #
#                                                                           #
# To add a checksum to a subscription file, run the script like this:       #
#                                                                           #
#   python addChecksum.py < subscription.txt > subscriptionSigned.txt       #
#                                                                           #
# Note: your subscription file should be saved in UTF-8 encoding, otherwise #
# the operation will fail.                                                  #
#############################################################################

import io
import sys
import re
import hashlib
import base64
import datetime

checksumRegexp = re.compile(r"^\s*!\s*checksum[\s\-:]+([\w\+\/=]+).*\n", re.I | re.M)
dateRegexp = re.compile(r"^\s*!\s*Last modified[\s\-:]+([\w\+\/=]+).*\n", re.I | re.M)
OPTIONPATTERN = re.compile(r"^(?P<domain>.*)\$(?P<options>~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")

def addChecksum(data):
    # Update the last modified date
    data = re.sub(
        dateRegexp,
        "! Last modified: %s"
        % datetime.datetime.now(datetime.UTC).strftime("%d %b %Y %H:%M UTC\n"),
        data,
    )
    checksum = calculateChecksum(data)
    # Remove existing checksums
    data = re.sub(checksumRegexp, "", data)
    # Add the new checksum
    data = re.sub(r"(\r?\n)", r"\1! Checksum: %s\1" % checksum, data, count=1)
    return data


def calculateChecksum(data):
    md5 = hashlib.md5()
    # Normalize the data for checksum calculation
    md5.update(normalize(data).encode("utf-8"))
    return base64.b64encode(md5.digest()).rstrip(b"=").decode()


def normalize(data):
    # Split the data into lines
    lines = data.splitlines()

    # Filter out lines containing the checksum
    filtered_lines = [
        line for line in lines if not re.match(r"^\s*!?\s*checksum\s*:", line, re.I)
    ]

    # Join remaining lines for checksum calculation
    return "\n".join(filtered_lines)


# Coded by EasyList Hebrew Team
# Licence: https://easylist.to/pages/licence.html


def sort_file(data):
    lines = data.split("\n") + ["\n"]
    res = ""
    lst = []
    for line in lines:
        line = line.strip()
        if (
            line.startswith("!")
            or line == ""
            or line.startswith("# ")
            or line == "#"
            or (line.startswith("[") and line.endswith("]"))
        ):
            if lst:
                lst.sort()
                res += "".join(lst)
                lst = []
            res += line + "\n"
        else:
            isRegex = False
            isHidingRule = False
            if line:
                if (line.startswith("/") and len(line) > 1) or (
                    line.startswith("@@/") and len(line) > 3
                ):
                    if line.endswith("/"):
                        isRegex = True
                    elif (
                        line.rfind("$") == (line.rfind("/$") + 1)
                        and line.rfind("/") == line.rfind("/$")
                        and line.rfind("/") > line.find("/")
                    ):
                        isRegex = True
                if "##" in line or "#@#" in line:
                    if not isRegex:
                        isHidingRule = True
                        sep = line.index("#")
                        url = (line[:sep], line[sep:])
                        spl = url[0].split(",")
                        if len(spl) > 1:
                            spl = sorted(spl)
                        domain = ",".join(spl)
                        line = domain + url[1]
                if not isHidingRule:
                    if OPTIONPATTERN.match(line):
                        url_name = OPTIONPATTERN.match(line).group("domain")
                        options = OPTIONPATTERN.match(line).group("options")
                        # sort domains in domain
                        options = ','.join(sorted(options.split(",")))
                        options = ','.join(sorted(options.split(","), key=lambda x: x.startswith("~")))
                        options = sorted(options.split(","), key=lambda x: x.startswith("domain="))
                        if options[-1].startswith("domain="):
                            sorted_domains = sorted(options[-1].split("=")[1].split("|"))
                            options[-1] = "domain=" + "|".join(sorted_domains)
                        line = url_name + "$" + ",".join(options)
                lst.append(line + "\n")
    return res.rstrip()


if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = f.read()
        data = addChecksum(sort_file(data))
    with io.open(sys.argv[2], "w", newline="\n", encoding="utf-8") as f:
        f.write(data)
