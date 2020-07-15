class GlobalVariables():
    network = None
    proposers = []
    acceptors = []
    learners = []
    n_proposers = None
    n_acceptors = None
    n_learners = None
    n = 0
    msg_types = ["PROPOSE",
                "PREPARE",
                "PROMISE",
                "ACCEPT",
                "ACCEPTED",
                "REJECTED",
                "SUCCES",
                "PREDICTED"]