class Proposer():
    
    def __init__(self, id, network):
        self.id = id
        self.network = network
        self.failed = False

    def __str__(self):
        return f"P{self.id}"

class Acceptor():

    def __init__(self, id, network):
        self.id = id
        self.network = network
        self.failed = False

    def __str__(self):
        return f"A{self.id}"