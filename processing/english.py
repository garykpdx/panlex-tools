'''
Created on Oct 1, 2015

@author: gary
'''

import regex as re
from processing import process_synonyms
from processing import SourceProcesor
from processing import handle_synonyms


def extract_inchoative(text):
    return re.sub('\b(make|cause to)\s+(.*)', r'\1')



def extract_article(text):
    return re.sub('\b(a|an|the)\s+(.*)', r'\1')



class InfinitiveFilter(SourceProcesor):
    def __init__(self, pat='^to (.*)$'):
        super(self.__class__, self).__init__()
        self.inf_pat = re.compile(pat)

    @handle_synonyms
    def replace_infinitive(self, text):
        match = self.inf_pat.search(text)
        if match:
            text = self.inf_pat.sub(r'\1', text)
        
        return text
    
    
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.replace_infinitive( fields[0])
            entry[lang] = fields

        return


class AuxFilter(SourceProcesor):
    def __init__(self):
        super(self.__class__, self).__init__()
        
    @handle_synonyms
    def replace_aux(self, text):
        text = text.strip()
        text = re.sub('^be ', '', text)
        text = re.sub('^(.*) of something$', r'\1 (of something)', text)
        text = re.sub('^(.*) something$', r'\1 (something)', text)
        text = re.sub('^(.*) someone$', r'\1 (someone)', text)
        text = re.sub('(.*) type$', r'(type of) \1', text)
        text = re.sub('(.*) type (\(.*\))(.*)$', r'(type of) \1 \2\3', text)
        return text
        
        
    def run(self, entry):
        self.parent.run(entry)
            
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.replace_aux( fields[0])
            entry[lang] = fields
                
        return
            
