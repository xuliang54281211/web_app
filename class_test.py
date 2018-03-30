#!/usr/bin/env python3
# -*- coding: gbk -*-
import asyncio, logging

import aiomysql

class field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
        print("%s:%s" % (self.name , self.column_type))
    def __str__(self):
        return "<%s:%s:%s>" % (self.__class__.__name__, self.name, self.column_type)

class StringField(field):
    def __init__(self, name):
        super().__init__(name, "varchar(100)")
class IntegerField(field):
    def __init__(self, name):
        super().__init__(name, "bigint")

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print("name = %s!" % name)
        return type.__new__(cls, name, bases, attrs)
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super().__init__(self, **kw)

class User(Model):
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")
  
  
c = u = User(id=12345, name="ReedSun", email="sunhongzhao@foxmail.com", password="nicaicai")
print(c[name])
