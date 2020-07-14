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

    def __init__(self, src, dst, mtype, value=None, n=None, prior=None):
        self.src = src
        self.dst = dst
        self.mtype = mtype
        self.value = value
        self.n = n
        self.prior = prior

    def __str__(self):
        
        if self.mtype == "PROPOSE":
            return f"{self.mtype} v={self.value}"

        elif self.mtype in ["PREPARE", "REJECTED"]:
            return f"{self.mtype} n={self.n}" 

        elif self.mtype in ["ACCEPT", "ACCEPTED", "SUCCES"]:
            return f"{self.mtype} n={self.n} v={self.value}"

        elif self.mtype == "PROMISE":
            if self.prior:
                return f"{self.mtype} n={self.n} (Prior: n={self.prior[0]}, v={self.prior[1]})"
            else:
                return f"{self.mtype} n={self.n} (Prior: None)"

