from network import Network
from computer import Proposer, Acceptor
from message import Message
from attributes import GlobalVariables
import sys

class Simulation():

    def __init__(self, input):
        GlobalVariables.network = Network()
        GlobalVariables.n_proposers, GlobalVariables.n_acceptors, self.tickmax, events = self.read_input(input)
        GlobalVariables.proposers = [Proposer(i + 1) for i in range(GlobalVariables.n_proposers)]
        GlobalVariables.acceptors = [Acceptor(i + 1) for i in range(GlobalVariables.n_acceptors)]
        self.E = self.parse_events(events)

    def run(self):

        # simulation
        event_incrementer = 0
        for tick in range(self.tickmax):
            
            # simulation ended
            if len(GlobalVariables.network.queue) == 0 and (event_incrementer >= len(self.E)):
                for proposer in GlobalVariables.proposers:
                    if proposer.has_consensus:
                        print(f"{proposer} heeft wel consensus (voorgesteld: {proposer.proposed_value}, geaccepteerd: {proposer.accepted_value})")
                    else:
                        print(f"{proposer} heeft geen consensus.")
                sys.exit(0)

            # get event data
            if event_incrementer < len(self.E):
                t_event, F, R, pi_v, pi_c = self.E[event_incrementer]

            # event tick is equal to current tick
            if t_event == tick:

                # fail computers
                for c in F:
                    print(f"{tick}: ** {c} kapot **")
                    c.failed = True

                # recover computers
                for c in R:
                    print(f"{tick}: ** {c} gerepareerd **")
                    c.failed = False
                
                # propose message to provided machine
                if pi_v != None and pi_c != None:
                    msg = Message(None, pi_c, "PROPOSE", value=pi_v, n=None)
                    msg.dst.deliver_msg(msg)
                    print(f"{tick}:  -> {pi_c} {msg}")

                # get next event
                event_incrementer += 1
            
            else:
                msg = GlobalVariables.network.get_msg()
                if msg != None:
                    msg.dst.deliver_msg(msg)
                    print(f"{tick}: {msg.src} -> {msg.dst} {msg}")
                else:
                    print(f"{tick}:")

    def read_input(self, input):
        try:
            reader = open(input, "r")
            str_input = reader.readlines()
            parsed_input = [i.strip("\n").split(" ") for i in str_input]

            proposers = int(parsed_input[0][0])
            acceptors = int(parsed_input[0][1])
            tickmax = int(parsed_input[0][2])
            events = parsed_input[1:-1] # except first and last

            return proposers, acceptors, tickmax, events

        except:
            print("Input file could not be read")
            sys.exit(0)

    def parse_events(self, events):

        parsed = []
        for e in events:

            tick = int(e[0])
            F, R = [], []
            pi_v, pi_c = None, None

            if e[1] == 'PROPOSE':
                pi_c = GlobalVariables.proposers[int(e[2]) - 1]
                pi_v = e[3]

            elif e[1] == 'FAIL':
                if e[2] == 'PROPOSER':
                    F.append(GlobalVariables.proposers[int(e[3]) - 1])
                elif e[2] == 'ACCEPTOR':
                    F.append(GlobalVariables.acceptors[int(e[3]) - 1])
                else:
                    print("Unvalid target type was found in input")
                    sys.exit(0)

            elif e[1] == 'RECOVER':
                if e[2] == 'PROPOSER':
                    R.append(GlobalVariables.proposers[int(e[3]) - 1])
                elif e[2] == 'ACCEPTOR':
                    R.append(GlobalVariables.acceptors[int(e[3]) - 1])
                else:
                    print("Unvalid target type was found in input")
                    sys.exit(0)
            else:
                print("Unvalid message type was found in input")
                sys.exit(0)
            
            parsed.append([tick, F, R, pi_v, pi_c])

        return parsed



