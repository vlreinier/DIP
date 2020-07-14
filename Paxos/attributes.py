class GlobalVariables():
    network = None
    proposers = []
    acceptors = []
    n_proposers = None
    n_acceptors = None
    proposal_n = 0
    msg_types = ["PROPOSE",
            "PREPARE",
            "PROMISE",
            "ACCEPT",
            "ACCEPTED",
            "REJECTED",
            "SUCCES",
            "PREDICTED"]

    @staticmethod
    def next_proposal_n():
        GlobalVariables.proposal_n += 1
        return GlobalVariables.proposal_n