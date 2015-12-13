'''
Created on Oct 1, 2015

@author: gary
'''

import regex as re
from processing.generic import *
from processing import SourceProcesor
from processing import handle_synonyms


class NoFilter(SourceProcesor):
    def __init__(self):
        super(self.__class__, self).__init__()
        
    
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.mark_no_phrase( fields[0])
            entry[lang] = fields
        
        return

    
    @handle_synonyms
    def mark_no_phrase(self, text):
        if re.search('.の.', text):
            return self.add_df( text.strip())
        else:
            return text.strip()
    
    
    def add_df(self, text):
        if text.startswith('⫷df⫸'):
            return text
        else:
            return '⫷df⫸%s' % text



class OrSplitFilter(SourceProcesor):
    def __init__(self):
        super(self.__class__, self).__init__()


    @process_method_outside_parens
    def split_on_or(self, text):
        if len(text.split()) == 3:
            result = re.sub('^(.*?)または(.*)$', r'\1‣\2', text)
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
