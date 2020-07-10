import sys

class Message(object):

    messages = ["PROPOSE","PREPARE","PROMISE","ACCEPT","ACCEPTED","REJECTED","SUCCES","PREDICTED"]

    def __init__(self, source, destination, message, n=None, v=None, prior=None)

        if not message in messages:
            print("Unvalid message type was provided")
            sys.exit(0)

        self.source = source
        self.destination = destination
        self.message = message
        self.n = n
        self.v = v
        self.prior = prior

    