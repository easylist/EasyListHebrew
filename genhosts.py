#!/usr/bin/python3
# Generates a hosts file from easylist
from sys import argv

endswith_filters = ['^$third-party', '^$popup,third-party', '^$popup', '^$document', '^$doc', '^$all', '^']
lines = open(argv[1], 'r').read().splitlines()

print("# This lists only contains domains which are used for ads, tracking or popups. it does not block in-HTML elements.")
print("# For use, simply copy paste this into your computers' HOSTS file. See https://en.wikipedia.org/wiki/Hosts_(file)#Location_in_the_file_system")

for line in lines:
	if line.startswith('||'):
		if '/' not in line and ':' not in line:
			for filter in endswith_filters:
				if line.endswith(filter):
					domain = line.replace(filter, '').replace('||', '')
					if '*' not in domain:
						print("0.0.0.0 " + domain)

