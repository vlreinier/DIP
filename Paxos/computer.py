class Computer(object):
    def __init__(self, number, network, failed=False):
        self.number = number
        self.failed = failed
        self.network = network
        self.acceptors = []
        self.proposers = []

class Proposer(Computer):
    ...

class Acceptor(Computer):
    ...
