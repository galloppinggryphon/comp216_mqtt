class sequence_gen:
    id: int

    def __init__(self, start_id: int):
        self.id = start_id

    def next(self):
        self.id += 1
        return self.id
