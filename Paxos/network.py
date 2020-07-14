class Network():

    def __init__(self):
        self.queue = []

    def add_msg(self, msg):
        self.queue.append(msg)
        return None

    def get_msg(self):
        for msg in self.queue:
            if not msg.src.failed and not msg.dst.failed:
                return self.queue.pop(self.queue.index(msg))
        return None

