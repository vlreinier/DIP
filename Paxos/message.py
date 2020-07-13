import sys

class Message(object):

    msg_types = ["PROPOSE",
                "PREPARE",
                "PROMISE",
                "ACCEPT",
                "ACCEPTED",
                "REJECTED",
                "SUCCES",
                "PREDICTED"]

    def __init__(self, src, dst, msg_type, n=None, v=None, prior=None):
        self.src = src
        self.dst = dst
        self.msg_type = msg_type
