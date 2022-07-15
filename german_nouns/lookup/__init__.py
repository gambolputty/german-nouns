import difflib
import csv
import re
from collections import defaultdict
from typing import Any, Dict, List, Literal, TypedDict, Union

from german_nouns.config import CSV_FILE_PATH, PACKAGE_PATH


INDEX_FILE_PATH = PACKAGE_PATH.joinpath("index.txt")
Record = Dict[str, Any]


class WordSlice(TypedDict):
    lemma: str
    match: str
    pos: int


class Nouns(object):
    def __init__(self) -> None:
        # parse csv file
        data = list(csv.reader(open(CSV_FILE_PATH)))
        self.header = data[0]
        self.data = data[1:]

        # load or create index file
        self.index = defaultdict(list)
        if INDEX_FILE_PATH.is_file():
            self.load_index()
        else:
            self.create_index()

    def create_index(self) -> None:
        print("Creating index once")

        # create index
        col_index_to_skip = {
            1,
            2,
            3,
            4,
            5,
            6,
        }  # everything before "pos" and after the last "genus" column
        for row_idx, row in enumerate(self.data):
            for col_idx, word in enumerate(row):
                if col_idx in col_index_to_skip:
                    continue
                if not word:
                    continue

                word_low = word.lower()
                if row_idx not in self.index[word_low]:
                    # liste, weil Reihenfolge der Indexes erhalten bleiben muss
                    self.index[word_low].append(row_idx)

        # save index file
        output = ""
        for k, v in self.index.items():
            indexes = "\t".join(str(x) for x in v)
            output += f"{k}\t{indexes}\n"

        with open(INDEX_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(output)

    def load_index(self) -> None:
        with open(INDEX_FILE_PATH, encoding="utf8") as f:
            lines = [l.strip() for l in f.readlines()]

            for line in lines:
                split = line.split("\t")
                word_low = split[0]
                self.index[word_low] = [int(x) for x in split[1:] if x]

    def __getitem__(self, key: Union[str, int]) -> List[Record]:
        if isinstance(key, str):
            index_item = self.index[key.lower()]
            results = [self.row_to_dict(self.data[idx]) for idx in index_item]

            # Sorty by key similarity to lemma
            # source: https://stackoverflow.com/a/17903726/5732518
            results.sort(
                key=lambda x: difflib.SequenceMatcher(None, x["lemma"], key).ratio(),
                reverse=True,
            )

            return results

        elif isinstance(key, int):
            return [self.row_to_dict(self.data[key])]

    def __len__(self):
        return len(self.data)

    def row_to_dict(self, row) -> Record:
        result = {"flexion": {}}

        for col_idx, col_name in enumerate(self.header):
            if not row[col_idx]:
                continue

            if col_name in [
                "lemma",
                "pos",
                "genus",
                "genus 1",
                "genus 2",
                "genus 3",
                "genus 4",
            ]:
                if col_name == "pos":
                    result[col_name] = row[col_idx].split(",")
                else:
                    result[col_name] = row[col_idx]
            else:
                result["flexion"][col_name] = row[col_idx]

        return result

    def parse_compound(
        self, search_val: str, exlcude_lemmas: List[str] = []
    ) -> List[str]:
        fugen_laute = {"e", "s", "es", "n", "en", "er", "ens"}
        forb_words = {"ich", "du", "er", "sie", "es", "wir", "ihr"}
        forb_pos = {
            "Buchstabe",
            "Abkürzung",
            "Wortverbindung",
            "Vorname",
            "Nachname",
            "Familienname",
            "Eigenname",
            "Straßenname",
            "Ortsnamengrundwort",
            "Toponym",
        }
        search_val_low = search_val.lower()

        def loop_characters(chars: str) -> Union[Literal[False], WordSlice]:
            hits: Dict[str, WordSlice] = {}
            test_str = ""

            for idx, char in enumerate(reversed(chars)):
                test_str = char + test_str

                # don't add last character to variants
                if idx == 0:
                    continue

                variations = [test_str]
                for f in fugen_laute:
                    if len(f) >= len(test_str):
                        continue
                    repl = re.sub(f + r"$", "", test_str)
                    if repl and repl != char and repl not in variations:
                        variations.append(repl.lower())

                for var in variations:
                    try:
                        items = [
                            self.row_to_dict(self.data[idx])
                            for idx in self.index[var]
                            if self.data[idx][0] not in exlcude_lemmas
                        ]
                    except KeyError:
                        continue
                    for item in items:
                        # exclude forbidden POS
                        if forb_pos.intersection(item["pos"]):
                            continue
                        if var in hits or var == search_val_low or var in forb_words:
                            continue

                        # append position and lemma of found word
                        hits[var] = {
                            "lemma": item["lemma"],
                            "match": var,
                            "pos": search_val_low.index(var),
                        }
            if not hits:
                return False

            # sort hits by word length and position and return first item
            return sorted(
                list(hits.values()), key=lambda k: (-len(k["lemma"]), k["pos"])
            )[0]

        results = []
        curr_str = search_val_low
        while True:
            found_word = loop_characters(curr_str)
            if not found_word:
                if len(curr_str) > 1 and self.index[curr_str] and len(results) > 0:
                    results.append(curr_str)
                break

            curr_str = curr_str[: found_word["pos"]]
            results.append(found_word["lemma"])

        results.reverse()

        return results
