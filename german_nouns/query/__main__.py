from pprint import pprint
from query.NounDictionary import NounDictionary

nouns = NounDictionary('../nouns.csv')

# get the last word of a compound
last_word = nouns.last_word('Falkenstein')
print(last_word)

# parse compound word
compound_words = nouns.parse_compound('Vermögensbildung')
print(compound_words)


# pprint(nouns.parse_compound('Vermögensbildung'))
# print('Haus', nouns.parse_compound('Haus'))
# print('Nichtpersonalmaskulinum', nouns.parse_compound('Nichtpersonalmaskulinum'))
# print('Berichterstattung', nouns.parse_compound('Berichterstattung'))
# print('Ersatzlieferungen', nouns.parse_compound('Ersatzlieferungen'))
# print('Vermögensbildung', nouns.parse_compound('Vermögensbildung'))
# print('Transfergesellschaft', nouns.parse_compound('Transfergesellschaft'))
# print('Dampfwalze', nouns.parse_compound('Dampfwalze'))
# print('Einkommensteuer', nouns.parse_compound('Einkommensteuer'))
# print('Einkommensverteilung', nouns.parse_compound('Einkommensverteilung'))
# print('Ertragsteuer', nouns.parse_compound('Ertragsteuer'))
# print('Ertragssteigerung', nouns.parse_compound('Ertragssteigerung'))
# print('Körperschaftsteuer', nouns.parse_compound('Körperschaftsteuer'))
# print('Körperschaftsstatus', nouns.parse_compound('Körperschaftsstatus'))
# print('Verkehrsteuer', nouns.parse_compound('Verkehrsteuer'))
# print('Verkehrszeichen', nouns.parse_compound('Verkehrszeichen'))
# print('Vermögensteuer', nouns.parse_compound('Vermögensteuer'))
# print('Vermögensbildung', nouns.parse_compound('Vermögensbildung'))
# print('Versicherungsteuer', nouns.parse_compound('Versicherungsteuer'))
# print('Versicherungspolice', nouns.parse_compound('Versicherungspolice'))
