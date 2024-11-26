# 变异组件
from model import Fuzz


def fuzz_one(fuzz):
    """
    执行一次变异操作，需要在变异的同时将新种子拿去执行
    :param fuzz: Fuzz实例
    :return: 变异是否成功
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO
    return False