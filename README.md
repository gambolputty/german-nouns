# German nouns
A comma seperated list of ~ 90 thousand German nouns and their grammatical properties (*tense, number, gender*) as CSV file. Plus some methods to query the data.

## Usage

## Clone repository and install requirements
```shell
clone https://github.com/gambolputty/german_nouns
bash setup.sh
```

### Create CSV file
```shell
cd german_nouns
python -m create_csv /path-to-dump-file/dewiktionary-latest-pages-articles-multistream.xml.bz2
```

### Query the CSV file
All examples in `german_nouns/query/__main__.py` (command: `cd german_nouns && python -m query`):
```python
from query.NounDictionary import NounDictionary

nouns = NounDictionary('../nouns.csv')

# Lookup a word
word_entry = nouns['Fahrrad']
pprint(word_entry)
# Output:
[{'flexion': {'akkusativ plural': 'Fahrräder',
              'akkusativ singular': 'Fahrrad',
              'dativ plural': 'Fahrrädern',
              'dativ singular': 'Fahrrad',
              'dativ singular*': 'Fahrrade',
              'genitiv plural': 'Fahrräder',
              'genitiv singular': 'Fahrrades',
              'genitiv singular*': 'Fahrrads',
              'nominativ plural': 'Fahrräder',
              'nominativ singular': 'Fahrrad'},
  'genus': 'n',
  'lemma': 'Fahrrad',
  'pos': ['Substantiv']}]

# get the last word of a compound
last_word = nouns.last_word('Falkenstein')
print(last_word)
# Output:
[{'flexion': {'akkusativ plural': 'Steine',
              'akkusativ singular': 'Stein',
              'dativ plural': 'Steinen',
              'dativ singular': 'Stein',
              'dativ singular*': 'Steine',
              'genitiv plural': 'Steine',
              'genitiv singular': 'Steins',
              'genitiv singular*': 'Steines',
              'nominativ plural': 'Steine',
              'nominativ singular': 'Stein'},
  'genus': 'm',
  'lemma': 'Stein',
  'pos': ['Substantiv']}

# parse compound word
compound_words = nouns.parse_compound('Vermögensbildung')
print(compound_words)
# Output:
['vermögen', 'bildung'] # Lookup the words: nouns['vermögen'] etc.
```

List compiled from [WiktionaryDE](https://de.wiktionary.org) with [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser).

License: [Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en).
