'''
Created on Oct 1, 2015

@author: gary
'''

import regex as re
from processing.generic import *
from processing import SourceProcesor
from processing import handle_synonyms


class ArticleFilter(SourceProcesor):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.articles = ['el', 'los', 'la', 'las', '^\s*[ou]']

    
    @handle_synonyms
    def remove_article(self, text):
        for art in self.articles:
            text = re.sub('\s*\m%s\M\s*' % art, ' ', text)
            
        text = re.sub('\mdel\M', 'de', text)
        text = re.sub('^\s*es\M\s*', '', text)
        return text.strip()
        
        
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.remove_article( fields[0])
            entry[lang] = fields
         
        return
            

class OrSplitFilter(SourceProcesor):
    def __init__(self):
        super(self.__class__, self).__init__()


    @process_method_outside_parens
    def split_on_or(self, text):
        if len(text.split()) == 3:
            result = re.sub('^\s*?(?:\S+)(?:,)?\s+[ou]\s+(\S+)\s*$', '‣', text)
            return result
        else:
            return text

    
    def run(self, entry):
        self.parent.run(entry)

        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.split_on_or( fields[0])
            entry[lang] = fields
            
        return
