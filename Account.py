class Account:
    def __init__(self, acctName, value=100, isPorter=False):
        self.id = acctName
        self.value = value
        self.isPorter = isPorter

    def deductValue(self, amount):
        self.value = self.value - amount

    def addValue(self, amount):
        self.value = self.value + amount

    def __hash__(self):
        return hash((self.id, str(self.value)))
