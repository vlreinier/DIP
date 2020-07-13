import sys

class Message():

    msg_types = ["PROPOSE",
                "PREPARE",
                "PROMISE",
                "ACCEPT",
                "ACCEPTED",
                "REJECTED",
                "SUCCES",
                "PREDICTED"]

    def __init__(self, src, dst, msg_type, value=None, n=None, prior=None):
        self.src = src
        self.dst = dst
        self.msg_type = msg_type
        self.value = value
        self.n = n
        self.prior = prior

    def __str__(self):
        
        if self.msg_type == "PROPOSE":
            return f"v={self.value}"

        elif self.msg_type == "PREDICTED":
            return f"n={self.n}"

        else:
            
            if self.msg_type in ["ACCEPT", "ACCEPTED", "SUCCES"]:
                return f"n={self.n} v={self.value}"

            elif self.prior:
                return f" (Prior: n={self.prior[0]}, v={self.prior[1]})"

            else:
                return f" (Prior: None)"

