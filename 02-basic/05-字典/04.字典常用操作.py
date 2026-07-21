sts = dict(name='张三', age=18)
print(sts)

# 添加
sts['friends'] = ['李四', '王五', '赵六']
print(sts)

# 删除
sts.pop('friends')
print(sts)

# 修改
sts['name'] = '李四'
print(sts)

# 查询
print(sts.get('friends', '测试不存在'))