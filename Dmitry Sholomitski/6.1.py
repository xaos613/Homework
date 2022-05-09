
class Counter():

    def __init__(self, start=0, stop=-1):
        self.start = start
        self.stop = stop

    def increment(self):

        if self.start <= self.stop:
            self.start += 1
        else:
            print("Maximal value is reached.")


    def get(self):
        print(self.start)


c = Counter(start=42)
c.increment()
c.get()


c = Counter()
c.increment()
c.get()

c.increment()
c.get()


c = Counter(start=42, stop=43)
c.increment()
c.get()

c.increment()
c.increment()
c.increment()
c.increment()


c.get()