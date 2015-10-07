'''
Created on Oct 1, 2015

@author: gary
'''

import regex as re


def extract_verb(text):
    return re.sub('\bto\s+(.*)', r'\1')



def extract_inchoative(text):
    return re.sub('\b(make|cause to)\s+(.*)', r'\1')



def extract_article(text):
    return re.sub('\b(a|an|the)\s+(.*)', r'\1')
