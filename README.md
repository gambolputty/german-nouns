# German nouns
A comma seperated list of ~ 90 thousand German nouns and their grammatical properties (*tense, number, gender*) as CSV file. Plus some methods to query the data.

## Usage

### Create CSV file
```bash
cd german_nouns
python -m create_csv /path-to-dump-file/dewiktionary-latest-pages-articles-multistream.xml.bz2
```

### Query the CSV file
Example in `german_nouns/query/__main__.py` (command: `cd german_nouns && python -m query`):
```python
from query.NounDictionary import NounDictionary

nouns = NounDictionary('../nouns.csv')

# get the last word of a compound
last_word = nouns.last_word('Falkenstein')
print(last_word)
# Output:
# [{'flexion': {'nominativ singular': 'Stein', 'nominativ plural': 'Steine', 'genitiv singular': 'Steins', 'genitiv singular*': 'Steines', 'genitiv plural': 'Steine', 'dativ singular': 'Stein', 'dativ singular*': 'Steine', 'dativ plural': 'Steinen', 'akkusativ singular': 'Stein', 'akkusativ plural': 'Steine'}, 'lemma': 'Stein', 'pos': ['Substantiv'], 'genus': 'm'}]

# parse compound word
compound_words = nouns.parse_compound('Vermögensbildung')
print(compound_words)
# Output:
# ['vermögen', 'bildung']
```

List compiled from [WiktionaryDE](https://de.wiktionary.org) with [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser).

License: [Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en).
