# 执行结果监控组件
from model import Fuzz, SeedEntry
from fuzzconstants import FuzzConstants

import os
import json


def show_stats(fuzz):
    """
    打印执行过程中的统计信息，以日志的形式打印在控制台上
    :param fuzz: Fuzz实例
    :return: 无
    :分行展示当前fuzz状态
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    print(f"=== {FuzzConstants.status_show_count}次状态展示 ===")
    FuzzConstants.status_show_count += 1

    print(f"当前循环次数: {fuzz.cycle_times}")
    print(f"当前执行种子数: {len(fuzz.seed_queue)}")
    print(f"新发现的种子数: {fuzz.last_fuzz_finds_count}")
    print(f"当前崩溃种子数: {fuzz.last_fuzz_crash_count}")
    print(f"当前超时种子数: {fuzz.last_fuzz_timeout_count}")
    print(f"当前总覆盖率位图大小: {fuzz.total_bitmap_size}")
    print(f"当前执行时间: {fuzz.total_execution_time}")
    print(f"当前执行次数: {fuzz.execution_entry_count}")
    print(f"当前种子的能量总分: {fuzz.total_score}")
    print(f"当前没有发现新覆盖率的循环次数: {fuzz.no_new_coverage_cycle_times}")
    print(f"当前探索模式: {fuzz.exploration_mode}")
    print("===================")


def save_data(fuzz):
    """
    保存执行过程中的数据以json格式到本地文件中
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    filepath = fuzz.out_dir
    # 创建输出文件夹
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    # 将一些统计数据保存为JSON文件
    stats_data = {
        "cycle_times": fuzz.cycle_times,
        "total_bitmap_size": fuzz.total_bitmap_size,
        "total_execution_time": fuzz.total_execution_time,
        "execution_entry_count": fuzz.execution_entry_count,
        "total_score": fuzz.total_score,
        "no_new_coverage_cycle_times": fuzz.no_new_coverage_cycle_times,
        "exploration_mode": fuzz.exploration_mode,
        "last_fuzz_finds_count": fuzz.last_fuzz_finds_count,
        "last_fuzz_crash_count": fuzz.last_fuzz_crash_count,
        "last_fuzz_timeout_count": fuzz.last_fuzz_timeout_count,
    }

    # 保存当前的统计数据到JSON文件
    datafile_name = f"stats{FuzzConstants.data_file_count}.json"
    FuzzConstants.data_file_count += 1
    with open(os.path.join(filepath, datafile_name), "w") as f:
        json.dump(stats_data, f, indent=4)

def save_seed_info(fuzz):
    """
    保存当前fuzz中所有种子的基本信息到内存中，确保每个种子的id唯一。
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    # 创建一个字典来保存种子信息，key为种子的id，value为种子信息
    if not hasattr(fuzz, "seed_info"):
        fuzz.seed_info = {}

    # 遍历fuzz的种子队列并保存信息
    for seed in fuzz.seed_queue:
        if isinstance(seed, SeedEntry):
            # 如果种子信息已存在，则跳过
            if seed.id not in fuzz.seed_info:
                seed_info = {
                    "seed_id": seed.id,
                    "seed": seed.seed,
                    "depth": seed.depth,
                    "handicap": seed.handicap,
                    "bitmap_size": seed.bitmap_size,
                    "execution_time": seed.execution_time,
                    "score": seed.perf_score,  # 如果需要性能得分
                }
                fuzz.seed_info[seed.id] = seed_info

    print(f"种子信息已保存，当前共有 {len(fuzz.seed_info)} 个唯一种子")
