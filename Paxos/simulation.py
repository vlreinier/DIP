from network import Network
from computer import Proposer, Acceptor
from message import Message
import sys

class Simulation(object):

    def __init__(self, input):
        self.network = Network()
        self.n_P, self.n_A, self.tickmax, events = self.read_input(input)
        self.P = [Proposer(i + 1, self.network) for i in range(self.n_P)]
        self.A = [Acceptor(i + 1, self.network) for i in range(self.n_A)]
        self.E = self.parse_events(events)

    def run(self):

        # first event
        event_incrementer = 0
        t_event, F, R, pi_v, pi_c = self.E[event_incrementer]

        # simulation
        for tick in range(self.tickmax):

            print(event_incrementer, len(self.E))
            
            # simulation ended
            if len(self.network.queue) == 0 and (event_incrementer >= len(self.E)):
                # consensus print
                sys.exit(0)

            # event tick is equal to current tick
            if t_event == tick:

                # fail computers
                for c in F:
                    c.failed = True

                # recover computers
                for c in R:
                    c.failed = False
                
                # propose message
                if pi_v != None and pi_c != None:
                    msg = Message(None, pi_c, "PROPOSE", pi_v)
                    msg.dst.deliver_msg(msg)

                # get next event
                event_incrementer += 1
                t_event, F, R, pi_v, pi_c = self.E[event_incrementer]
            
            else:
                msg = self.network.get_msg()
                if msg != None:
                    msg.dst.deliver_msg(msg)

    def read_input(self, input):
        reader = open(input, "r")
        str_input = reader.readlines()
        parsed_input = [i.strip("\n").split(" ") for i in str_input]

        proposers = int(parsed_input[0][0])
        acceptors = int(parsed_input[0][1])
        tickmax = int(parsed_input[0][2])
        events = parsed_input[1:-1]

        return proposers, acceptors, tickmax, events

    def parse_events(self, events):
        
        parsed = []

        for e in events:
            tick = int(e[0])
            F, R = [], []
            pi_v, pi_c = None, None

            if e[1] == 'PROPOSE':
                pi_c = self.P[int(e[2]) - 1]
                pi_v = e[3]

            elif e[1] == 'FAIL':
                if e[2] == 'PROPOSER':
                    F.append(self.P[int(e[3]) - 1])
                elif e[2] == 'ACCEPTOR':
                    F.append(self.A[int(e[3]) - 1])
                else:
                    print("Unvalid target type was found in input")
                    sys.exit(0)

            elif e[1] == 'RECOVER':
                if e[2] == 'PROPOSER':
                    R.append(self.P[int(e[3]) - 1])
                elif e[2] == 'ACCEPTOR':
                    R.append(self.A[int(e[3]) - 1])
                else:
                    print("Unvalid target type was found in input")
                    sys.exit(0)
            else:
                print("Unvalid message type was found in input")
                sys.exit(0)
            
            parsed.append([tick, F, R, pi_v, pi_c])

        return parsed



