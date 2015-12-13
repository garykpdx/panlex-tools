
import collections

import io
import regex as re

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

    def __str__(self):
        return '\t'.join( self.data)


    def __repr__(self):
        values = [('<%s:%s>' % (lang,self.__getitem__(lang))) for lang in self.lang_cols]
        return 'Entry(%s)' % ';'.join(values)


def ignore_parens(proc):
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


def process_synonyms(proc):
    # s = '‣'
    def wrapper(text):
        fields = text.split('‣')
        for i in range(len(fields)):
            fields[i] = proc(fields[i])
        return '‣'.join( fields)
    return wrapper


@ignore_parens
def normalize_synonym_delimiter(text, delim='‣'):
    text = re.sub('\s*,\s*', delim, text)
    return text


def increment_fileid(filename, ext=None):
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


def append_synonym(text, elem):
    if len(text.strip()) == 0:
        return elem

    fields = text.split('\s*‣\s*')

    if elem not in fields:
        # append to list
        return '%s‣%s' % (text,elem)
    else:
        # already in list, don't append
        return text
