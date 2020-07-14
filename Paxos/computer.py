from message import Message
from attributes import GlobalVariables

class Proposer():
    
    def __init__(self, id):
        self.id = id
        self.failed = False
        self.has_consensus = False
        self.proposed_value, self.accepted_value = None, None
        self.rejected, self.accepted = 0, 0

    def deliver_msg(self, msg):

        if msg.mtype == "PROPOSE":
            self.proposed_value = msg.value
            next_proposal_n = GlobalVariables.next_proposal_n()
            for acceptor in GlobalVariables.acceptors:
                msg = Message(self, acceptor, "PREPARE", value=None, n=next_proposal_n)
                GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "PROMISE":
            if msg.src.acceptedValue != None:
                for acceptor in GlobalVariables.acceptors:
                    msg = Message(self, acceptor, "ACCEPT", value=self.proposed_value, n=msg.n)
                    GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "ACCEPTED":
            self.accepted += 1
            if self.accepted > (GlobalVariables.n_acceptors // 2): # majority accepted and consensus is true
                self.has_consensus = True

        elif msg.mtype == "REJECTED":
            self.rejected += 1
            if self.rejected > (GlobalVariables.n_acceptors // 2): # majority rejected 
                next_proposal_n = GlobalVariables.next_proposal_n()
                for acceptor in GlobalVariables.acceptors:
                    msg = Message(self, acceptor, "PREPARE", value=None, n=next_proposal_n)
                    GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"P{self.id}"

class Acceptor():

    def __init__(self, id):
        self.id = id
        self.failed = False
        self.minProposal = 0
        self.acceptedProposal = None
        self.acceptedValue = None

    def deliver_msg(self, msg):

        if msg.mtype == "PREPARE":
            if msg.n > self.minProposal:
                self.minProposal = msg.n
                msg = Message(self, msg.src, "PROMISE", value=self.acceptedValue, n=self.acceptedProposal)
                GlobalVariables.network.add_msg(msg)
                
        elif msg.mtype == "ACCEPT":
            if msg.n >= self.minProposal:
                self.acceptedValue = msg.value
                self.acceptedProposal = self.minProposal
                msg = Message(self, msg.src, "ACCEPTED", value=msg.value, n=msg.n)
                GlobalVariables.network.add_msg(msg)
            else:
                msg = Message(self, msg.src, "REJECTED", value=None, n=msg.n)
                GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"A{self.id}"