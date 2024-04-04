class IterableClass:
    def __iter__(self):
        for k in self.__dict__:
            yield self[k]

    def __getitem__(self, key):
        return getattr(self, key)
