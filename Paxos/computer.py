from message import Message
from attributes import GlobalVariables
import flickbike

class Proposer():
    
    def __init__(self, id):
        self.id = id
        self.failed = False
        self.hasConsensus = False
        self.proposedValue, self.acceptedValue = None, None
        self.rejected, self.accepted = 0, 0

    def deliver_msg(self, msg):

        # proposal for new value with a new n
        if msg.mtype == "PROPOSE":
            self.proposedValue = msg.value
            self.acceptedValue = self.proposedValue
            GlobalVariables.n += 1
            for acceptor in GlobalVariables.acceptors:
                msg = Message(self, acceptor, "PREPARE", value=None, n=GlobalVariables.n)
                GlobalVariables.network.add_msg(msg)

        # if promise returns with new accepted n, set accepted value from this acceptor
        elif msg.mtype == "PROMISE":
            if msg.src.acceptedN != 0:
                self.acceptedValue = msg.src.acceptedValue
            msg = Message(self, msg.src, "ACCEPT", value=self.acceptedValue, n=msg.n)
            GlobalVariables.network.add_msg(msg)

        # if majority accepted, consensus is true for current accepted value
        elif msg.mtype == "ACCEPTED":
            self.accepted += 1
            if self.accepted > (GlobalVariables.n_acceptors // 2):
                self.hasConsensus = True
                for learner in GlobalVariables.learners:
                    msg = Message(self, learner, "SUCCES", value=msg.value, n=msg.n)
                    GlobalVariables.network.add_msg(msg)

        # if majority rejected n, start over with a higher n
        elif msg.mtype == "REJECTED":
            self.rejected += 1
            if self.rejected > (GlobalVariables.n_acceptors // 2):
                GlobalVariables.n += 1
                for acceptor in GlobalVariables.acceptors:
                    msg = Message(self, acceptor, "PREPARE", value=None, n=GlobalVariables.n)
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
                msg = Message(self, msg.src, "PROMISE", value=None, n=msg.n)
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

class Learner():

    def __init__(self, id):
        self.id = id
        self.failed = False

    def deliver_msg(self, msg):

        if msg.mtype == "SUCCES":
            msg = Message(self, msg.src, "PREDICTED", value=flickbike.PredictValue(msg.value), n=None)
            GlobalVariables.network.add_msg(msg)

    def __str__(self):
        return f"A{self.id}"