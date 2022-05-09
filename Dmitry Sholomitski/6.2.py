from collections import deque


class HistoryDict:

    def __init__(self, start_value):
        self.queue = deque(maxlen=10)
        self.hist_Dict = dict()
        hist_Dict = ({**start_value})
        print(hist_Dict)

    def set_value(self, *value):
        self.queue.append(value[0])
        self.hist_Dict[value[0]] = value[1]

    def get_history(self):
        print(list(self.queue))


d = HistoryDict({"foo": 42})
for x in range(16):
    d.set_value(str(x), x)

d.get_history()
