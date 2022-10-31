class File:
    """FIFO data structure"""

    def __init__(self):
        self.input = []
        self.output = []

    def add(self, elem):
        self.input.append(elem)

    def add_list(self, l):
        for elem in l:
            self.add(elem)

    def pop(self):
        if self.is_empty():
            raise "No element to pop"
        elif len(self.output) == 0:
            for i in range(len(self.input)):
                self.output.append(self.input.pop())
            return self.output.pop()
        else:
            return self.output.pop()

    def is_empty(self):
        return len(self.input) + len(self.output) == 0
