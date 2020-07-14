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
            self.accepted_value = msg.value
            self.proposed_value = self.accepted_value
            GlobalVariables.proposer_n += 1
            for acceptor in GlobalVariables.acceptors: # always send prepare to all acceptors
                msg = Message(self, acceptor, "PREPARE", n=GlobalVariables.proposer_n)
                GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "PROMISE":
            if msg.prior:
                self.accepted_value = msg.prior[1]
            msg = Message(self, msg.src, "ACCEPT", value=self.accepted_value, n=msg.n)
            GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "ACCEPTED" and not self.has_consensus:
            self.accepted += 1
            if self.accepted > (GlobalVariables.n_acceptors // 2): # majority
                self.has_consensus = True

        elif msg.mtype == "REJECTED":
            self.rejected += 1
            if self.rejected > (GlobalVariables.n_acceptors // 2): # majority
                GlobalVariables.proposer_n += 1
                for acceptor in GlobalVariables.acceptors: # always send prepare to all acceptors
                    msg = Message(self, acceptor, "PREPARE", n=GlobalVariables.proposer_n)
                    GlobalVariables.network.add_msg(msg)
                self.accepted, self.rejected = 0, 0

    def __str__(self):
        return f"P{self.id}"

class Acceptor():

    def __init__(self, id):
        self.id = id
        self.failed = False
        self.prior = (0, None)

    def deliver_msg(self, msg):

        if msg.mtype == "PREPARE":
            if self.prior[0] < msg.n:
                if self.prior[1]:
                    msg = Message(self, msg.src, "PROMISE", n=msg.n, prior=self.prior)
                    GlobalVariables.network.add_msg(msg)
                else:
                    msg = Message(self, msg.src, "PROMISE", n=msg.n)
                    GlobalVariables.network.add_msg(msg)
                
        elif msg.mtype == "ACCEPT":
            if self.prior[0] < msg.n:
                msg = Message(self, msg.src, "ACCEPTED", value=msg.value, n=msg.n)
                GlobalVariables.network.add_msg(msg)
                self.prior = (msg.n, msg.value)
            else:
                msg = Message(self, msg.src, "REJECTED", n=msg.n)
                GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"A{self.id}"