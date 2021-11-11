from operator import itemgetter
import locale
import csv

# make sure your system supports this locale
# see: https://stackoverflow.com/a/36257050/5732518
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

header = [
    'lemma',
    'pos',
    'genus',
    'genus 1',
    'genus 2',
    'genus 3',
    'genus 4',

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


def create_csv_lines(data):
    lines = []

    for record in data:
        line = []
        # flatten record['pos'], which is a dict() of lists
        if record['pos']:
            pos = set()
            for key, value in record['pos'].items():
                pos.add(key)
                if value:
                    pos.update(value)
            pos = list(pos)
            record['pos'] = ','.join(pos)

        for col_name in header:
            if col_name in record:
                line.append(record[col_name])
            elif 'flexion' in record and col_name in record['flexion']:
                line.append(record['flexion'][col_name])
            else:
                line.append('')

        lines.append(line)

    # sort alphabetically
    result = sorted(lines, key=itemgetter(0))

    return result


def save(csv_path, data):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)

        # map dict values to list
        csv_lines = create_csv_lines(data)

        for line in csv_lines:
            csv_writer.writerow(line)
