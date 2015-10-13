#!/usr/bin/python3

from collections import OrderedDict
import os



class Entry(object):
    def __init__(self, lang_cols):
        self.lang_cols = dict(lang_cols)
        self.data = [''] * sum(self.lang_cols.values())
        self.lang_order = [lang for lang,count in lang_cols]

        idx = 0
        self.col_index = {}
        for lang,count in lang_cols:
            self.col_index[lang] = idx
            idx += count

    
    def get_language_columns(self):
        cols = []
        idx = 0
        
        for lang in self.lang_order:
            cols.append((lang,idx))
            idx += self.lang_cols[lang]
            
        return cols

    
    def _get_range(self, lang):
        idx = self.col_index[lang]
        count = self.lang_cols[lang]
        return (idx,(idx + count))

    
    def __getitem__(self, lang):
        (start,stop) = self._get_range(lang)
        return self.data[start:stop]
    
    
    def __setitem__(self, lang, value_list):
        (start,stop) = self._get_range(lang)
        if len(value_list) != (stop-start):
            raise IndexError('Found %d values, should be %d' % (len(value_list),(stop-start)))
        self.data[start:stop] = value_list
    
    
    def __delitem__(self,lang):
        start,stop = self._get_range(lang)
        for idx in range(start,stop):
            self.data[idx] = ''

    
    def __repr__(self):        
        return '\t'.join( self.data)




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
