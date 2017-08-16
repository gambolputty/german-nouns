#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodecsv
import re

csv_reader = unicodecsv.reader(open('./moprhy/nouns.csv'), encoding='utf-8')
morphy = [x for x in csv_reader]
del morphy[0]
# morphy_singular_words = [x[0] for x in morphy]


csv_reader_wiktionary = unicodecsv.reader(open('./wiktionary/substantive.csv'), encoding='utf-8')
wiktionary = [x for x in csv_reader_wiktionary]
del wiktionary[0]
wiktionary_words = [x[1] for x in wiktionary]

print 'Length morphy: {}'.format(len(morphy))
print 'Length wiktionary: {}'.format(len(wiktionary))
print

result = []
trash = []
found_in_morphy = 0
for row in wiktionary:
    if row[2] != '0':
        # keine Kompositas
        continue
    noun_singular = row[4].lower()
    noun_singular = re.sub(r'\([^\)]+\) ?', '', noun_singular).strip()
    # exclude suffixes
    if noun_singular.startswith('-') and len(noun_singular) > 1:
        continue
    if ' ' in noun_singular:
        continue
    if noun_singular in trash:
        continue
    noun_plural = row[8].lower()
    noun_plural = re.sub(r'\([^\)]+\) ?', '', noun_plural).strip()
    # exclude suffixes
    if noun_plural.startswith('-') and len(noun_plural) > 1:
        continue
    if ' ' in noun_plural:
        continue
    genus = row[3].lower()
    if not genus or genus not in 'mfn':
        continue
    if len(noun_singular) == 0 and len(noun_plural) == 0:
        continue
    result.append([noun_singular, noun_plural, genus])
    trash.append(noun_singular)
    if re.match(r'[\(\)\:]', noun_singular) is not None:
        print 'not allowed: ' + noun_singular

for row in morphy:
    if row[0] not in trash:
        result.append(row)
        trash.append(row)

print 'Length result: {}'.format(len(result))

result.sort(key=lambda x: x[0])
with open('nouns.csv', "w") as f:
    try:
        w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
        for r in result:
            w.writerow(r)
    except Exception as e:
        print 'Error saving file:'
        print e