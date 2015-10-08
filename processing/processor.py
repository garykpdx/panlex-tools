#!/usr/bin/python3

from collections import OrderedDict
import os


class Entry(object):
    def __init__(self, langs):
        self.langs = langs
        values = [''] * len(langs)
        self.data = dict(zip(langs,values))

    
    def getLanguages(self):
        return langs[:]

    
    def __getitem__(self, idx):
        return self.data[idx]
    
    
    def __setitem__(self, idx, v):
        self.data[idx] = v
    
    
    def __delitem__(self,idx):
        self.data[idx] = ['']

    
    def __repr__(self):
        values = ['\t'.join(self.data[lang]) for lang in self.langs]
        return '%s\n' % ('\t'.join( values))



class Processor(object):
    def __init__(self, base=None):
        if base != None:
            self.basefile = base
        else:
            basedir = os.path.split(os.getcwd())[1]
            self.basefile = '%s-0.txt' % basedir
            self.filterlist = []
        return

    
    def add(self,filter):
        self.filterlist.append( filter)
        return self

    
    def run(self):
        #with codecs.open( self.basefile, encoding='utf-8')
        for filter in self.filterlist:
            filter.run()
