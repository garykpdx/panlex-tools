
class EntryFilter(object):
    def __init__(self, func, *attributes):
        self.func = func
        self.attrs = attributes

    def __call__(self, entry, *args, **kwargs):
        for attr in self.attrs:
            field = entry.__getattribute__(attr)
            result = self.func(field, **kwargs)
