import pytest

from german_nouns.lookup import Nouns

test_wordss = [
    ('Faktencheck', [{'flexion': {'nominativ singular': 'Faktencheck',
                                  'nominativ plural': 'Faktenchecks',
                                  'genitiv singular': 'Faktenchecks',
                                  'genitiv plural': 'Faktenchecks',
                                  'dativ singular': 'Faktencheck',
                                  'dativ plural': 'Faktenchecks',
                                  'akkusativ singular': 'Faktencheck',
                                  'akkusativ plural': 'Faktenchecks'},
                      'lemma': 'Faktencheck',
                      'pos': ['Substantiv'],
                      'genus': 'm'}]),
    ('Krüge', [{'flexion': {'nominativ singular': 'Krug',
                            'nominativ plural': 'Krüge',
                            'genitiv singular': 'Kruges',
                            'genitiv singular*': 'Krugs',
                            'genitiv plural': 'Krüge',
                            'dativ singular': 'Krug',
                            'dativ singular*': 'Kruge',
                            'dativ plural': 'Krügen',
                            'akkusativ singular': 'Krug',
                            'akkusativ plural': 'Krüge'},
                'lemma': 'Krug',
                'pos': ['Substantiv'],
                'genus': 'm'}]),
    ('Heidelberg', [{'flexion': {}, 'lemma': 'Heidelberg', 'pos': ['Substantiv', 'Toponym']}])
]

compound_test_words = [
    ('Faktencheck', ['Fakt', 'Check']),
    ('Dreiergespann', ['Dreier', 'Gespann']),
    ('Falkenstein', ['Falke', 'Stein']),
    ('Vermögensbildung', ['Vermögen', 'Bildung']),
    ('Nichtpersonalmaskulinum', ['Personalmaskulinum']),
    ('Berichterstattung', ['Bericht', 'Erstattung']),
    ('Ersatzlieferungen', ['Ersatz', 'Lieferung']),
    ('Transfergesellschaft', ['Transfer', 'Gesellschaft']),
    ('Dampfwalze', ['Dampf', 'Walze']),
    ('Einkommensteuer', ['Einkommen', 'Steuer']),
    ('Einkommensverteilung', ['Einkommen', 'Verteilung']),
    ('Ertragsteuer', ['Ertrag', 'Steuer']),
    ('Ertragssteigerung', ['Ertrag', 'Steigerung']),
    ('Körperschaftsteuer', ['Körperschaft', 'Steuer']),
    ('Körperschaftsstatus', ['Körperschaft', 'Status']),
    ('Verkehrszeichen', ['Verkehr', 'Zeichen']),
    ('Versicherungsteuer', ['Versicherung', 'Steuer']),
    ('Versicherungspolice', ['Versicherung', 'Police']),
]


class TestLookup:
    @pytest.mark.parametrize('test_input,expected', test_wordss)
    def test_lookup(self, test_input, expected):
        nouns = Nouns()
        result = nouns[test_input]

        assert result == expected

    @pytest.mark.parametrize('test_input,expected', compound_test_words)
    def test_parse_compound(self, test_input, expected):
        nouns = Nouns()
        result = nouns.parse_compound(test_input)

        assert result == expected
