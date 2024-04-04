class Point:
    x: int
    y: int

    @property
    def as_tuple(self):
        return (self.x, self.y)

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __getitem__(self, key):
        if key == 0 or key == 1:
            key = ["x", "y"][key]
        return self.__dict__[key]

    def __iter__(self):
        for k in self.__dict__:
            yield self[k]

    def __repr__(self) -> str:
        return f"{self.as_tuple}"
