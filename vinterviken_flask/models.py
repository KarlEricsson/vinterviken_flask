import queue


class Court:
    updated_time = "Not updated since server restart."

    def __init__(self, name) -> None:
        self.name = name
        self.available = True
        self.booked = False
        self.booked2h = False

    def update_time(self, time):
        Court.updated_time = time

    #def get_update_time(self):
    #    return Court.update_time()

class MessengerQueue:
    listeners = []

    def new_listener(self):
        q = queue.Queue(maxsize=2)
        self.listeners.append(q)
        q.put(Court.updated_time)
        return q

    def update_listeners(self, update_time):
        for listener in self.listeners:
            listener.put(update_time)


