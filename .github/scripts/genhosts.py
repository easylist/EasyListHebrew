#!/usr/bin/python3
# Generates a hosts file from adblock file
from sys import argv
import io

endswith_filters = [
    "^$third-party",
    "^$popup,third-party",
    "^$popup",
    "^$document",
    "^$doc",
    "^$all",
    "##*",
    "^",
]

hosts = "hosts.txt"
ad_guard_hosts = "adguard_hosts.txt"

domains = set()

with open(argv[1], "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if (
            line.startswith("||") and "/" not in line and ":" not in line
        ) or line.endswith("##*"):
            for filter in endswith_filters:
                if line.endswith(filter) and "*" not in line[:-1]:
                    domain = line.replace(filter, "").replace("||", "")
                    domains.add(domain)

domains = list(domains)
domains.sort()

with io.open(hosts, "w", newline="\n", encoding="utf-8") as ho, io.open(
    ad_guard_hosts, "w", newline="\n", encoding="utf-8"
) as agho:
    for f in (ho, agho):
        f.write(
            "# This lists only contains domains which are used for ads, tracking or popups. it does not block in-HTML elements.\n"
        )
        f.write(
            "# For use, simply copy paste this into your computers' HOSTS file. See https://en.wikipedia.org/wiki/Hosts_(file)#Location_in_the_file_system\n"
        )
    for domain in domains:
        ho.write("0.0.0.0 " + domain + "\n")
        agho.write(domain + "\n")
