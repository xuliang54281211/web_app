#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 定义Field(定义域：元类遇到Field的方法或属性时即进行修改）
class Field(object):

    def __init__(self, name, column_type):  # column==>列类型
        self.name = name
        self.column_type = column_type

    # 当用print打印输出的时候，python会调用他的str方法
    # 在这里是输出<类的名字，实例的name参数(定义实例时输入)>
    # 在ModelMetaclass中会用到
    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self. name)  # __class__获取对象的类，__name__取得类名


class StringField(Field):

    def __init__(self, name):
        # super(type[, object-or-type])  返回type的父类对象
        # super().__init()的作用是调用父类的init函数
        # varchar(100)和bigint都是sql中的一些数据类型
        super(StringField, self).__init__(name, "varchar(100)")  

class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, "bigint")

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print("Found model:%s" % name)
        mappings = dict()
        print("items =",attrs.items())
        for k, v in attrs.items():
            if isinstance(v, Field):
                print("Found mappings:%s ==> %s" % (k, v))  # 找到映射， 这里用到上面的__str__
                mappings[k] = v
        for k in mappings.keys():
                print('pop', k)
                attrs.pop(k)
        attrs["__mappings__"] = mappings
        attrs["__table__"] = name # 添加表名，假设表名与类名一致
        attrs["hello"] = "xuliang"
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,  **kw):
        # 调用父类，即dict的初始化方法
        super(Model, self).__init__(**kw)

    # 让获取key的值不仅仅可以d[k]，也可以d.k
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 允许动态设置key的值，不仅仅可以d[k]，也可以d.k
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        # 在所有映射中迭代
        for k, v in self.__mappings__.items():
            print("k=",k,"v=", v.name)
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) values (%s)" % (self.__table__, ",".join(fields), str(args))
        print("SQL: %s" % sql)
# 这样一个简单的ORM就写完了


# 下面实际操作一下，先定义个User类来对应数据库的表User
class Users(Model):
    # 定义类的属性到列的映射
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")
    print("HHHHHHHHHHHHHHHHHH")


# 创建一个实例
u = Users(id=12345, name="ReedSun", email="sunhongzhao@foxmail.com", password="nicaicai", hello = "xuliang")
u.save()
print(u.__mappings__["id"])
