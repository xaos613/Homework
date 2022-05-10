"""
Create hierarchy out of birds. Implement 4 classes:

class Bird with an attribute name and methods fly and walk.
class FlyingBird with attributes name, ration, and with the
same methods. ration must have default value. Implement the
method eat which will describe its typical ration.
class NonFlyingBird with same characteristics but which obviously
without attribute fly. Add same "eat" method but with other
implementation regarding the swimming bird tastes.
class SuperBird which can do all of it: walk, fly, swim and eat.
But be careful which "eat" method you inherit.
"""


class Bird:
    def __init__(self, name, ration='grains'):
        self.name = name
        self.ration = ration

    def fly(self):
        print(f'{self.name} bird can fly')

    def walk(self):
        print(f'{self.name} bird can walk')

    def eat(self):
        print(f"It eats mostly {self.ration}")


class FlyingBird(Bird):
    def __init__(self, name, ration="grains"):
        super().__init__(name)
        self.ration = ration

    def __str__(self):
        return str(f"{self.name} can walk and fly")


class NonFlyingBird(Bird):

    def __init__(self, name, ration="fish"):
        super().__init__(name, ration)

    def swim(self):
        print(f'{self.name} bird can swim')

    def fly(self):
        print("AttributeError: 'Penguin' object has no attribute 'fly'")


def __str__(self):
    return str(f"{self.name} can walk and swim.")


class SuperBird(NonFlyingBird, FlyingBird):

    def __init__(self, name, ration="fish"):
        super().__init__(name, ration)

    def __str__(self):
        return str(f"{self.name} can walk, fly and swim")

    def eat(self):
        print(f"{self.name} bird eats mostly {self.ration}")


b = Bird("Any")
b.walk()
print("Any bird can walk---")

p = NonFlyingBird("Penguin", "fish")
p.swim()
print("Penguin bird can swim---")
p.fly()
print("AttributeError: 'Penguin' object has no attribute 'fly'")
p.eat()
print("It eats mostly fish--")

c = FlyingBird("Canary")
print(str(c))
print("Canary can walk and fly---")
c.eat()
print("It eats mostly grains---")

s = SuperBird("Gull")
g = SuperBird("Gull")
print(str(s))
# print("Gull bird can walk, swim and fly-----")
print("It eats fish")

print(SuperBird.__mro__)
