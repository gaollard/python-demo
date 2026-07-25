# dataclasses

`dataclasses` 用装饰器自动生成 `__init__`、`__repr__`、`__eq__` 等样板代码，适合「主要用来存数据」的类。Python 3.7+ 标准库自带。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| `@dataclass` | 根据类型注解字段，自动生成常用方法 | `@dataclass class User: ...` |
| 字段（field） | 类体里带类型注解的属性 | `name: str`、`age: int = 0` |
| `field()` | 精细控制单个字段的默认值、是否参与比较等 | `field(default_factory=list)` |
| `__post_init__` | `__init__` 之后自动调用的钩子 | 校验、派生字段 |

关系可以记成：

```
类型注解字段
    │
    ▼
@dataclass 扫描字段
    │
    ▼
自动生成 __init__ / __repr__ / __eq__ ...
    │
    ▼
可选：__post_init__ 做校验或二次计算
```

## 为什么需要 dataclass

手写数据类会重复很多样板：

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return (self.name, self.age) == (other.name, other.age)
```

用 `@dataclass` 等价且更短：

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

u = User("Ada", 30)
print(u)                 # User(name='Ada', age=30)
print(u == User("Ada", 30))  # True
```

## 基本用法

字段必须有**类型注解**，`@dataclass` 才认作字段：

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"   # 有默认值的字段必须排在无默认值字段后面

p = Point(1.0, 2.0)
print(p.x, p.label)      # 1.0 origin
print(Point(3, 4, "A"))  # Point(x=3, y=4, label='A')
```

注意：

```python
@dataclass
class Bad:
    # z = 1              # 没有类型注解 → 不是字段，不会进 __init__
    name: str
    # age = 18           # 同样不是字段
```

## 装饰器常用参数

```python
from dataclasses import dataclass

@dataclass(
    init=True,       # 生成 __init__
    repr=True,       # 生成 __repr__
    eq=True,         # 生成 __eq__
    order=False,     # True 时生成 < <= > >=（需 eq=True）
    unsafe_hash=False,
    frozen=False,    # True 时实例只读（近似不可变）
    match_args=True, # 3.10+：支持结构模式匹配
    kw_only=False,   # 3.10+：字段默认只能关键字传参
    slots=False,     # 3.10+：使用 __slots__，省内存、禁动态属性
)
class Demo:
    value: int
```

### `frozen=True`：只读

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080

c = Config("localhost")
# c.port = 9000          # FrozenInstanceError
print(c.host)            # localhost
```

`frozen` 适合配置、值对象；需要改某个字段时用 `replace`（见下文）。

### `order=True`：可排序

```python
from dataclasses import dataclass

@dataclass(order=True)
class Student:
    score: int
    name: str

students = [Student(90, "Bob"), Student(95, "Ada"), Student(90, "Ann")]
print(sorted(students))
# [Student(score=90, name='Ann'), Student(score=90, name='Bob'), Student(score=95, name='Ada')]
```

比较按字段定义顺序逐个比。若只想按部分字段排序，可用 `field(compare=False)` 排除其它字段。

### `slots=True`（3.10+）

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Item:
    id: int
    name: str

item = Item(1, "pen")
# item.extra = 1         # AttributeError：不能动态加属性
```

## 默认值与可变默认值陷阱

和函数默认参数一样，**可变对象不能直接当类级默认值**：

```python
from dataclasses import dataclass, field

# 错误示范：所有实例会共享同一个 list
# @dataclass
# class Team:
#     members: list[str] = []

@dataclass
class Team:
    members: list[str] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)

a = Team()
b = Team()
a.members.append("Ada")
print(a.members)         # ['Ada']
print(b.members)         # []  —— 互不影响
```

| 写法 | 适用 |
|---|---|
| `x: int = 0` | 不可变默认值（int/str/tuple/None…） |
| `field(default=...)` | 与上面类似，可附加更多选项 |
| `field(default_factory=list)` | list/dict/set 等可变默认值 |

## `field()` 精细控制

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    # 不参与 __init__，在 __post_init__ 或别处赋值
    sku: str = field(init=False)
    # 不出现在 __repr__
    secret: str = field(default="", repr=False)
    # 不参与 == / 排序
    note: str = field(default="", compare=False)
    # 仅关键字传参（3.10+ 也可用装饰器 kw_only=True）
    meta: dict = field(default_factory=dict, kw_only=True)

    def __post_init__(self):
        self.sku = self.name.upper().replace(" ", "-")

p = Product("green tea", 12.5, meta={"origin": "CN"})
print(p)                 # Product(name='green tea', price=12.5, sku='GREEN-TEA', meta={...})
# secret 被 repr=False 隐藏
```

