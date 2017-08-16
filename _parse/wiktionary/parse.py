#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import os
import unicodecsv
import re
from pprint import pprint
from progressbar import ProgressBar, FormatLabel, Percentage, Bar, ETA, AnimatedMarker, SimpleProgress, UnknownLength, Timer
import mwparserfromhell

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def parse_page(text):
    result = {}
    for template in mwparserfromhell.parse(text).filter_templates():
        if template.name.matches(u'Deutsch Substantiv Übersicht'):
                for param in template.params:
                    m = re.match(ur'^([^=]+)=(.+)', unicode(param))
                    if m is None:
                        continue
                    key = m.group(1).strip().title()
                    value = m.group(2)
                    value = value.replace('[[', '')
                    value = value.replace(']]', '')
                    result[key] = value
    return result

def is_kompositum(text):
    if 'kompositum' in text.lower():
        clean = re.sub(r'[^a-zA-Z\d\s]', '', text).lower()
        # test:
        # s = s[ beginning : beginning + LENGTH]
        # idx = clean.index('kompositum')
        # print clean[idx:idx+80].replace('\n', '')
        if re.search(r'kompositum +(aus|von|der substantive|bestehend aus|zusammensetzung|zusammengesetzt|zusammengezogen)', clean, re.I | re.U) is not None:
            return True

    return False


"""
Create new csv file with header
"""
csv_path = 'substantive.csv'
storage = []
all_titles = []
if not os.path.isfile(csv_path):
    # save header
    with open(csv_path, "wb") as f:
        w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
        header = [
            'Id',
            'Titel',
            'Kompositum',
            'Genus',
            'Nominativ Singular',
            'Genitiv Singular',
            'Dativ Singular',
            'Akkusativ Singular',
            'Nominativ Plural',
            'Genitiv Plural',
            'Dativ Plural',
            'Akkusativ Plural',
        ]
        w.writerow(header)


"""
Progressbar
"""
widgets = [SimpleProgress(), ' ', AnimatedMarker(), '', ' [', Timer(), '] ']
bar = ProgressBar(widgets=widgets, max_value=UnknownLength)
bar.update(0)
widgets[3] = FormatLabel(' 0 saved ')

"""
XML dump
"""
total_count = 0
process_count = 0
path_wiki_xml = 'dewiktionary-20170501-pages-articles.xml'
# save memory by saveing first element reference in a variable: http://effbot.org/zone/element-iterparse.htm

# get an iterable
context = etree.iterparse(path_wiki_xml, events=("start", "end"))

# turn it into an iterator
context = iter(context)

# get the root element
event, root = context.next()

for event, elem in context:
    process_count += 1
    if process_count > 1 and (process_count % 50000) == 0:
        bar.update(process_count)
    # if process_count <= 22000000:
    #   root.clear()
    #   continue

    tname = strip_tag_name(elem.tag)

    if event == 'start':

        if tname == 'page':
            id = -1
            title = ''
            text = ''
            inrevision = False
            redirect = False
        elif tname == 'revision':
            # Do not pick up on revision id's
            inrevision = True

    else:

        # no redirect pages
        if tname == 'redirect':
            redirect = True
        elif tname == 'title':
            title = elem.text
            # if title in all_titles:
            #   root.clear()
            #   continue
        elif tname == 'text':
            text = elem.text
        elif tname == 'id' and not inrevision:
            id = int(elem.text)
        elif tname == 'page':

            if redirect is True or title.lower().startswith(('wiktionary', 'mediawiki')):
                root.clear()
                continue

            parsed = parse_page(text)

            if len(parsed.keys()) == 0:
                root.clear()
                continue

            """
            create row
            """
            parsed_clean_keys = {}
            for _key, value in parsed.items():
                clean_key = re.sub(r' ?\d+$', '', _key)
                if clean_key in parsed_clean_keys.keys():
                    continue
                parsed_clean_keys[clean_key] = value
            row = [
                id,
                title,
                1 if is_kompositum(text) is True else 0,
                parsed_clean_keys['Genus'] if 'Genus' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Nominativ Singular'] if 'Nominativ Singular' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Genitiv Singular'] if 'Genitiv Singular' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Dativ Singular'] if 'Dativ Singular' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Akkusativ Singular'] if 'Akkusativ Singular' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Nominativ Plural'] if 'Nominativ Plural' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Genitiv Plural'] if 'Genitiv Plural' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Dativ Plural'] if 'Dativ Plural' in parsed_clean_keys.keys() else '',
                parsed_clean_keys['Akkusativ Plural'] if 'Akkusativ Plural' in parsed_clean_keys.keys() else '',
            ]

            storage.append(row)

            total_count += 1
            if total_count > 1 and (total_count % 1000) == 0:
                with open(csv_path, "ab") as f:
                    try:
                        w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
                        for r in storage:
                            w.writerow(r)
                        storage = []
                    except Exception as e:
                        'Error saving "{}"'.format(csv_path)
                        import sys
                        sys.exit()

                widgets[3] = FormatLabel(' {0} saved '.format(total_count))

        root.clear()

if len(storage) > 0:
    with open(csv_path, "ab") as f:
        try:
            w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
            for r in storage:
                w.writerow(r)
        except Exception as e:
            'Error saving "{}"'.format(csv_path)
            import sys
            sys.exit()

    widgets[3] = FormatLabel(' {0} saved '.format(total_count))