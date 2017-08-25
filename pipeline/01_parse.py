#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import os
import unicodecsv
import re
from pprint import pprint
from progressbar import ProgressBar, FormatLabel, Percentage, Bar, ETA, AnimatedMarker, SimpleProgress, UnknownLength, Timer
import mwparserfromhell
from bz2file import BZ2File

"""
Siehe Vorlage Flexionstabelle:
https://de.wiktionary.org/wiki/Hilfe:Flexionstabellen
"""

def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def parse_page(text):
    if not text:
        return []

    # 1 Wort kann mehrere Bedeutungen (und Grammatiken haben)
    parsed_items = []
    split = re.split(r'(=== ?\{\{Wortart.+)\n', text)
    word_found = False
    for chunk in split:
        if re.match(r'^=== ?\{\{Wortart', chunk) is not None:
            word_found = True
            found_word = {
                'Wortart': [],
                'Kompositum': '',
            }
            # wortart
            for template in mwparserfromhell.parse(chunk).filter_templates():
                if template.name == 'Wortart':
                    found_word['Wortart'].extend([unicode(x) for x in template.params if x != 'Deutsch'])

            continue

        if word_found is True:

            # Grammatik
            for template in mwparserfromhell.parse(chunk).filter_templates():
                if template.name.matches(u'Deutsch Substantiv Übersicht') \
                        or template.name.matches(u'Deutsch adjektivisch Übersicht'):
                    for param in template.params:
                        m = re.match(ur'^([^=]+)=(.+)', unicode(param))
                        if m is None:
                            continue
                        key = m.group(1).strip().title()
                        # key = re.sub(r' ?\d+$', '', key)
                        value = m.group(2)
                        value = value.replace('[[', '')
                        value = value.replace(']]', '')
                        found_word[key] = value

            # kompositum?
            sect_herkunft = re.search(r'(?:\{\{Herkunft\}\})((?:\n.+)+)', chunk)
            if sect_herkunft is not None:
                clean = re.sub(r'[^\w\s]', '', sect_herkunft.group(1))
                if re.search(r'kompositum +(aus|von|der substantive|bestehend aus|zusammensetzung|zusammengesetzt|zusammengezogen)', clean, re.I) is not None:
                    found_word['Kompositum'] = 1

            # append
            parsed_items.append(found_word)

    result = []
    for w in parsed_items:
        if len(w.keys()) <= 2 and 'Kompositum' in w.keys() and 'Wortart' in w.keys():
            continue
        if 'Substantiv' not in w['Wortart']:
            continue

        new_item = w
        distinct = list(set(new_item['Wortart']))
        new_item['Wortart'] = u','.join(distinct)
        result.append(new_item)
        
    return result


