class A:
    def ping(self):
        print('A')

class B:
    def pong(self):
        print('B')

class C(A, B):  # 多继承
    pass

c = C()
c.ping()  # A
c.pong()  # B


# 方法查找顺序由 MRO（Method Resolution Order） 决定，可用 C.__mro__ 或 C.mro() 查看。
# 同名方法冲突时，按 MRO 从左到右找，先找到的先用。