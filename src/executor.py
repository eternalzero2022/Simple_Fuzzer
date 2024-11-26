# 执行组件
from model import Fuzz


def perform_dry_run(fuzz):
    """
    先将当前种子队列中的所有种子执行一遍，更新种子队列中的信息以及fuzz统计信息，主要是更新每个种子的执行时间和覆盖位图大小
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO