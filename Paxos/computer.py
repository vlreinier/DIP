class Computer(object):
    def __init__(self, id, network, failed=False):
        self.id = id
        self.failed = failed
        self.network = network

    def deliver_msg(self, msg):
        ...

    def __str__(self):
        return f"{self.id}"

class Proposer(Computer):
    ...
    def __str__(self):
        return f"P{self.id}"

class Acceptor(Computer):
    ...
    def __str__(self):
        return f"A{self.id}"