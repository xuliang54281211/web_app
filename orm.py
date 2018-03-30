#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ����Field(������Ԫ������Field�ķ���������ʱ�������޸ģ�
class Field(object):

    def __init__(self, name, column_type):  # column==>������
        self.name = name
        self.column_type = column_type

    # ����print��ӡ�����ʱ��python���������str����
    # �����������<������֣�ʵ����name����(����ʵ��ʱ����)>
    # ��ModelMetaclass�л��õ�
    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self. name)  # __class__��ȡ������࣬__name__ȡ������


class StringField(Field):

    def __init__(self, name):
        # super(type[, object-or-type])  ����type�ĸ������
        # super().__init()�������ǵ��ø����init����
        # varchar(100)��bigint����sql�е�һЩ��������
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
                print("Found mappings:%s ==> %s" % (k, v))  # �ҵ�ӳ�䣬 �����õ������__str__
                mappings[k] = v
        for k in mappings.keys():
                print('pop', k)
                attrs.pop(k)
        attrs["__mappings__"] = mappings
        attrs["__table__"] = name # ��ӱ������������������һ��
        attrs["hello"] = "xuliang"
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,  **kw):
        # ���ø��࣬��dict�ĳ�ʼ������
        super(Model, self).__init__(**kw)

    # �û�ȡkey��ֵ����������d[k]��Ҳ����d.k
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # ����̬����key��ֵ������������d[k]��Ҳ����d.k
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        # ������ӳ���е���
        for k, v in self.__mappings__.items():
            print("k=",k,"v=", v.name)
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) values (%s)" % (self.__table__, ",".join(fields), str(args))
        print("SQL: %s" % sql)
# ����һ���򵥵�ORM��д����


# ����ʵ�ʲ���һ�£��ȶ����User������Ӧ���ݿ�ı�User
class Users(Model):
    # ����������Ե��е�ӳ��
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")
    print("HHHHHHHHHHHHHHHHHH")


# ����һ��ʵ��
u = Users(id=12345, name="ReedSun", email="sunhongzhao@foxmail.com", password="nicaicai", hello = "xuliang")
u.save()
print(u.__mappings__["id"])
