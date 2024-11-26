# 种子选择组件
import random

from model import Fuzz, SeedEntry
from fuzzconstants import FuzzConstants
from power_scheduler import calculate_score


def select_next_seed(fuzz):
    """
    选择下一个种子
    :param fuzz: Fuzz实例
    :return: 下一个种子的索引
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    if fuzz.strategy == 'COVERAGE':
        return select_coverage(fuzz)
    elif fuzz.strategy == 'OLD':
        return select_old(fuzz)
    else:
        return select_coverage(fuzz)


def select_old(fuzz):
    """
    初始种子调度策略：按顺序选择。如果选择到最后一个则返回None，如果是None则选择队列第一个
    :param fuzz: Fuzz实例
    :return: 选择的种子索引
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    print('种子选择策略：OLD')
    # 基于当前fuzz的seed项，返回这个项所处的队列的下一项
    if fuzz.current_seed is None:
        return fuzz.seed_queue[0]
    else:
        index = fuzz.seed_queue.index(fuzz.current_seed)
        if index == len(fuzz.seed_queue) - 1:
            return None
        else:
            return fuzz.seed_queue[index + 1]  # 否则选择队列中下一个种子


def select_coverage(fuzz):
    """
    基于覆盖率选择种子，如果有种子产生新覆盖率且还未选择，选择该种子，否则按照能量调度组件计算的分数的加权随机来选择
    :param fuzz: Fuzz实例
    :return: 选择的种子索引
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    print('种子选择策略：COVERAGE')
    # 如果存在产生新覆盖的种子，则优先选择
    if len(fuzz.new_seed_queue) > 0:
        # 选择新发现的种子
        new_seed = fuzz.new_seed_queue.pop(0)
        return new_seed
    else:
        # 如果队列有更新，则计算每个种子的分数
        if fuzz.queue_changed:
            for seed_entry in fuzz.seed_queue:
                if not isinstance(seed_entry, SeedEntry):
                    raise TypeError('Error: 种子必须是SeedEntry类型')
                score = calculate_score(seed_entry, fuzz)
                seed_entry.perf_score = score

            # 计算总分数，将seed_queue中的每个队列元素的perf_score求和
            fuzz.total_score = sum(seed_entry.perf_score for seed_entry in fuzz.seed_queue)
            fuzz.queue_changed = False

        # 计算每个种子的概率
        fuzz.select_probabilities = [seed_entry.perf_score / fuzz.total_score for seed_entry in fuzz.seed_queue]
        # 随机产生一个0到1之间的随机数，并用这个随机数选择种子
        random_num = random.random()
        # 计算累积概率
        cumulative_prob = 0
        for i, seed_entry in enumerate(fuzz.seed_queue):
            cumulative_prob += fuzz.select_probabilities[i]
            if random_num < cumulative_prob:
                return seed_entry

        # 如果出现其它意外情况，返回队列最后一个元素
        return fuzz.seed_queue[-1]


def finished_one_cycle(fuzz):
    """
    判断是否完成了队列中一次循环的调度
    :param fuzz: Fuzz实例
    :return: 是否完成了一次调度循环
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    if fuzz.strategy == 'COVERAGE':
        return fuzz.fuzz_times_in_cycle == len(fuzz.seed_queue)  # 如果当前fuzz次数等于种子队列长度，则完成了一次调度循环
    elif fuzz.strategy == 'OLD':
        return fuzz.current_seed is None  # 如果当前种子为None，则完成了一次调度循环
    else:
        return True


def start_new_fuzz_cycle(fuzz):
    """
    开始新的调度循环
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    fuzz.fuzz_times_in_cycle = 0  # 重置fuzz次数为0
    fuzz.cycle_times += 1  # 增加循环次数

    # 根据当前队列元素个数以及上一次的队列元素个数，判断有没有新的队列元素加入，如果没有则说明没有新发现
    if fuzz.last_cycle_finds_count == 0:
        fuzz.no_new_coverage_cycle_times += 1  # 增加没有新发现的循环次数
    else:
        fuzz.no_new_coverage_cycle_times = 0  # 重置没有新发现的循环次数为0
        fuzz.prev_queue_size = len(fuzz.seed_queue)  # 更新上一次的队列元素个数
        fuzz.last_cycle_finds_count = 0  # 重置上一次发现的新种子数量为0

    # 根据当前没有发现新覆盖率的循环次数决定是否开启
    fuzz.exploration_mode = start_exploration_mode(fuzz)  # 根据条件决定是否开启探索模式

    # if fuzz.strategy == 'OLD':
    #     fuzz.current_seed_index = -1  # 重置当前种子索引为-1，表示开始新的调度循环
    # elif fuzz.strategy == 'COVERAGE':
    #     pass  # 不需要做任何操作，因为COVERAGE策略不需要重置种子索引
    # else:
    #     pass  # 不需要做任何操作，因为COVERAGE策略不需要重置种子索引


def start_exploration_mode(fuzz):
    """
    判断开启探索模式
    :param fuzz: Fuzz实例
    :return: 是否开启探索模式
    """
    if fuzz.cycle_times < FuzzConstants.exploration_switch_cycle_times_begin:
        return True
    if fuzz.no_new_coverage_cycle_times > FuzzConstants.exploration_switch_cycle_times_notfound:
        return True
    return False
