#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodecsv
import re
import os
import locale
locale.setlocale(locale.LC_ALL, 'deu_deu' if os.name == 'nt' else 'de_DE.UTF-8')
from operator import itemgetter

file_path = 'parsed.csv'
cleaned = []
header = []
csv_reader = unicodecsv.reader(open(file_path), encoding='utf-8')
for idx, row in enumerate(csv_reader):

    _row = row

    # skip head
    if idx == 0:
        header.append(_row)
        continue

    if _row[1].startswith(('Vorlage:', '-')):
        continue

    if _row in cleaned:
        continue

    # parse cells
    for i in xrange(0, (len(_row) - 1)):
        _row[i] = re.sub(r'<!--.+?-->', '', _row[i])
        _row[i] = re.sub(ur'^—$', '', _row[i])

    cleaned.append(_row)

# sort
result = sorted(cleaned, key=itemgetter(0))

result = header + result

# save
with open('cleaned.csv', "wb") as f:
    for row in result:
        w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
        w.writerow(row)