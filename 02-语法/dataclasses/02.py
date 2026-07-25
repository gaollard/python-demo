from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"   # 有默认值的字段必须排在无默认值字段后面

p = Point(1.0, 2.0)
print(p.x, p.label)      # 1.0 origin
print(Point(3, 4, "A"))  # Point(x=3, y=4, label='A')
print(p == Point(3, 4, "A")) 