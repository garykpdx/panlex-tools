'''
Created on Oct 1, 2015

@author: gary
'''

import io
import regex as re


lang_map = {'English':'eng-000'}


def get_lang_id(lang):
    return lang_map[lang]



def increment_version(filename, ext=None):
    # filename of XYZ-n (optionally .ext)
    match = re.search('(.*)-(\d+)(?:.(\w+))?', filename)
    if match:
        version = int(match[2]) + 1
        if not ext:
            ext = 'txt'
        else:
            ext = match[3]
            
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



def convert_separator(text, sep='‣'):
    return re.sub(', ', '‣', text)



def remove_final_punct(text):
    return re.sub('((?<!\.\.)\.$|(?:[,/]+)$', '', text)


