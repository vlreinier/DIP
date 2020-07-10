from network import Network

class Simulation(object):

    def __init__(self, n_p, n_a, tmax, E):
        self.network = Network()
        self.P = [Proposer(i + 1, self.network) for i in range(n_p)]
        self.A = [Acceptor(i + 1, self.network) for i in range(n_a)]
        self.tmax = tmax
        self.E = E

    def run(self):

        for t in range(self.tmax):
            ...