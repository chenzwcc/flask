# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:53

from . import home

@home.route('/')
def index():
    return "this is home page"