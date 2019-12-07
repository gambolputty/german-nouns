from operator import itemgetter
import os
import locale
import csv
locale.setlocale(locale.LC_ALL, 'deu_deu' if os.name == 'nt' else 'de_DE.UTF-8')
import sqlite3

# from pdb import set_trace as bp

header = [
    # 'id',
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


def create_db_entries(db, data):
    # map dict values to list
    for word_data in data:
    
        for col_name in header:
            if col_name in word_data:
                db.execute('INSERT INTO Nomen VALUES(NULL,\'{}\',\'{}\',\'{}\')'.format(word_data['lemma'], col_name, word_data[col_name]))
            elif 'flexion' in word_data and col_name in word_data['flexion']:
                db.execute('INSERT INTO Nomen VALUES(NULL,\'{}\',\'{}\',\'{}\')'.format(word_data['lemma'], col_name, word_data['flexion'][col_name]))
            else:
                pass

def save(db_path, data):
        
    db = sqlite3.connect(db_path)

    db.execute('CREATE TABLE IF NOT EXISTS Nomen (id INTEGER PRIMARY KEY AUTOINCREMENT, lemma VARCHAR(250), Typ VARCHAR(250), Wortform VARCHAR(250))')

    create_db_entries(db, data)

    db.commit()

    db.close()