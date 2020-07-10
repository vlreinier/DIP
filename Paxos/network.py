class Network(object):

    def __init__(self):
        self.queue = []

    def add_message_to_queue(self, message):
        self.queue.append(message)

    def get_message_from_queue(self):
        for message in self.queue:
            if message.source.failed == False and message.destination.failed == False:
                return self.queue.pop(self.queue.index(message))

    def is_empty(self):
        return len(self.queue) == 0