常用 `field` 参数：

| 参数 | 作用 |
|---|---|
| `default` | 默认值 |
| `default_factory` | 无参工厂，每次新建实例调用 |
| `init` | 是否进入 `__init__` |
| `repr` | 是否出现在 `__repr__` |
| `compare` | 是否参与 `==` / 排序 |
| `hash` | 是否参与哈希（常与 `frozen` 配合） |
| `kw_only` | 该字段是否仅关键字传参 |

## `__post_init__`

在自动生成的 `__init__` 末尾调用，适合校验和派生字段：

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("宽高必须为正")
        self.area = self.width * self.height

r = Rectangle(3, 4)
print(r.area)            # 12.0
```

若同时使用 `InitVar`（只传给 `__post_init__`、不当实例属性）：

```python
from dataclasses import dataclass, InitVar, field

@dataclass
class Database:
    path: str
    connect: InitVar[bool] = True
    conn: object = field(init=False, default=None)

    def __post_init__(self, connect: bool):
        if connect:
            self.conn = f"connected:{self.path}"

db = Database("/tmp/app.db")
print(db.conn)           # connected:/tmp/app.db
# db.connect             # AttributeError：InitVar 不是实例属性
```

## 转换与拷贝：`asdict` / `astuple` / `replace`

```python
from dataclasses import dataclass, asdict, astuple, replace

@dataclass
class Address:
    city: str
    zip_code: str

@dataclass
class Person:
    name: str
    address: Address

p = Person("Ada", Address("Shanghai", "200000"))

print(asdict(p))
# {'name': 'Ada', 'address': {'city': 'Shanghai', 'zip_code': '200000'}}

print(astuple(p))
# ('Ada', ('Shanghai', '200000'))

p2 = replace(p, name="Bob")
print(p2)                # Person(name='Bob', address=Address(...))
print(p.name)            # Ada —— 原对象不变
```

`asdict` / `astuple` 会**递归**处理嵌套 dataclass，适合序列化前的中间结构；深层可变对象仍是浅层共享，需要独立副本时要自己处理。

## 继承

子类会合并父类字段，再追加自己的字段：

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str

@dataclass
class Dog(Animal):
    breed: str

d = Dog("Buddy", "Beagle")
print(d)                 # Dog(name='Buddy', breed='Beagle')
```

注意默认值规则仍然成立：父类若有带默认值的字段，子类新增的无默认值字段会出问题。更稳妥的做法是父类字段都带默认值，或子类字段也都带默认值。

## 与其它「数据容器」对比

| | `@dataclass` | `NamedTuple` | 普通 class | `TypedDict` |
|---|---|---|---|---|
| 可变性 | 默认可变；`frozen=True` 只读 | 不可变 | 自定 | 本质是 dict |
| 方法 | 可随意加 | 可加，但较少用 | 随意 | 无实例方法 |
| 默认值 | 支持 | 支持（较新版本） | 支持 | 有限 |
| 类型检查 | 字段注解 | 字段注解 | 自定 | 键的注解 |
| 典型场景 | 业务模型、DTO、配置 | 轻量不可变记录 | 有复杂行为的对象 | JSON/API 字典形状 |

经验法则：

- **主要是数据 + 少量方法** → `dataclass`
- **固定字段、要当 tuple 用、要可哈希** → `NamedTuple` 或 `frozen` dataclass
- **就是字典结构、要和 JSON 对齐** → `TypedDict`
- **行为很多、状态复杂** → 普通 class

## 对比小结

| | 手写 class | `@dataclass` | `@dataclass(frozen=True)` |
|---|---|---|---|
| 样板代码 | 多 | 少 | 少 |
| 可变性 | 默认可变 | 默认可变 | 近似不可变 |
| 自动 `__repr__`/`__eq__` | 需手写 | 有 | 有 |
| 可变默认值 | 易踩坑 | 用 `default_factory` | 同左 |
| 适合 | 复杂行为 | 数据为主的模型 | 配置、值对象 |

## 实践建议

1. **数据为主就用 `@dataclass`**，别为了「看起来正式」手写一堆 `__init__`/`__repr__`。
2. **可变默认值一律 `default_factory`**，不要写 `= []` / `= {}`。
3. **配置、作为 dict key 的对象优先 `frozen=True`**，改字段用 `replace`。
4. **校验和派生字段放 `__post_init__`**，保持字段声明干净。
5. **不要滥用**：逻辑很重、生命周期复杂的对象，普通 class 往往更清晰。
6. **序列化**：`asdict` 只是转 dict；真正落盘/出网仍需配合 `json` 等，并注意 datetime 等不可直接 JSON 化的类型。
