# 执行结果监控组件
from model import Fuzz


def show_stats(fuzz):
    """
    打印执行过程中的统计信息，以日志的形式打印在控制台上
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO


def save_data(fuzz):
    """
    保存执行过程中的数据到本地文件中
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO