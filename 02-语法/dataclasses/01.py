from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

u = User("Ada", 30)
print(u)                 # User(name='Ada', age=30)
print(u == User("Ada", 30))  # True