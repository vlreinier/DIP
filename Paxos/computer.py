class Computer(object):
    def __init__(self, id, network, failed=False):
        self.id = id
        self.failed = failed
        self.network = network

    def deliver_msg(self):
        ...


class Proposer(Computer):
    ...

class Acceptor(Computer):
    ...
