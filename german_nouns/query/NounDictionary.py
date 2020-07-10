from os.path import isfile, dirname
import difflib
import csv
import re
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path

class NounDictionary(object):

    def __init__(self, nouns_path, index_path=None):
        if not isinstance(nouns_path, str) or not isfile(nouns_path):
            raise Exception('Nouns csv file is incorrect')

        self.index = defaultdict(list)

        # parse nouns csv file to data
        nouns_file_path = Path(nouns_path)
        nouns_folder_path = nouns_file_path.parent
        data = list(csv.reader(open(nouns_file_path)))
        self.header = data[0]
        self.data = data[1:]

        # get or create index
        default_index_path = f'{nouns_folder_path.joinpath("nouns_index.txt")}'
        index_path_is_str = isinstance(index_path, str)
        index_file_path = Path(index_path) if index_path_is_str else default_index_path
        index_file_exists = isfile(index_file_path)

        if index_file_exists:
            # load index file
            self.load_index(index_file_path)
        else:
            # create index
            self.create_index(index_file_path)

    
    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.lower()
            results = [self.row_to_dict(self.data[idx]) for idx in self.index[key]]
            # sorty by key similarity to lemma
            # source: https://stackoverflow.com/a/17903726/5732518
            results = sorted(results, key=lambda x: difflib.SequenceMatcher(None, x['lemma'], key).ratio(), reverse=True)
            return results
        elif isinstance(key, int):
            return self.row_to_dict(self.data[key])


    def __len__(self):
        return len(self.data)


    def create_index(self, file_path, skip_col_index=3):
        print('Creating index once.')
        
        # create index
        for row_idx, row in tqdm(enumerate(self.data)):
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
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output)


    def load_index(self, file_path):
        with open(file_path, encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
            for line in lines:
                split = line.split('\t')
                word_low = split[0]
                self.index[word_low] = [int(x) for x in split[1:] if x]


    def row_to_dict(self, row):
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

    
    def last_word(self, compound):
        """
        find last noun in compound word
        """
        words = self.parse_compound(compound.lower(), strict=False)
        if not words: return None

        return [self.row_to_dict(self.data[i]) for i in self.index[words[-1]]]


    def parse_compound(self, search_val, strict=False):
        fugen_laute = {'e', 's', 'es', 'n', 'en', 'er', 'ens'}
        forb_words = {'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr'}
        search_val_low = search_val.lower()

        def loop_characters(chars):
            hits = defaultdict(dict)
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
                        items = [self.row_to_dict(self.data[idx]) for idx in self.index[var]]
                    except KeyError:
                        continue
                    for item in items:
                        if 'Buchstabe' in item['pos'] \
                                or u'Abkürzung'in item['pos'] \
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
            return sorted(list(hits.values()), key=lambda k: (-len(k['lemma']), k['pos']))[0]

        results = []
        curr_str = search_val_low
        while True:
            found_word = loop_characters(curr_str)
            if not found_word:
                if len(curr_str) > 1 and self.index[curr_str] and len(results) > 0:
                    results.append(curr_str)
                break

            curr_str = curr_str[:found_word['pos']]
            results.append(found_word)

        results.reverse()

        if strict is True:
            if len(results['lemma']) <= 1:
                return []

        return results
