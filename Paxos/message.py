import sys
from attributes import GlobalVariables

class Message():

    def __init__(self, src, dst, mtype, value, n):

        if not mtype in GlobalVariables.msg_types:
            print("Invalid msg type")
            sys.exit(0)

        self.src = src
        self.dst = dst
        self.mtype = mtype
        self.value = value
        self.n = n

    def __str__(self):
        
        if self.mtype == "PROPOSE":
            return f"{self.mtype} v={self.value}"

        elif self.mtype in ["PREPARE", "REJECTED"]:
            return f"{self.mtype} n={self.n}" 

        elif self.mtype in ["ACCEPT", "ACCEPTED", "SUCCES"]:
            return f"{self.mtype} n={self.n} v={self.value}"

        elif self.mtype == "PROMISE":
            prior = f"n={self.src.acceptedN}, v={self.src.acceptedValue}" if self.src.acceptedN != 0 else "None"
            return f"{self.mtype} n={self.n} (Prior: {prior})"
        
        elif self.mtype == "PREDICTED":
            return f"{self.mtype} v={self.value}"

        elif self.mtype == "REJECTED":
            return f"{self.mtype} n={self.n}"

        else:
            print("Invalid msg type")
            sys.exit(0)

