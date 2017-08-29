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
                'wortart': [],
                'kompositum': '',
            }
            # wortart
            for template in mwparserfromhell.parse(chunk).filter_templates():
                if template.name == 'Wortart':
                    found_word['wortart'].extend([unicode(x) for x in template.params if x != 'Deutsch'])

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
                        key = key.lower()  # normalize
                        value = m.group(2)
                        value = value.replace('[[', '')
                        value = value.replace(']]', '')
                        found_word[key] = value

                    if template.name.matches(u'Deutsch adjektivisch Übersicht'):
                        """
                        ergänze adjektivische Deklinationen, die von der Vorlage
                        autom. ausgefüllt werden und nicht im Wikitext stehen
                        """
                        keys = found_word.keys()
                        if 'stamm' in keys and 'genus' in keys and found_word['genus'] in ['f', 'm', 'n']:
                            kein_singular = True if 'kein singular' in keys and found_word['kein singular'].lower() in ['1', 'ja'] else False
                            kein_plural = True if 'kein plural' in keys and found_word['kein plural'].lower() in ['1', 'ja'] else False
                            stamm = found_word['stamm']
                            genus = found_word['genus']

                            if 'nominativ singular stark' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'r'
                                elif genus == 'f':
                                    form = stamm
                                elif genus == 'n':
                                    form = stamm + u's'
                                found_word['nominativ singular stark'] = form
                            if 'nominativ plural stark' not in keys and kein_plural is False:
                                found_word['nominativ plural stark'] = stamm
                            if 'genitiv singular stark' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'n'
                                elif genus == 'f':
                                    form = stamm + u'r'
                                elif genus == 'n':
                                    form = stamm + u'n'
                                found_word['genitiv singular stark'] = form
                            if 'genitiv plural stark' not in keys and kein_plural is False:
                                found_word['genitiv plural stark'] = stamm + u'r'
                            if 'dativ singular stark' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'm'
                                elif genus == 'f':
                                    form = stamm + u'r'
                                elif genus == 'n':
                                    form = stamm + u'm'
                                found_word['dativ singular stark'] = form
                            if 'dativ plural stark' not in keys and kein_plural is False:
                                found_word['dativ plural stark'] = stamm + u'n'
                            if 'akkusativ singular stark' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'n'
                                elif genus == 'f':
                                    form = stamm
                                elif genus == 'n':
                                    form = stamm + u's'
                                found_word['akkusativ singular stark'] = form
                            if 'akkusativ plural stark' not in keys and kein_plural is False:
                                found_word['akkusativ plural stark'] = stamm

                            if 'nominativ singular schwach' not in keys and kein_singular is False:
                                found_word['nominativ singular schwach'] = stamm
                            if 'nominativ plural schwach' not in keys and kein_plural is False:
                                found_word['nominativ plural schwach'] = stamm + u'n'
                            if 'genitiv singular schwach' not in keys and kein_singular is False:
                                found_word['genitiv singular schwach'] = stamm + u'n'
                            if 'genitiv plural schwach' not in keys and kein_plural is False:
                                found_word['genitiv plural schwach'] = stamm + u'n'
                            if 'dativ singular schwach' not in keys and kein_singular is False:
                                found_word['dativ singular schwach'] = stamm + u'n'
                            if 'dativ plural schwach' not in keys and kein_plural is False:
                                found_word['dativ plural schwach'] = stamm + u'n'
                            if 'akkusativ singular schwach' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'n'
                                else:
                                    form = stamm
                                found_word['akkusativ singular schwach'] = form
                            if 'akkusativ plural schwach' not in keys and kein_plural is False:
                                found_word['akkusativ plural schwach'] = stamm + u'n'

                            if 'nominativ singular gemischt' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'r'
                                elif genus == 'f':
                                    form = stamm
                                elif genus == 'n':
                                    form = stamm + u's'
                                found_word['nominativ singular gemischt'] = form
                            if 'nominativ plural gemischt' not in keys and kein_plural is False:
                                found_word['nominativ plural gemischt'] = stamm
                            if 'genitiv singular gemischt' not in keys and kein_singular is False:
                                found_word['genitiv singular gemischt'] = stamm + u'n'
                            if 'genitiv plural gemischt' not in keys and kein_plural is False:
                                found_word['genitiv plural gemischt'] = stamm + u'n'
                            if 'dativ singular gemischt' not in keys and kein_singular is False:
                                found_word['dativ singular gemischt'] = stamm + u'n'
                            if 'dativ plural gemischt' not in keys and kein_plural is False:
                                found_word['dativ plural gemischt'] = stamm + u'n'
                            if 'akkusativ singular gemischt' not in keys and kein_singular is False:
                                if genus == 'm':
                                    form = stamm + u'n'
                                elif genus == 'f':
                                    form = stamm
                                elif genus == 'n':
                                    form = stamm + u's'
                                found_word['akkusativ singular gemischt'] = form
                            if 'akkusativ plural gemischt' not in keys and kein_plural is False:
                                found_word['akkusativ plural gemischt'] = stamm

            # kompositum?
            sect_herkunft = re.search(r'(?:\{\{Herkunft\}\})((?:\n.+)+)', chunk)
            if sect_herkunft is not None:
                clean = re.sub(r'[^\w\s]', '', sect_herkunft.group(1))
                if re.search(r'kompositum +(aus|von|der substantive|bestehend aus|zusammensetzung|zusammengesetzt|zusammengezogen)', clean, re.I) is not None:
                    found_word['kompositum'] = 1

            # append
            parsed_items.append(found_word)

    result = []
    for w in parsed_items:
        if len(w.keys()) <= 2 and 'kompositum' in w.keys() and 'wortart' in w.keys():
            continue
        if 'Substantiv' not in w['wortart']:
            continue

        new_item = w
        distinct = list(set(new_item['wortart']))
        new_item['wortart'] = u','.join(distinct)
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
            # 'id',
            'lemma',
            'wortart',
            'kompositum',
            'genus',

            'nominativ singular',
            'nominativ singular*',
            'nominativ singular 1',
            'nominativ singular 2',
            'nominativ singular 3',
            'nominativ singular 4',
            'nominativ singular stark',
            'nominativ singular schwach',
            'nominativ singular gemischt',
            'nominativ plural',
            'nominativ plural*',
            'nominativ plural 1',
            'nominativ plural 2',
            'nominativ plural 3',
            'nominativ plural 4',
            'nominativ plural stark',
            'nominativ plural schwach',
            'nominativ plural gemischt',

            'genitiv singular',
            'genitiv singular*',
            'genitiv singular 1',
            'genitiv singular 2',
            'genitiv singular 3',
            'genitiv singular 4',
            'genitiv singular stark',
            'genitiv singular schwach',
            'genitiv singular gemischt',
            'genitiv plural',
            'genitiv plural*',
            'genitiv plural 1',
            'genitiv plural 2',
            'genitiv plural 3',
            'genitiv plural 4',
            'genitiv plural stark',
            'genitiv plural schwach',
            'genitiv plural gemischt',

            'dativ singular',
            'dativ singular*',
            'dativ singular 1',
            'dativ singular 2',
            'dativ singular 3',
            'dativ singular 4',
            'dativ singular stark',
            'dativ singular schwach',
            'dativ singular gemischt',
            'dativ plural',
            'dativ plural*',
            'dativ plural 1',
            'dativ plural 2',
            'dativ plural 3',
            'dativ plural 4',
            'dativ plural stark',
            'dativ plural schwach',
            'dativ plural gemischt',

            'akkusativ singular',
            'akkusativ singular*',
            'akkusativ singular 1',
            'akkusativ singular 2',
            'akkusativ singular 3',
            'akkusativ singular 4',
            'akkusativ singular stark',
            'akkusativ singular schwach',
            'akkusativ singular gemischt',
            'akkusativ plural',
            'akkusativ plural*',
            'akkusativ plural 1',
            'akkusativ plural 2',
            'akkusativ plural 3',
            'akkusativ plural 4',
            'akkusativ plural stark',
            'akkusativ plural schwach',
            'akkusativ plural gemischt',
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
                    word['wortart'] if 'wortart' in word.keys() else '',
                    word['kompositum'],
                    word['genus'] if 'genus' in word.keys() and word['genus'] in 'fmn' else '',

                    word['nominativ singular'] if 'nominativ singular' in word.keys() else '',
                    word['nominativ singular*'] if 'nominativ singular*' in word.keys() else '',
                    word['nominativ singular 1'] if 'nominativ singular 1' in word.keys() else '',
                    word['nominativ singular 2'] if 'nominativ singular 2' in word.keys() else '',
                    word['nominativ singular 3'] if 'nominativ singular 3' in word.keys() else '',
                    word['nominativ singular 4'] if 'nominativ singular 4' in word.keys() else '',
                    word['nominativ singular stark'] if 'nominativ singular stark' in word.keys() else '',
                    word['nominativ singular schwach'] if 'nominativ singular schwach' in word.keys() else '',
                    word['nominativ singular gemischt'] if 'nominativ singular gemischt' in word.keys() else '',
                    word['nominativ plural'] if 'nominativ plural' in word.keys() else '',
                    word['nominativ plural*'] if 'nominativ plural*' in word.keys() else '',
                    word['nominativ plural 1'] if 'nominativ plural 1' in word.keys() else '',
                    word['nominativ plural 2'] if 'nominativ plural 2' in word.keys() else '',
                    word['nominativ plural 3'] if 'nominativ plural 3' in word.keys() else '',
                    word['nominativ plural 4'] if 'nominativ plural 4' in word.keys() else '',
                    word['nominativ plural stark'] if 'nominativ plural stark' in word.keys() else '',
                    word['nominativ plural schwach'] if 'nominativ plural schwach' in word.keys() else '',
                    word['nominativ plural gemischt'] if 'nominativ plural gemischt' in word.keys() else '',

                    word['genitiv singular'] if 'genitiv singular' in word.keys() else '',
                    word['genitiv singular*'] if 'genitiv singular*' in word.keys() else '',
                    word['genitiv singular 1'] if 'genitiv singular 1' in word.keys() else '',
                    word['genitiv singular 2'] if 'genitiv singular 2' in word.keys() else '',
                    word['genitiv singular 3'] if 'genitiv singular 3' in word.keys() else '',
                    word['genitiv singular 4'] if 'genitiv singular 4' in word.keys() else '',
                    word['genitiv singular stark'] if 'genitiv singular stark' in word.keys() else '',
                    word['genitiv singular schwach'] if 'genitiv singular schwach' in word.keys() else '',
                    word['genitiv singular gemischt'] if 'genitiv singular gemischt' in word.keys() else '',
                    word['genitiv plural'] if 'genitiv plural' in word.keys() else '',
                    word['genitiv plural*'] if 'genitiv plural*' in word.keys() else '',
                    word['genitiv plural 1'] if 'genitiv plural 1' in word.keys() else '',
                    word['genitiv plural 2'] if 'genitiv plural 2' in word.keys() else '',
                    word['genitiv plural 3'] if 'genitiv plural 3' in word.keys() else '',
                    word['genitiv plural 4'] if 'genitiv plural 4' in word.keys() else '',
                    word['genitiv plural stark'] if 'genitiv plural stark' in word.keys() else '',
                    word['genitiv plural schwach'] if 'genitiv plural schwach' in word.keys() else '',
                    word['genitiv plural gemischt'] if 'genitiv plural gemischt' in word.keys() else '',

                    word['dativ singular'] if 'dativ singular' in word.keys() else '',
                    word['dativ singular*'] if 'dativ singular*' in word.keys() else '',
                    word['dativ singular 1'] if 'dativ singular 1' in word.keys() else '',
                    word['dativ singular 2'] if 'dativ singular 2' in word.keys() else '',
                    word['dativ singular 3'] if 'dativ singular 3' in word.keys() else '',
                    word['dativ singular 4'] if 'dativ singular 4' in word.keys() else '',
                    word['dativ singular stark'] if 'dativ singular stark' in word.keys() else '',
                    word['dativ singular schwach'] if 'dativ singular schwach' in word.keys() else '',
                    word['dativ singular gemischt'] if 'dativ singular gemischt' in word.keys() else '',
                    word['dativ plural'] if 'dativ plural' in word.keys() else '',
                    word['dativ plural*'] if 'dativ plural*' in word.keys() else '',
                    word['dativ plural 1'] if 'dativ plural 1' in word.keys() else '',
                    word['dativ plural 2'] if 'dativ plural 2' in word.keys() else '',
                    word['dativ plural 3'] if 'dativ plural 3' in word.keys() else '',
                    word['dativ plural 4'] if 'dativ plural 4' in word.keys() else '',
                    word['dativ plural stark'] if 'dativ plural stark' in word.keys() else '',
                    word['dativ plural schwach'] if 'dativ plural schwach' in word.keys() else '',
                    word['dativ plural gemischt'] if 'dativ plural gemischt' in word.keys() else '',
                    
                    word['akkusativ singular'] if 'akkusativ singular' in word.keys() else '',
                    word['akkusativ singular*'] if 'akkusativ singular*' in word.keys() else '',
                    word['akkusativ singular 1'] if 'akkusativ singular 1' in word.keys() else '',
                    word['akkusativ singular 2'] if 'akkusativ singular 2' in word.keys() else '',
                    word['akkusativ singular 3'] if 'akkusativ singular 3' in word.keys() else '',
                    word['akkusativ singular 4'] if 'akkusativ singular 4' in word.keys() else '',
                    word['akkusativ singular stark'] if 'akkusativ singular stark' in word.keys() else '',
                    word['akkusativ singular schwach'] if 'akkusativ singular schwach' in word.keys() else '',
                    word['akkusativ singular gemischt'] if 'akkusativ singular gemischt' in word.keys() else '',
                    word['akkusativ plural'] if 'akkusativ plural' in word.keys() else '',
                    word['akkusativ plural*'] if 'akkusativ plural*' in word.keys() else '',
                    word['akkusativ plural 1'] if 'akkusativ plural 1' in word.keys() else '',
                    word['akkusativ plural 2'] if 'akkusativ plural 2' in word.keys() else '',
                    word['akkusativ plural 3'] if 'akkusativ plural 3' in word.keys() else '',
                    word['akkusativ plural 4'] if 'akkusativ plural 4' in word.keys() else '',
                    word['akkusativ plural stark'] if 'akkusativ plural stark' in word.keys() else '',
                    word['akkusativ plural schwach'] if 'akkusativ plural schwach' in word.keys() else '',
                    word['akkusativ plural gemischt'] if 'akkusativ plural gemischt' in word.keys() else '',
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