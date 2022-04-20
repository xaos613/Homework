import sys

from .skill_python import python
from .skill_c import c
from .skill_nim import nim
from .skill_linux import linux

print('#--------------')
print(sys.path)
print('#--------------')

def learn_all():
    python()
    c()
    nim()
    linux()

    
if __name__ == '__main__':
    learn_all()
