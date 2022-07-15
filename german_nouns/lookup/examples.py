from pprint import pprint
from german_nouns.lookup import Nouns

nouns = Nouns()

# Get a word
word_entry = nouns["Fahrrad"]
pprint(word_entry)

# parse compound word
compound_words = nouns.parse_compound("Vermögensbildung")
print(compound_words)
