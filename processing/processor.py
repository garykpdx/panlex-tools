#!/usr/bin/python3

import os

class Processor(object):
    def __init__(self, base=None):
        if base != None:
            self.basefile = base
        else:
            basedir = os.path.split(os.getcwd())[1]
            self.basefile = '%s-0.txt' % basedir
            self.filterlist = []
        return

    def add(self,filter):
        self.filterlist.append( filter)
        return self

    def run(self):
        #with codecs.open( self.basefile, encoding='utf-8')
        for filter in self.filterlist:
            filter.run()
            

def run_processes(text, proc_list):
    for proc in proc_list:
        text = proc(text)
    return text
