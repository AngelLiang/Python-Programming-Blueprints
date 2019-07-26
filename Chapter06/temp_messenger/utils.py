# coding=utf-8

import time


def runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        finish = time.time() - start
        print("%r run time:%r" % (func.__name__, finish))
        return ret
    return wrapper
