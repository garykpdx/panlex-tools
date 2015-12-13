
import functools
import io
import regex as re


def handle_synonyms(func):
    def synonym_handler(self, text):
        fields = text.split('‣')
        for i in range(len(fields)):
            fields[i] = func(self, fields[i])
        
        return '‣'.join(fields)
    
    return synonym_handler



def trace(f):
    def wrapper(*args,**kwargs):
        params = list(args) + list(kwargs.values())
        params_text = ','.join([p.__repr__() for p in params])
        
        result = f(*args,**kwargs)
        if isinstance(result, types.GeneratorType):
            results_list = [x for x in result]
            results = ', '.join([r.__repr__() for r in results_list])
            print(("%s(%s) -> [%s]\n" % (f.__name__.upper(),params_text,results)))
            return (r for r in results_list)
        else:
            print("%s(%s) -> %s\n" % (f.__name__.upper(),params_text,result.__repr__()))
            return result
        
        return wrapper



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

    
    def strip_extra(self, text):
        meanings = text.split('⁋')
        for i,meaning in enumerate(meanings):
            synonyms = meaning.split('‣')
            
            for j,syn in enumerate(synonyms):
                text = syn.strip(self.strip_pattern)
                synonyms[j] = text
            meanings[i] = '‣'.join(synonyms)
            
        return '⁋'.join(meanings)

    
    def run(self, entry):
        self.parent.run(entry)

        for lang in self.columns:
            fields = entry[lang]
            text = self.strip_extra(fields[0])
            fields[0] = text
            entry[lang] = fields
        return self



class PosNormalizeFilter(SourceProcesor):
    def __init__(self,mapping={}):
        super(self.__class__, self).__init__()
        self.mapping = mapping

    
    def normalize(self, tag):
        return self.mapping[ tag]

    
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            text = self.normalize(fields[1])
            entry[lang] = fields
            
        return self
                                                    


class DelimiterFilter(SourceProcesor):
    def __init__(self, pattern_to_replace='[,\uFF0C]\s*'):
        super(self.__class__, self).__init__()
        self.delim_pat = pattern_to_replace


    @handle_outside_parens
    def replace_delim(self, text):
        result = re.sub(self.delim_pat, '‣', text)
        result = re.sub('\s*;\s*(?=\w+)', '⁋', result)
        return result
    
    
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            fields[0] = self.replace_delim( fields[0])
            entry[lang] = fields

        return self
        

class PunctFilter(SourceProcesor):
    def __init__(self, remove_re='^[-,. ]*$'):
        self.remove_re = remove_re
    

    @handle_synonyms
    def normalize_epplisis(self, text):
        return re.sub('\s*\.{2,}\s*', ' … ', text)

    
    @handle_synonyms
    def remove_final_punctuation(self, text):
        result = re.sub('\.+\s*$', '', text)
        result = re.sub('…\s*$', '', result)
        return result

    
    def run(self, entry):
        self.parent.run(entry)
        
        for lang in self.columns:
            fields = entry[lang]
            text = fields[0]

            text = self.normalize_epplisis(text)
            text = self.remove_final_punctuation(text)
            fields[0] = text
            entry[lang] = fields
        
        return self
    
