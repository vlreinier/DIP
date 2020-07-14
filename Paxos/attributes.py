class GlobalVariables():
    network = None
    proposers = None
    acceptors = None
    n_proposers = None
    n_acceptors = None
    proposer_n = 0
    msg_types = ["PROPOSE",
            "PREPARE",
            "PROMISE",
            "ACCEPT",
            "ACCEPTED",
            "REJECTED",
            "SUCCES",
            "PREDICTED"]