"""
Create new csv file with header
"""
csv_path = 'parsed.csv'
storage = []
all_titles = []
if not os.path.isfile(csv_path):
    # save header
    with open(csv_path, "wb") as f:
        w = unicodecsv.writer(f, delimiter=',', encoding='utf-8')
        header = [
            # 'Id',
            'Titel',
            'Wortart',
            'Kompositum',
            'Genus',

            'Nominativ Singular',
            'Nominativ Singular*',
            'Nominativ Singular 1',
            'Nominativ Singular 2',
            'Nominativ Singular 3',
            'Nominativ Singular 4',
            'Nominativ Singular stark',
            'Nominativ Singular schwach',
            'Nominativ Singular gemischt',
            'Nominativ Plural',
            'Nominativ Plural*',
            'Nominativ Plural 1',
            'Nominativ Plural 2',
            'Nominativ Plural 3',
            'Nominativ Plural 4',
            'Nominativ Plural stark',
            'Nominativ Plural schwach',
            'Nominativ Plural gemischt',

            'Genitiv Singular',
            'Genitiv Singular*',
            'Genitiv Singular 1',
            'Genitiv Singular 2',
            'Genitiv Singular 3',
            'Genitiv Singular 4',
            'Genitiv Singular stark',
            'Genitiv Singular schwach',
            'Genitiv Singular gemischt',
            'Genitiv Plural',
            'Genitiv Plural*',
            'Genitiv Plural 1',
            'Genitiv Plural 2',
            'Genitiv Plural 3',
            'Genitiv Plural 4',
            'Genitiv Plural stark',
            'Genitiv Plural schwach',
            'Genitiv Plural gemischt',

            'Dativ Singular',
            'Dativ Singular*',
            'Dativ Singular 1',
            'Dativ Singular 2',
            'Dativ Singular 3',
            'Dativ Singular 4',
            'Dativ Singular stark',
            'Dativ Singular schwach',
            'Dativ Singular gemischt',
            'Dativ Plural',
            'Dativ Plural*',
            'Dativ Plural 1',
            'Dativ Plural 2',
            'Dativ Plural 3',
            'Dativ Plural 4',
            'Dativ Plural stark',
            'Dativ Plural schwach',
            'Dativ Plural gemischt',

            'Akkusativ Singular',
            'Akkusativ Singular*',
            'Akkusativ Singular 1',
            'Akkusativ Singular 2',
            'Akkusativ Singular 3',
            'Akkusativ Singular 4',
            'Akkusativ Singular stark',
            'Akkusativ Singular schwach',
            'Akkusativ Singular gemischt',
            'Akkusativ Plural',
            'Akkusativ Plural*',
            'Akkusativ Plural 1',
            'Akkusativ Plural 2',
            'Akkusativ Plural 3',
            'Akkusativ Plural 4',
            'Akkusativ Plural stark',
            'Akkusativ Plural schwach',
            'Akkusativ Plural gemischt',
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
bzfile_path = '/Users/gregor/Downloads/dewiktionary-20170820-pages-articles-multistream.xml.bz2'
# save memory by saveing first element reference in a variable: http://effbot.org/zone/element-iterparse.htm

# get an iterable
bz = BZ2File(bzfile_path)
context = etree.iterparse(bz, events=("start", "end"))

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

            if len(parsed) == 0:
                root.clear()
                continue

            """
            loop found words
            create row
            """
            for word in parsed:

                row = [
                    # id,
                    title,
                    word['Wortart'] if 'Wortart' in word.keys() else '',
                    word['Kompositum'],
                    word['Genus'] if 'Genus' in word.keys() and word['Genus'] in 'fmn' else '',

                    word['Nominativ Singular'] if 'Nominativ Singular' in word.keys() else '',
                    word['Nominativ Singular*'] if 'Nominativ Singular*' in word.keys() else '',
                    word['Nominativ Singular 1'] if 'Nominativ Singular 1' in word.keys() else '',
                    word['Nominativ Singular 2'] if 'Nominativ Singular 2' in word.keys() else '',
                    word['Nominativ Singular 3'] if 'Nominativ Singular 3' in word.keys() else '',
                    word['Nominativ Singular 4'] if 'Nominativ Singular 4' in word.keys() else '',
                    word['Nominativ Singular stark'] if 'Nominativ Singular stark' in word.keys() else '',
                    word['Nominativ Singular schwach'] if 'Nominativ Singular schwach' in word.keys() else '',
                    word['Nominativ Singular gemischt'] if 'Nominativ Singular gemischt' in word.keys() else '',
                    word['Nominativ Plural'] if 'Nominativ Plural' in word.keys() else '',
                    word['Nominativ Plural*'] if 'Nominativ Plural*' in word.keys() else '',
                    word['Nominativ Plural 1'] if 'Nominativ Plural 1' in word.keys() else '',
                    word['Nominativ Plural 2'] if 'Nominativ Plural 2' in word.keys() else '',
                    word['Nominativ Plural 3'] if 'Nominativ Plural 3' in word.keys() else '',
                    word['Nominativ Plural 4'] if 'Nominativ Plural 4' in word.keys() else '',
                    word['Nominativ Plural stark'] if 'Nominativ Plural stark' in word.keys() else '',
                    word['Nominativ Plural schwach'] if 'Nominativ Plural schwach' in word.keys() else '',
                    word['Nominativ Plural gemischt'] if 'Nominativ Plural gemischt' in word.keys() else '',

                    word['Genitiv Singular'] if 'Genitiv Singular' in word.keys() else '',
                    word['Genitiv Singular*'] if 'Genitiv Singular*' in word.keys() else '',
                    word['Genitiv Singular 1'] if 'Genitiv Singular 1' in word.keys() else '',
                    word['Genitiv Singular 2'] if 'Genitiv Singular 2' in word.keys() else '',
                    word['Genitiv Singular 3'] if 'Genitiv Singular 3' in word.keys() else '',
                    word['Genitiv Singular 4'] if 'Genitiv Singular 4' in word.keys() else '',
                    word['Genitiv Singular stark'] if 'Genitiv Singular stark' in word.keys() else '',
                    word['Genitiv Singular schwach'] if 'Genitiv Singular schwach' in word.keys() else '',
                    word['Genitiv Singular gemischt'] if 'Genitiv Singular gemischt' in word.keys() else '',
                    word['Genitiv Plural'] if 'Genitiv Plural' in word.keys() else '',
                    word['Genitiv Plural*'] if 'Genitiv Plural*' in word.keys() else '',
                    word['Genitiv Plural 1'] if 'Genitiv Plural 1' in word.keys() else '',
                    word['Genitiv Plural 2'] if 'Genitiv Plural 2' in word.keys() else '',
                    word['Genitiv Plural 3'] if 'Genitiv Plural 3' in word.keys() else '',
                    word['Genitiv Plural 4'] if 'Genitiv Plural 4' in word.keys() else '',
                    word['Genitiv Plural stark'] if 'Genitiv Plural stark' in word.keys() else '',
                    word['Genitiv Plural schwach'] if 'Genitiv Plural schwach' in word.keys() else '',
                    word['Genitiv Plural gemischt'] if 'Genitiv Plural gemischt' in word.keys() else '',

                    word['Dativ Singular'] if 'Dativ Singular' in word.keys() else '',
                    word['Dativ Singular*'] if 'Dativ Singular*' in word.keys() else '',
                    word['Dativ Singular 1'] if 'Dativ Singular 1' in word.keys() else '',
                    word['Dativ Singular 2'] if 'Dativ Singular 2' in word.keys() else '',
                    word['Dativ Singular 3'] if 'Dativ Singular 3' in word.keys() else '',
                    word['Dativ Singular 4'] if 'Dativ Singular 4' in word.keys() else '',
                    word['Dativ Singular stark'] if 'Dativ Singular stark' in word.keys() else '',
                    word['Dativ Singular schwach'] if 'Dativ Singular schwach' in word.keys() else '',
                    word['Dativ Singular gemischt'] if 'Dativ Singular gemischt' in word.keys() else '',
                    word['Dativ Plural'] if 'Dativ Plural' in word.keys() else '',
                    word['Dativ Plural*'] if 'Dativ Plural*' in word.keys() else '',
                    word['Dativ Plural 1'] if 'Dativ Plural 1' in word.keys() else '',
                    word['Dativ Plural 2'] if 'Dativ Plural 2' in word.keys() else '',
                    word['Dativ Plural 3'] if 'Dativ Plural 3' in word.keys() else '',
                    word['Dativ Plural 4'] if 'Dativ Plural 4' in word.keys() else '',
                    word['Dativ Plural stark'] if 'Dativ Plural stark' in word.keys() else '',
                    word['Dativ Plural schwach'] if 'Dativ Plural schwach' in word.keys() else '',
                    word['Dativ Plural gemischt'] if 'Dativ Plural gemischt' in word.keys() else '',
                    
                    word['Akkusativ Singular'] if 'Akkusativ Singular' in word.keys() else '',
                    word['Akkusativ Singular*'] if 'Akkusativ Singular*' in word.keys() else '',
                    word['Akkusativ Singular 1'] if 'Akkusativ Singular 1' in word.keys() else '',
                    word['Akkusativ Singular 2'] if 'Akkusativ Singular 2' in word.keys() else '',
                    word['Akkusativ Singular 3'] if 'Akkusativ Singular 3' in word.keys() else '',
                    word['Akkusativ Singular 4'] if 'Akkusativ Singular 4' in word.keys() else '',
                    word['Akkusativ Singular stark'] if 'Akkusativ Singular stark' in word.keys() else '',
                    word['Akkusativ Singular schwach'] if 'Akkusativ Singular schwach' in word.keys() else '',
                    word['Akkusativ Singular gemischt'] if 'Akkusativ Singular gemischt' in word.keys() else '',
                    word['Akkusativ Plural'] if 'Akkusativ Plural' in word.keys() else '',
                    word['Akkusativ Plural*'] if 'Akkusativ Plural*' in word.keys() else '',
                    word['Akkusativ Plural 1'] if 'Akkusativ Plural 1' in word.keys() else '',
                    word['Akkusativ Plural 2'] if 'Akkusativ Plural 2' in word.keys() else '',
                    word['Akkusativ Plural 3'] if 'Akkusativ Plural 3' in word.keys() else '',
                    word['Akkusativ Plural 4'] if 'Akkusativ Plural 4' in word.keys() else '',
                    word['Akkusativ Plural stark'] if 'Akkusativ Plural stark' in word.keys() else '',
                    word['Akkusativ Plural schwach'] if 'Akkusativ Plural schwach' in word.keys() else '',
                    word['Akkusativ Plural gemischt'] if 'Akkusativ Plural gemischt' in word.keys() else '',
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