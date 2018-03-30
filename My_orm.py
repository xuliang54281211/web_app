#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class field(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "<%s:%s>" %(self.__class__.__name__, self.name)

class StringField(field):
    def __init__(self, name):
        super().__init__(name, "varchar100")

class IntegerField(field):
    def __init__(self, name):
        super().__init__(name, "bigint")

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, field):
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs["__mappings__"] = mappings
        attrs["__table__"] = name
        return type.__new__(cls,name,bases,attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super().__init__(self, **kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            print(r"There is no attr '%s' in Model" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) value " % (self.__table__, ",".join(fields)) 
        sql.append("3")
        print(sql)
class User(Model):
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")


p = User(id=5566, name="xuliang", email="12345@sina.com", password="123456")
p.save()
