
import functools
import io
import regex as re

import processing


def handle_synonyms(func):
    def synonym_handler(self, text):
        fields = text.split('‣')
        for i in range(len(fields)):
            fields[i] = func(self, fields[i])
        
        return '‣'.join(fields)
    return synonym_handler



def handle_outside_parens(func):
    pat = re.compile('\([^)]*\)')
    
    def wrapper(self, text):
        if not pat.search(text):
            return func(self, text)
        
        out = io.StringIO()
        
        i = j = 0
        for match in pat.finditer(text):
            j = match.start()
            out.write( func(self, text[i:j]))
            i = match.end()
            out.write( text[j:i])
            
        out.write( func(self, text[i:]))
        text = out.getvalue()
        out.close()
        return text
        
    return wrapper



class NullFilter(object):
    def run(self, e):
        return



class SourceProcesor(object):
    def __init__(self):
        self.columns = ()
        self.parent = NullFilter()
        return

    
    def set_languages(self, *cols):
        self.columns = cols
        return

    
    def set_parent(self, parent):
        self.parent = parent
        return



class TextStripFilter(SourceProcesor):
    def __init__(self, strip_pat = '[ \t\n\u00A0\uFEFF]'):
        super(self.__class__, self).__init__()
        self.strip_pattern = strip_pat
        return


    @handle_synonyms
    def strip_extra(self, text):
        return text.strip( self.strip_pattern)

    
    def run(self, entry):
        self.parent.run(entry)

        for lang in self.columns:
            fields = entry[lang]
            for i in range(len(fields)):
                fields[i] = self.strip_extra(fields[i])
            
            entry[lang] = fields
        return



class DelimiterFilter(SourceProcesor):
    def __init__(self, pattern_to_replace='[,;:/]\s*'):
        super(self.__class__, self).__init__()
        self.delim_pat = pattern_to_replace


    @handle_outside_parens
    def replace_delim(self, text):
        return re.sub(self.delim_pat, '‣', text)
    
    
    def run(self, entry):
        self.parent.run(entry)
                  
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.replace_delim( fields[0])
            entry[lang] = fields
        
        
