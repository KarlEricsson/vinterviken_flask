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
    listeners: list[queue.Queue] = []

    def new_listener(self, request_addr):
        request_addr = request_addr
        q = queue.Queue(maxsize=1)
        self.listeners.append(q)
        q.put({"addr": request_addr, "msg": Court.updated_time})
        return q

    def update_listeners(self, update_time, request_addr):
        request_addr = request_addr
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait({"addr": request_addr, "msg": update_time})
            except queue.Full:
                del self.listeners[i]



