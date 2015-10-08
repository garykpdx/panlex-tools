
class SourceProcesor(object):
    def __init__(self,*cols):
        self.columns = list(cols)
    
    
    def run(self):
        pass



class DelimiterFilter(SourceProcesor):
    def __init__(self, delim):
        self.delimiters = delim


    def run(self, text):
        delims = '[%s]' % self.delimiters
        return re.sub(delims, '‣', text)
        
