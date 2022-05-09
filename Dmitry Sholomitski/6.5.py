class Sun:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sun, cls).__new__(cls)
        return cls._instance
    def inst(cls):
        return 'class'

p = Sun()
f = Sun()
print(p is f)


print(p.inst() is f.inst())