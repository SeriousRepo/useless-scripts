#!/usr/bin/python3

from os import path
from urllib import request
from re import split
from datetime import datetime, timedelta


last_updates_file = path.realpath(__file__)[:-17] + 'last-updates.txt'

content = request.urlopen("https://downloads.oneplus.com/devices/oneplus-5t/").read()

green_color = '\033[92m'
red_color = '\033[91m'
end_color = '\033[0m'
bold_text = '\033[1m'

markers = str(content).split('><')
versions = []
dates = []
for marker in markers:
    if marker.startswith('a role=\"button\"'):
        versions.append(split('[<>]+', marker)[1])
    if marker.startswith('span class=\"time\"'):
        dates.append(split('[<>]+', marker)[1])

is_changed = False
if len(open(last_updates_file).readlines()):
    with open(last_updates_file) as file:
        file_lines = file.read().splitlines()
        print(str(datetime.now()).split('.')[0], end=' | ')
        if file_lines[0].split()[0] == dates[0]:
            print(bold_text + red_color + 'NO UPDATES' + end_color)
        else:
            print(bold_text + green_color + 'AVAILABLE UPDATE' + end_color)
            is_changed = True
        print('---------------------------------------------------')
else:
    is_changed = True

if is_changed:
    open(last_updates_file, 'w').close()
    with open(last_updates_file, 'w') as file:
        extended = []
        for index in range(0, len(versions)):
            extended.append('{} {}'.format(dates[index], versions[index]))
        file.write('\n'.join(extended))

with open(last_updates_file) as file:
    for line in file.readlines():
        if datetime.now() - timedelta(days=50) < datetime.strptime(line.split()[0], '%Y-%m-%d'):
            print(green_color, end='')
        print(line[:-1] + end_color)
