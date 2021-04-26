class Account:
    def __init__(self, id, value=100, isPorter=False):
        self.id = id
        self.value = value
        self.isPorter = isPorter

    def __hash__(self):
        return hash((self.id, str(self.value)))
