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
            GlobalVariables.proposer_n += 1
            for acceptor in GlobalVariables.acceptors: # always send prepare to all acceptors
                msg = Message(self, acceptor, "PREPARE", value=None, n=GlobalVariables.proposer_n)
                GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "PROMISE":
            if msg.value:
                self.accepted_value = msg.prior[1]
            msg = Message(self, msg.src, "ACCEPT", value=self.accepted_value, n=msg.n)
            GlobalVariables.network.add_msg(msg)

        elif msg.mtype == "ACCEPTED":
            self.accepted += 1
            if self.accepted > (GlobalVariables.n_acceptors // 2): # majority accepted and consensus is true
                self.has_consensus = True

        elif msg.mtype == "REJECTED":
            self.rejected += 1
            if self.rejected > (GlobalVariables.n_acceptors // 2): # majority rejected 
                GlobalVariables.proposer_n += 1
                for acceptor in GlobalVariables.acceptors: # always send prepare to all acceptors
                    msg = Message(self, acceptor, "PREPARE", value=None, n=GlobalVariables.proposer_n)
                    GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"P{self.id}"

class Acceptor():

    def __init__(self, id):
        self.id = id
        self.failed = False
        self.min_n = 0
        self.accepted_value = None

    def deliver_msg(self, msg):

        if msg.mtype == "PREPARE":
            if msg.n > self.min_n:
                msg = Message(self, msg.src, "PROMISE", value=msg.value, n=msg.n)
                GlobalVariables.network.add_msg(msg)
                
        elif msg.mtype == "ACCEPT":
            if msg.n > self.min_n:
                self.min_n = msg.n
                self.accepted_value = msg.value
                msg = Message(self, msg.src, "ACCEPTED", value=msg.value, n=msg.n)
                GlobalVariables.network.add_msg(msg)
            else:
                msg = Message(self, msg.src, "REJECTED", value=None, n=msg.n)
                GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"A{self.id}"