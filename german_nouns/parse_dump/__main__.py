import re
import sys

from bz2file import BZ2File
from wiktionary_de_parser import Parser

from german_nouns.parse_dump.extend_flexion import extend_flexion
from german_nouns.parse_dump.save import save

if len(sys.argv) <= 1:
    print('Please provide a path to the Wiktionary XML-Dump file')
    sys.exit()

data = []
dump_path = sys.argv[1]
bz = BZ2File(dump_path)

for record in Parser(bz, custom_methods=[extend_flexion]):

    if record['inflected'] is True:
        continue

    if 'lang' not in record or record['lang'].lower() != 'deutsch':
        continue

    if 'pos' not in record or 'Substantiv' not in record['pos']:
        continue

    # Titel muss Buchstabend enthalten
    if re.search(r'([a-zA-Z]+)', record['title']) is None:
        continue

    if re.search(r'{{Schweizer und Liechtensteiner Schreibweise\|[^}]+}}', record['wikitext']):
        continue

    if re.search(r'{{Alte Schreibweise\|[^}]+}}', record['wikitext']):
        continue

    data.append(record)

save('nouns.csv', data)

print(f'Saved {len(data)} records')
