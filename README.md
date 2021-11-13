# German nouns

A comma seperated list of ~98 thousand German nouns and their grammatical properties (_tense, number, gender_) as CSV file. Plus a module to look up the data and parse compound words. Compiled from the [WiktionaryDE](https://de.wiktionary.org).

The list can be found here: [german_nouns/nouns.csv](https://github.com/gambolputty/german-nouns/blob/main/german_nouns/nouns.csv)

If you want to look up nouns or parse compound words, install this package (for Python 3.8+) and follow the instructions below:

## Installation

`pip install german-nouns`

## Lookup words

```python
from pprint import pprint
from german_nouns.lookup import Nouns

nouns = Nouns()

# Lookup a word
word = nouns['Fahrrad']
pprint(word)

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

# parse compound word
words = nouns.parse_compound('Vermögensbildung')
print(words)

# Output:
['Vermögen', 'Bildung'] # Now lookup nouns['Vermögen'] etc.
```

## Compiling the list

To compile the list yourself, you need Python 3.8+ and [Poetry](https://python-poetry.org/) installed.

### 1. Clone the repository and install dependencies with [Poetry](https://python-poetry.org/):

```shell
$ git clone https://github.com/gambolputty/german-nouns
$ cd german-nouns
$ poetry install
```

### 2. Compile the list of nouns from a Wiktionary XML file:

Find the latest XML-dump files here: [https://dumps.wikimedia.org/dewiktionary/latest](https://dumps.wikimedia.org/dewiktionary/latest), for example [this one](https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles-multistream.xml.bz2) and download it. Then execute:

```shell
$ poetry run python -m german_nouns.parse_dump /path-to-xml-dump-file.xml.bz2
```

The CSV file will be saved here: [german_nouns/nouns.csv](https://github.com/gambolputty/german-nouns/blob/main/german_nouns/nouns.csv).


----

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
