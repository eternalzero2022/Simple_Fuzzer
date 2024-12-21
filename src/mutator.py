# 变异组件
import random

from src.model import Fuzz, SeedEntry
from src.power_scheduler import calculate_score
from src.executor import execute_seed
from src.result_monitor import save_data, save_crash_seed, save_timeout_seed
from src.fuzzconstants import FuzzConstants


def fuzz_one(fuzz):
    """
    执行一次变异操作，需要在变异的同时将新种子拿去执行
    :param fuzz: Fuzz实例
    :return: 变异是否成功
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    # 获取当前种子
    parent_seed = fuzz.current_seed
    if not parent_seed:
        print("没有可供选择的种子")
        return False  # 跳过变异

    original_seed = parent_seed.seed
    depth = parent_seed.depth

    # 通过能量调度组件计算性能分数
    score = calculate_score(parent_seed, fuzz)
    mutation_count = decide_mutation_count(score)

    # 初始化统计信息
    found_new_seed = False

    for _ in range(mutation_count):
        # 选择变异方法并执行变异
        mutation_type = random.choice(["bitflip", "arith", "interest", "havoc"])
        mutated_seed = mutate(original_seed, mutation_type, fuzz)
        new_seed = SeedEntry(mutated_seed, depth + 1, fuzz.cycle_times)

        # 模拟调用执行组件
        exec_result = execute_seed(new_seed,fuzz)

        if exec_result["new_coverage"]:
            # 如果有新的覆盖率，创建新种子项并添加到队列创建的新种子队列项
            found_new_seed = True
            fuzz.add_seed(new_seed)
            fuzz.last_fuzz_finds_count += 1
            save_data(fuzz)

        if exec_result["crash"]:
            # 增加崩溃计数
            fuzz.last_fuzz_crash_count += 1
            fuzz.total_crash_count += 1
            if fuzz.total_crash_count <= FuzzConstants.max_crash_seeds_saved:
                save_crash_seed(new_seed,fuzz)

        if exec_result["timeout"]:
            # 增加超时计数
            fuzz.last_fuzz_timeout_count += 1
            fuzz.total_timeout_count += 1
            if fuzz.total_timeout_count <= FuzzConstants.max_timeout_seeds_saved:
                save_timeout_seed(new_seed,fuzz)

        if not exec_result["new_coverage"]:
            del new_seed

    # 如果没有发现新覆盖，作为最后手段执行 splice 变异
    if not found_new_seed:
        mutated_seed = mutate(original_seed, "splice", fuzz)
        new_seed = SeedEntry(mutated_seed, depth + 1, fuzz.cycle_times)
        exec_result = execute_seed(new_seed, fuzz)

        if exec_result["new_coverage"]:
            found_new_seed = True
            fuzz.add_seed(new_seed)
            fuzz.last_fuzz_finds_count += 1
            save_data(fuzz)

        if exec_result["crash"]:
            fuzz.last_fuzz_crash_count += 1
            fuzz.total_crash_count += 1
            if fuzz.total_crash_count <= FuzzConstants.max_crash_seeds_saved:
                save_crash_seed(new_seed,fuzz)

        if exec_result["timeout"]:
            fuzz.last_fuzz_timeout_count += 1
            fuzz.total_timeout_count += 1
            if fuzz.total_timeout_count <= FuzzConstants.max_timeout_seeds_saved:
                save_timeout_seed(new_seed,fuzz)

    # print("变异结果：",found_new_seed)
    return found_new_seed


def mutate(seed, mutation_type, fuzz):
    """
    根据变异类型对种子执行变异操作。
    :param seed: 原始种子
    :param mutation_type: 变异类型
    :param fuzz: Fuzz实例（需要访问种子队列或字典）
    :return: 变异后的种子
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    if mutation_type == "bitflip":
        fuzz.current_mutate_strategy = "bitfilp"
        return bitflip_mutation(seed)
    elif mutation_type == "arith":
        fuzz.current_mutate_strategy = "arith"
        return arithmetic_mutation(seed)
    elif mutation_type == "interest":
        fuzz.current_mutate_strategy = "interest"
        return interest_mutation(seed)
    elif mutation_type == "havoc":
        fuzz.current_mutate_strategy = "havoc"
        return havoc_mutation(seed)
    elif mutation_type == "splice":
        fuzz.current_mutate_strategy = "splice"
        return splice_mutation(seed, fuzz.seed_queue)
    else:
        raise ValueError(f"未知的变异类型: {mutation_type}")


def decide_mutation_count(score):
    """
    根据能量得分决定变异次数
    :param score: 种子的能量得分
    :return: 变异次数
    """
    # 设定基本变异次数的下限和上限
    base_mutation_count = 1
    max_mutation_count = 20  # 假设最大变异次数为 20

    mutation_count = int(score / 100)

    # 确保变异次数在有效范围内
    return max(base_mutation_count, min(mutation_count, max_mutation_count))


