# 能量调度组件
from model import SeedEntry, Fuzz
from fuzzconstants import FuzzConstants


def calculate_score(entry, fuzz):
    """
    计算种子的能量得分，根据不同的调度策略计算不同的得分
    :param entry: 种子队列项
    :param fuzz:Fuzz实例
    :return: 种子的能量得分
    """
    if not isinstance(entry, SeedEntry):
        raise TypeError('种子必须是SeedEntry类型')
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    score = 100
    if FuzzConstants.same_score:
        return score

    avg_bitmap_size = fuzz.total_bitmap_size / fuzz.bitmap_entry_count

    # 基于覆盖率改变分数
    if entry.bitmap_size * 0.3 > avg_bitmap_size:
        score *= 3
    elif entry.bitmap_size * 0.5 > avg_bitmap_size:
        score *= 2
    elif entry.bitmap_size * 0.75 > avg_bitmap_size:
        score *= 1.5
    elif entry.bitmap_size * 3 < avg_bitmap_size:
        score *= 0.25
    elif entry.bitmap_size * 2 < avg_bitmap_size:
        score *= 0.5
    elif entry.bitmap_size * 1.5 < avg_bitmap_size:
        score *= 0.75

    # 基于执行时间改变分数
    avg_execution_time = fuzz.total_execution_time / fuzz.execution_entry_count
    if entry.execution_time * 0.1 > avg_execution_time:
        score *= 0.1
    elif entry.execution_time * 0.25 > avg_execution_time:
        score *= 0.25
    elif entry.execution_time * 0.5 > avg_execution_time:
        score *= 0.5
    elif entry.execution_time * 0.75 > avg_execution_time:
        score *= 0.75
    elif entry.execution_time * 4 < avg_execution_time:
        score *= 3
    elif entry.execution_time * 3 < avg_execution_time:
        score *= 2
    elif entry.execution_time * 2 < avg_execution_time:
        score *= 1.5

    # 基于深度调整分数
    depth = entry.depth
    if depth <= 3:
        score *= 1
    elif depth <= 7:
        score *= 2
    elif depth <= 13:
        score *= 3
    elif depth <= 25:
        score *= 4
    else:
        score *= 5

    # 基于handicap调整分数，handicap表示多晚发现这条路径，越晚发现则分数越高
    if FuzzConstants.cal_score_based_on_handicap:
        handicap = entry.handicap
        if handicap >= 4:
            score *= 4
            entry.handicap -= 4
        elif handicap > 0:
            score *= 2
            entry.handicap -= 1
    return score
