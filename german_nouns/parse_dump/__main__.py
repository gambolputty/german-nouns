import re
import sys
import locale
from operator import itemgetter
import csv

from bz2 import BZ2File
from wiktionary_de_parser import Parser

from german_nouns.config import CSV_FILE_PATH
from german_nouns.parse_dump.extend_flexion import extend_flexion

# make sure your system supports this locale
# see: https://stackoverflow.com/a/36257050/5732518
locale.setlocale(locale.LC_ALL, "C.UTF-8")

if len(sys.argv) <= 1:
    print("Please provide a path to the Wiktionary XML-Dump file")
    sys.exit()

header = [
    "lemma",
    "pos",
    "genus",
    "genus 1",
    "genus 2",
    "genus 3",
    "genus 4",
    "nominativ singular",
    "nominativ singular*",
    "nominativ singular 1",
    "nominativ singular 2",
    "nominativ singular 3",
    "nominativ singular 4",
    "nominativ singular stark",
    "nominativ singular schwach",
    "nominativ singular gemischt",
    "nominativ plural",
    "nominativ plural*",
    "nominativ plural 1",
    "nominativ plural 2",
    "nominativ plural 3",
    "nominativ plural 4",
    "nominativ plural stark",
    "nominativ plural schwach",
    "nominativ plural gemischt",
    "genitiv singular",
    "genitiv singular*",
    "genitiv singular 1",
    "genitiv singular 2",
    "genitiv singular 3",
    "genitiv singular 4",
    "genitiv singular stark",
    "genitiv singular schwach",
    "genitiv singular gemischt",
    "genitiv plural",
    "genitiv plural*",
    "genitiv plural 1",
    "genitiv plural 2",
    "genitiv plural 3",
    "genitiv plural 4",
    "genitiv plural stark",
    "genitiv plural schwach",
    "genitiv plural gemischt",
    "dativ singular",
    "dativ singular*",
    "dativ singular 1",
    "dativ singular 2",
    "dativ singular 3",
    "dativ singular 4",
    "dativ singular stark",
    "dativ singular schwach",
    "dativ singular gemischt",
    "dativ plural",
    "dativ plural*",
    "dativ plural 1",
    "dativ plural 2",
    "dativ plural 3",
    "dativ plural 4",
    "dativ plural stark",
    "dativ plural schwach",
    "dativ plural gemischt",
    "akkusativ singular",
    "akkusativ singular*",
    "akkusativ singular 1",
    "akkusativ singular 2",
    "akkusativ singular 3",
    "akkusativ singular 4",
    "akkusativ singular stark",
    "akkusativ singular schwach",
    "akkusativ singular gemischt",
    "akkusativ plural",
    "akkusativ plural*",
    "akkusativ plural 1",
    "akkusativ plural 2",
    "akkusativ plural 3",
    "akkusativ plural 4",
    "akkusativ plural stark",
    "akkusativ plural schwach",
    "akkusativ plural gemischt",
]


def create_csv_row(record):
    result = []

    # flatten record['pos'], which is a dict() of lists
    if record["pos"]:
        pos = set()
        for key, value in record["pos"].items():
            pos.add(key)
            if value:
                pos.update(value)
        pos = sorted(list(pos))
        record["pos"] = ",".join(pos)

    for col_name in header:
        if col_name in record:
            result.append(record[col_name])
        elif "flexion" in record and col_name in record["flexion"]:
            result.append(record["flexion"][col_name])
        else:
            result.append("")

    return result


bz = BZ2File(sys.argv[1])
count = 0
rows = []

print("Parsing started...")

# collect records
for record in Parser(
    bz, custom_methods=[extend_flexion], config={"include_wikitext": True}
):
    wikitext = record.get("wikitext", "")

    if record["inflected"] is True:
        continue

    if "lang" not in record or record["lang"].lower() != "deutsch":
        continue

    if "pos" not in record or "Substantiv" not in record["pos"]:
        continue

    # Titel muss Buchstabend enthalten
    if re.search(r"([a-zA-Z]+)", record["title"]) is None:
        continue

    if re.search(r"{{Schweizer und Liechtensteiner Schreibweise\|[^}]+}}", wikitext):
        continue

    if re.search(r"{{Alte Schreibweise\|[^}]+}}", wikitext):
        continue

    rows.append(create_csv_row(record))
    count += 1

# sort alphabetically
rows.sort(key=itemgetter(0))

# write csv file
with open(CSV_FILE_PATH, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)

    # write header row
    csv_writer.writerow(header)

    # write rows
    for row in rows:
        csv_writer.writerow(row)

print(f"Saved {count} records")
