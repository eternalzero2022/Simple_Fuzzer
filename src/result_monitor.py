# 执行结果监控组件
from model import Fuzz
from fuzzconstants import FuzzConstants

import os
import matplotlib.pyplot as plt
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


def save_coverage_plot(fuzz):
    """
    读取数据fuzz.out_dir的json文件并生成覆盖率曲线图
    :param fuzz: Fuzz实例
    :return: 无
    """
    # 获取文件夹中的所有json文件
    filepath = fuzz.out_dir
    all_files = [f for f in os.listdir(filepath) if f.endswith(".json")]

    cycle_times = []
    avg_bitmap_sizes = []

    # 读取所有json文件
    for file in all_files:
        with open(os.path.join(filepath, file), "r") as f:
            data = json.load(f)
            # 计算平均位图大小,只存储有效值
            if data["execution_entry_count"] > 0:
                avg_bitmap_size = data["total_bitmap_size"] / data["execution_entry_count"]
                avg_bitmap_sizes.append(avg_bitmap_size)
                cycle_times.append(data["cycle_times"])

    # 绘制覆盖率曲线
    plt.figure(figsize=(10, 6))
    plt.plot(cycle_times, avg_bitmap_sizes, label="Average Bitmap Size", color='blue', marker='o')

    # 添加标题和标签
    plt.title("Average Bitmap Size vs Cycle Times")
    plt.xlabel("Cycle Times")
    plt.ylabel("Average Bitmap Size")
    plt.legend()

    # 保存图表
    plot_file = os.path.join(filepath, "coverage_plot.png")
    plt.savefig(plot_file)
    plt.close()


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

