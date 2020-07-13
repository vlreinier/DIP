class Network():

    def __init__(self):
        self.queue = []

    def add_msg(self, msg):
        self.queue.append(msg)
        return None

    def get_msg(self):
        for msg in self.queue:
            if not msg.source.failed and not msg.destination.failed:
                return self.queue.pop(self.queue.index(msg))
        return None

