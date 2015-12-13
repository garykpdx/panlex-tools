
import regex as re


verbs = ['不是', '是', '做(了)?一个', '不幸生', '说', '伤害', '不成', '给', '要作',
         '只为', '呐喊', '信']


def has_verb(text):
    verb_found = False
    
    for vb in verbs:
        if re.search(vb, text):
            return True
    
    return False
