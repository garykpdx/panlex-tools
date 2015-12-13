'''
Created on Oct 1, 2015

@author: gary
'''

import io
import regex as re
import types

lang_map = {'English':'eng-000'}


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



def get_lang_id(lang):
    return lang_map[lang]



def increment_version(filename, ext=None):
    # filename of XYZ-n (optionally .ext)
    match = re.search('(.*)-(\d+)(?:\.(\w+))?$', filename)
    if match:
        version = int(match[2]) + 1
        if not ext:
            ext = 'txt'
        else:
            if match[3]:
                ext = match[3]
            else:
                ext = 'txt'
                
        return '%s-%d.%s' % (match[1],version,ext)
    
    else:
        raise ValueError('Unable to match filename pattern')


    
def process_outide_parens(proc):
    pat = re.compile('\([^)]*\)')

    def wrapper(text):
        if not pat.search(text):
            return proc(text)

        out = io.StringIO()

        i = j = 0
        for match in pat.finditer(text):
            j = match.start()
            out.write( proc(text[i:j]))
            i = match.end()
            out.write( text[j:i])

        out.write( proc(text[i:]))
        text = out.getvalue()
        out.close()
        return text

    return wrapper



def process_method_outside_parens(func):
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


def process_outide_parens_with_gen(proc):
    pat = re.compile('\([^)]*\)')

    def wrapper(text):
        if not pat.search(text):
            return proc(text)
        
        out = io.StringIO()
        
        i = j = 0
        for match in pat.finditer(text):
            j = match.start()
            for text in proc(text[i:j]):
                out.write( text)
            i = match.end()
            out.write( text[j:i])
        for text in proc(text[i:]):
            out.write( text)
        text = out.getvalue()
        out.close()
        return text
    
    return wrapper



def normalize_ellipsis(text):
    return re.sub('\.{3,6}', '…', text)



def process_synonyms(proc):
    # s = '‣'
    def wrapper(text):
        fields = text.split('‣')
        for i in range(len(fields)):
            fields[i] = proc(fields[i])
        return '‣'.join( fields)
    return wrapper



def process_method_synonyms(proc):
    # s = '‣'
    def wrapper(self,text):
        fields = text.split('‣')
        for i in range(len(fields)):
            fields[i] = proc(self, fields[i])
        return '‣'.join( fields)
    return wrapper



def convert_separator(text, sep='‣'):
    return re.sub(', ', '‣', text)



def remove_final_punct(text):
    return re.sub('((?<!\.\.)\.$|(?:[,/]+)$', '', text)



def append_synonym(text, elem):
    fields = text.split('\s*‣\s*')
    
    if len(fields) == 0:
        # nothing to append to
        return elem
    else:
        if elem not in fields:
            # append to list
            return '%s‣%s' % (text,elem)
        else:
            # already in list, don't append
            return text
        


