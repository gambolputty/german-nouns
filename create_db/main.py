import xml.etree.ElementTree as etree
import os
import re
from bz2file import BZ2File
from pdb import set_trace as bp
from pprint import pprint
from wiktionary_de_parser import Parser
from extend_flexion import extend_flexion
from save import save

bzfile_path = 'dewiktionary-latest-pages-articles-multistream.xml.bz2'
bz = BZ2File(bzfile_path)

data = []
for record in Parser(bz, custom_methods=[extend_flexion]):
    # Titel muss Buchstabend enthalten
    if re.search(r'([a-zA-Z]+)', record['title']) is None:
        continue

    if re.search(r'{{Schweizer und Liechtensteiner Schreibweise\|[^}]+}}', record['wikitext']):
        continue

    if re.search(r'{{Alte Schreibweise\|[^}]+}}', record['wikitext']):
        continue

    if record['inflected'] is True:
        continue

    if 'language' not in record or record['language'].lower() != 'deutsch':
        continue

    if 'pos' not in record or 'Substantiv' not in record['pos']:
        continue

    data.append(record)

save('local.db', data)

print(f'Saved {len(data)} records')
