#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ElementTree
import progressbar

import helper
from pprint import pprint


class Wortformen(object):

    """
    Wortformen
    """

    def __init__(self, file_path):

        # load file
        # self.Tree = ElementTree.iterparse(file_path, events=("start", "end"))
        self.Items = ElementTree.parse(file_path).getroot().findall('item')

    def plurals(self):
        self.NumerusPairs = {}
        bar = progressbar.ProgressBar()
        for item in bar(self.Items):

            # all_forms = [f for f in item.findall('lemma') if f.get('wkl') in ['SUB', 'EIG', 'VER', 'ADJ']]

            for child in item.findall('lemma'):
                
                if child.get('kas') == 'NOM':

                    # if wkl not in ['SUB', 'EIG']:
                    #     save_item = False
                    #     break

                    num = child.get('num')
                    if child.get('wkl') in ['SUB', 'EIG'] and num in ['SIN', 'PLU'] and child.get('der') is None:
                        if child.text not in self.NumerusPairs.keys():
                            self.NumerusPairs[child.text] = {}
                        self.NumerusPairs[child.text][num.lower()] = item.find('form').text
                        self.NumerusPairs[child.text]['gen'] = child.get('gen').lower()

    def saveCSV(self):
        csv = u''
        for key, values in wf.NumerusPairs.items():
            sin = values.get(u'sin', u'')
            plu = values.get(u'plu', u'')
            gen = values.get(u'gen', u'')
            if sin and plu and gen:
                csv += u"{},{},{}\n".format(sin, plu, gen)

            # header
            csv = u"singular;plural;genus\n" + csv
            helper.writeFile('nouns.csv', csv, 'txt')



if __name__ == '__main__':
    wf = Wortformen(
        '/Users/gregor/Dropbox/Python/projects/sorry/data/morphy-export-20110722.xml')
    wf.plurals()
    # wf.find('Kriege', {
    #     'wkl': 'SUB',
    #     'num': 'PLU'
    # })
