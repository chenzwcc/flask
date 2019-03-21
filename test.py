# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/4 上午10:57
import os
from functools import wraps


def onner(func):
    @wraps(func)
    def inner(*args,**kwargs):
        return func(*args,**kwargs)
    return inner

@onner
def funcc():
    print('p')

print(funcc.__name__)

name = os.path.splitext('123.txt')
print(name[-1])