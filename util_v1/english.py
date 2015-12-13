
import regex as re

from newutil import *

@process_synonyms
def normalize_verb(text, **kwargs):
    return re.sub('^to\s+(.*)', r'\1', text)