# def execute_seed(seed, fuzz):
#     """
#     模拟种子执行并返回执行结果。
#     :param seed: 执行的种子
#     :return: 执行结果字典
#     """
#     # 调用执行组件执行种子
#     execution_time = random.uniform(0.01, 1.0)  # 模拟执行时间
#     bitmap_size = random.randint(10, 100)  # 模拟覆盖率位图大小
#     new_coverage = random.choice([True, False])
#     crash = random.choice([True, False])
#     timeout = random.choice([True, False])

#     # 更新Fuzz统计信息
#     fuzz.total_bitmap_size += bitmap_size
#     fuzz.bitmap_entry_count += 1
#     fuzz.total_execution_time += execution_time
#     fuzz.execution_entry_count += 1

#     # 返回模拟的执行结果
#     return {
#         "new_coverage": new_coverage,
#         "crash": crash,
#         "timeout": timeout,
#     }


# # 具体的变异方法（示例与之前类似）
def bitflip_mutation(seed, L=1, S=1):  # L/S 变体包括1/1、2/1、4/1、8/8、16/8、32/8
    """位翻转变异"""
    if not seed:
        return seed
    seed = bytearray(seed)

    length = len(seed)
    skip_bytes = 24
    if length <= 48:
        skip_bytes = 8
    if length <= 24:
        skip_bytes = 0
    
    
    for i in range(0, len(seed) * 8, S):

        # 跳过前8个字节
        if i // 8 < skip_bytes and FuzzConstants.not_modify_title_bytes_when_mutating:
            continue

        for j in range(L):
            if i + j < len(seed) * 8:
                byte_index, bit_index = divmod(i + j, 8)
                seed[byte_index] ^= (1 << bit_index)
    return bytes(seed)


def arithmetic_mutation(seed, L=8):  # L可能为8 16 32
    """算术操作变异 """
    if not seed:
        return seed
    seed = bytearray(seed)
    step = L // 8

    length = len(seed)
    skip_bytes = 24
    if length <= 48:
        skip_bytes = 8
    if length <= 24:
        skip_bytes = 0

    
 
    for i in range(0, len(seed) - step + 1, 1):  # 按 8 位步长操作

        # 跳过前16个字节
        if i < skip_bytes and FuzzConstants.not_modify_title_bytes_when_mutating:
            continue

        value = int.from_bytes(seed[i:i + step], 'little', signed=False)
        # 随机选择加法或减法
        mutation_type = random.choice(['add', 'sub'])
        # 随机生成变异值，选择一个较小的随机值（例如 -128 到 128 范围）
        mutation_value = random.randint(-128, 128)
        if mutation_type == 'sub':
            mutation_value = - mutation_value
        new_value = (value + mutation_value) & ((1 << L) - 1)
        seed[i:i + step] = new_value.to_bytes(step, 'little', signed=False)
    return bytes(seed)


def interest_mutation(seed, L=8):  # L可能为8 16 32
    """有趣值覆盖变异"""
    interesting_values = {
        8: [0, 1, 255],
        16: [0, 1, 65535, 32768],
        32: [0, 1, 4294967295, 2147483648],
    }
    if not seed or L not in interesting_values:
        return seed
    seed = bytearray(seed)
    step = L // 8

    length = len(seed)
    skip_bytes = 24
    if length <= 48:
        skip_bytes = 8
    if length <= 24:
        skip_bytes = 0

    for i in range(0, len(seed) - step + 1, step):

        # 跳过前16个字节
        if i < skip_bytes and FuzzConstants.not_modify_title_bytes_when_mutating:
            continue

        value = random.choice(interesting_values[L])
        seed[i:i + step] = value.to_bytes(step, 'little', signed=False)
    return bytes(seed)


def havoc_mutation(seed):
    """随机多种变异叠加 (havoc)"""
    seed = bytearray(seed)
    for _ in range(random.randint(1, 10)):  # 随机叠加 1~10 次变异
        mutation = random.choice([bitflip_mutation, arithmetic_mutation, interest_mutation])
        seed = bytearray(mutation(seed))
        if random.random() < 0.2:  # 随机删除块
            start = random.randint(0, len(seed))
            end = random.randint(start, len(seed))
            del seed[start:end]
        if random.random() < 0.2:  # 随机复制块
            start = random.randint(0, len(seed))
            end = random.randint(start, len(seed))
            seed[start:start] = seed[start:end]
    return bytes(seed)


def splice_mutation(seed, seed_queue):
    """拼接其他种子内容变异 (splice)"""
    if not seed_queue:
        return seed
    seed = bytearray(seed)
    other_seedEntry = random.choice(seed_queue)
    if not isinstance(other_seedEntry,SeedEntry):
        raise TypeError("变异失败，种子非SeedEntry类型")
    other_seed = other_seedEntry.seed
    splice_point = random.randint(0, len(seed))
    other_splice_point = random.randint(0, len(other_seed))
    seed[splice_point:] = other_seed[other_splice_point:]
    return bytes(seed)
