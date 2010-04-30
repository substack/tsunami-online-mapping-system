class DefaultDict(dict) :
    def __init__(self, default, *args, **kwargs) :
        self.default = default
        return dict.__init__(self, *args, **kwargs)
    
    def __getitem__(self, key) :
        if self.has_key(key) :
            return dict.__getitem__(self, key)
        else :
            return self.default
