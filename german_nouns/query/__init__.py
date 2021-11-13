import difflib
import csv
import re
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Literal, TypedDict, Union

from german_nouns.config import CSV_FILE_PATH, PACKAGE_PATH


INDEX_FILE_PATH = PACKAGE_PATH.joinpath('index.txt')
Record = Dict[str, Any]


class WordSlice(TypedDict):
    lemma: str
    match: str
    pos: int


class NounDictionary(object):

    def __init__(self) -> None:
        self.index = defaultdict(list)

        # parse csv file
        data = list(csv.reader(open(CSV_FILE_PATH)))
        self.header = data[0]
        self.data = data[1:]

        # load or create index file
        if INDEX_FILE_PATH.is_file():
            self.load_index()
        else:
            self.create_index()

    def create_index(self, skip_col_index=3) -> None:
        print('Creating index once.')

        # create index
        for row_idx, row in enumerate(self.data):
            for col_idx, cell in enumerate(row):
                if col_idx <= skip_col_index:
                    continue
                if len(cell) == 0:
                    continue

                word_low = cell.lower()
                if row_idx not in self.index[word_low]:
                    # liste, weil Reihenfolge der Indexes erhalten bleiben muss
                    self.index[word_low].append(row_idx)

        # save index file
        output = ''
        for k, v in self.index.items():
            indexes = '\t'.join(str(x) for x in v)
            output += f'{k}\t{indexes}\n'

        with open(INDEX_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(output)

    def load_index(self) -> None:
        with open(INDEX_FILE_PATH, encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]

            for line in lines:
                split = line.split('\t')
                word_low = split[0]
                self.index[word_low] = [int(x) for x in split[1:] if x]

    def __getitem__(self, key: Union[str, int]) -> Union[Record, List[Record]]:
        if isinstance(key, str):
            key = key.lower()
            results = [self.row_to_dict(self.data[idx]) for idx in self.index[key]]

            # sorty by key similarity to lemma
            # source: https://stackoverflow.com/a/17903726/5732518
            results.sort(
                key=lambda x: difflib.SequenceMatcher(None, x['lemma'], key).ratio(), reverse=True
            )

            return results

        elif isinstance(key, int):
            return self.row_to_dict(self.data[key])

    def __len__(self):
        return len(self.data)

    def row_to_dict(self, row) -> Record:
        result = {'flexion': {}}

        for col_idx, col_name in enumerate(self.header):
            if not row[col_idx]:
                continue

            col_name_low = col_name.lower()

            if col_name_low in ['lemma', 'pos', 'genus']:
                if col_name_low == 'pos':
                    result[col_name] = row[col_idx].split(',')
                else:
                    result[col_name] = row[col_idx]
            else:
                result['flexion'][col_name] = row[col_idx]

        return result

    def last_word(self, compound: str) -> Union[None, Record]:
        """
        find last noun in compound word
        """
        words = self.parse_compound(compound.lower())
        if not words:
            return None

        return self.row_to_dict(self.index[words[-1]])

    def parse_compound(
        self,
        search_val: str,
        exlcude_lemmas: List[str] = []
    ) -> List[str]:
        fugen_laute = {'e', 's', 'es', 'n', 'en', 'er', 'ens'}
        forb_words = {'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr'}
        search_val_low = search_val.lower()

        def loop_characters(chars: str) -> Union[Literal[False], WordSlice]:
            hits: Dict[str, WordSlice] = {}
            test_str = ''

            for idx, char in enumerate(reversed(chars)):
                test_str = char + test_str

                # don't add last character to variants
                if idx == 0:
                    continue

                variations = [test_str]
                for f in fugen_laute:
                    if len(f) >= len(test_str):
                        continue
                    repl = re.sub(f + r'$', '', test_str)
                    if repl and repl != char and repl not in variations:
                        variations.append(repl.lower())

                for var in variations:
                    try:
                        items = [self.row_to_dict(self.data[idx]) for idx
                                 in self.index[var] if self.data[idx][0] not in exlcude_lemmas]
                    except KeyError:
                        continue
                    for item in items:
                        if 'Buchstabe' in item['pos'] \
                                or u'Abkürzung' in item['pos'] \
                                or 'Wortverbindung' in item['pos'] \
                                or 'kompositum' in item:
                            continue
                        if var in hits \
                                or var == search_val_low \
                                or var in forb_words:
                            continue

                        # append position and lemma of found word
                        hits[var] = {
                            'lemma': item['lemma'],
                            'match': var,
                            'pos': search_val_low.index(var)
                        }
            if not hits:
                return False

            # sort hits by word length and position and return first item
            return sorted(
                list(hits.values()), key=lambda k: (-len(k['lemma']), k['pos'])
            )[0]

        results = []
        curr_str = search_val_low
        while True:
            found_word = loop_characters(curr_str)
            if not found_word:
                if len(curr_str) > 1 and self.index[curr_str] and len(results) > 0:
                    results.append(curr_str)
                break

            curr_str = curr_str[:found_word['pos']]
            results.append(found_word['lemma'])

        results.reverse()

        return results
