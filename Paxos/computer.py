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
            self.accepted_value = self.proposed_value
            next_proposal_n = GlobalVariables.next_proposal_n()
            for acceptor in GlobalVariables.acceptors:
                msg = Message(self, acceptor, "PREPARE", value=self.proposed_value, n=next_proposal_n)
                GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "PROMISE":
            if msg.src.acceptedN != 0:
                self.accepted_value = msg.src.acceptedValue
            msg = Message(self, msg.src, "ACCEPT", value=self.accepted_value, n=msg.n)
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
        self.acceptedN = 0
        self.acceptedValue = None

    def deliver_msg(self, msg):

        if msg.mtype == "PREPARE":
            if self.acceptedN < msg.n:
                msg = Message(self, msg.src, "PROMISE", value=msg.value, n=msg.n)
                GlobalVariables.network.add_msg(msg)
                
        elif msg.mtype == "ACCEPT":
            if self.acceptedN < msg.n:
                self.acceptedValue = msg.value
                self.acceptedN = msg.n
                msg = Message(self, msg.src, "ACCEPTED", value=self.acceptedValue, n=self.acceptedN)
                GlobalVariables.network.add_msg(msg)
            else:
                msg = Message(self, msg.src, "REJECTED", value=None, n=msg.n)
                GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"A{self.id}"