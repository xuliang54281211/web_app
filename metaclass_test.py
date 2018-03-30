#!/usr/bin/env python3
# -*- coding: gbk -*-

def upper_attrs(class_name, class_parents, class_attrs):
    attr = ((name, value)for name, value in class_attrs.items() if not name.startswith('__'))
    a = dict((name.upper(), value)for name, value in attr)
    return type(class_name, class_parents, a)

__metaclass__ = upper_attrs

pw = upper_attrs('trick', (), {'hello':'liang'})
pe = pw()
try:
    print(pe.hello)
except:
    print('has no attr \'hello\'')
    print(pe.HELLO)
finally:
    print("end")
