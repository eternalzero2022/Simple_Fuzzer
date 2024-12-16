# 评估组件
from src.model import Fuzz
from src.fuzzconstants import FuzzConstants
from matplotlib.ticker import MaxNLocator

import os
import matplotlib.pyplot as plt
import json
import csv


# def save_coverage_plot(fuzz):
#     """
#     读取数据fuzz.out_dir的json文件并生成覆盖率曲线图
#     :param fuzz: Fuzz实例
#     :return: 无
#     """
#     if not isinstance(fuzz,Fuzz):
#         raise TypeError("fuzz必须是Fuzz类型")
#     # 获取文件夹中的所有json文件
#     filepath = os.path.join(fuzz.out_dir, fuzz.task_name)
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)  # 确保文件夹存在

#     all_files = [f for f in os.listdir(filepath) if f.endswith(".json")]

#     cycle_times = []
#     avg_bitmap_sizes = []

#     # 读取所有json文件
#     for file in all_files:
#         with open(os.path.join(filepath, file), "r") as f:
#             data = json.load(f)
#             # 计算平均位图大小,只存储有效值
#             if data["execution_entry_count"] > 0:
#                 avg_bitmap_size = data["total_bitmap_size"] / data["execution_entry_count"]
#                 avg_bitmap_sizes.append(avg_bitmap_size)
#                 cycle_times.append(data["cycle_times"])

#     # 如果没有数据，提前返回
#     if not cycle_times:
#         print("没有有效的数据可用于绘制图表。")
#         return

#     # 创建渐变色
#     cmap = plt.get_cmap("Spectral")  # 使用漂亮的渐变色
#     norm = plt.Normalize(vmin=min(cycle_times), vmax=max(cycle_times))
#     sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
#     sm.set_array([])

#     # 绘制覆盖率曲线
#     plt.figure(figsize=(10, 6))

#     # 创建渐变色线条
#     for i in range(len(cycle_times) - 1):
#         plt.plot(cycle_times[i:i + 2], avg_bitmap_sizes[i:i + 2], color=cmap(norm(cycle_times[i])), lw=2)

#     # 添加渐变色条
#     plt.colorbar(sm, label="Cycle Times")

#     # 添加标题和标签
#     plt.title("Average Bitmap Size vs Cycle Times", fontsize=16)
#     plt.xlabel("Cycle Times", fontsize=12)
#     plt.ylabel("Average Bitmap Size", fontsize=12)

#     # 额外的图表美化
#     plt.grid(True, linestyle='--', alpha=0.5)  # 增加虚线网格
#     plt.tight_layout()

#     # 保存图表
#     plot_file = os.path.join(filepath, "plot", "coverage_plot.png")
#     plt.savefig(plot_file)
#     plt.close()
#     print(f"覆盖率图已保存到 {plot_file}")

def save_coverage_plot(fuzz):
    """
    读取数据fuzz.out_dir的CSV文件并生成覆盖率曲线图
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError("fuzz必须是Fuzz类型")
    
    # 获取CSV文件路径
    filepath = os.path.join(fuzz.out_dir, fuzz.task_name)
    csv_file_path = os.path.join(filepath, "stats.csv")

    if not os.path.exists(csv_file_path):
        print("CSV文件不存在，无法绘制图表。")
        return

    program_run_times = []
    bitmap_sizes = []

    # 读取CSV文件
    with open(csv_file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            execution_entry_count = int(row["execution_entry_count"])
            if execution_entry_count > 0:
                bitmap_size = (row["bitmap_size"])
                bitmap_sizes.append(bitmap_size)
                program_run_times.append(float(row["program_run_time"]))

    # 如果没有数据，提前返回
    if not program_run_times:
        print("没有有效的数据可用于绘制图表。")
        return

    # 创建渐变色
    cmap = plt.get_cmap("Spectral")  # 使用漂亮的渐变色
    norm = plt.Normalize(vmin=min(program_run_times), vmax=max(program_run_times))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # 绘制覆盖率曲线
    plt.figure(figsize=(10, 6))
    ax = plt.gca()  # 获取当前坐标轴

    # 创建渐变色线条
    for i in range(len(program_run_times) - 1):
        plt.plot(program_run_times[i:i + 2], bitmap_sizes[i:i + 2], color=cmap(norm(program_run_times[i])), lw=2)

    # 添加渐变色条
    cbar = plt.colorbar(sm, ax=ax, label="Program Run Time")  # 指定坐标轴

    # 添加标题和标签
    plt.title("Average Bitmap Size vs Program Run Time", fontsize=16)
    plt.xlabel("Program Run Time(s)", fontsize=12)
    plt.ylabel("Bitmap Size (Edges)", fontsize=12)

    # 设置纵坐标的刻度数量
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=10))  # 设置最多显示5个刻度

    # 额外的图表美化
    plt.grid(True, linestyle='--', alpha=0.5)  # 增加虚线网格
    plt.tight_layout()

    # 保存图表
    if not os.path.exists(os.path.join(filepath,"plot")):
        os.makedirs(os.path.join(filepath,"plot"))
    plot_file = os.path.join(filepath, "plot", "coverage_plot.png")
    plt.savefig(plot_file)
    plt.close()
    print(f"覆盖率图已保存到 {plot_file}")


# def display_json_stats(fuzz):
#     """
#     展示所有json文件的统计信息，按照图表格式逐行输出
#     :param fuzz: Fuzz实例
#     :return: 无
#     """
#     if not isinstance(fuzz, Fuzz):
#         raise TypeError('fuzz必须是Fuzz类型')

#     # 目录路径
#     filepath = os.path.join(fuzz.out_dir, fuzz.task_name) 
#     # 如果文件夹不存在，抛出错误
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"文件夹 {filepath} 不存在")

#     # 获取文件夹中所有的json文件
#     json_files = [f for f in os.listdir(filepath) if f.endswith('.json')]

#     if not json_files:
#         print("没有找到任何 JSON 文件。")
#         return

#     # 打印标题行
#     print(f"{'Cycle':<10}{'Total Bitmap Size':<20}{'Total Execution Time':<25}{'Execution Entry Count':<25}"
#           f"{'Total Score':<15}{'No New Coverage Cycles':<25}{'Exploration Mode':<20}"
#           f"{'Last Fuzz Finds':<20}{'Last Fuzz Crashes':<20}{'Last Fuzz Timeouts':<20}")

#     # 遍历每个JSON文件，读取并展示信息
#     for json_file in json_files:
#         with open(os.path.join(filepath, json_file), "r") as file:
#             stats_data = json.load(file)

#             cycle_times = stats_data.get("cycle_times", 0)
#             total_bitmap_size = stats_data.get("total_bitmap_size", 0)
#             total_execution_time = stats_data.get("total_execution_time", 0)
#             execution_entry_count = stats_data.get("execution_entry_count", 0)
#             total_score = stats_data.get("total_score", 0)
#             no_new_coverage_cycle_times = stats_data.get("no_new_coverage_cycle_times", 0)
#             exploration_mode = stats_data.get("exploration_mode", False)
#             last_fuzz_finds_count = stats_data.get("last_fuzz_finds_count", 0)
#             last_fuzz_crash_count = stats_data.get("last_fuzz_crash_count", 0)
#             last_fuzz_timeout_count = stats_data.get("last_fuzz_timeout_count", 0)

#             # 打印每个JSON文件的相关信息
#             print(f"{cycle_times:<10}{total_bitmap_size:<20}{total_execution_time:<25}{execution_entry_count:<25}"
#                   f"{total_score:<15}{no_new_coverage_cycle_times:<25}{exploration_mode:<20}"
#                   f"{last_fuzz_finds_count:<20}{last_fuzz_crash_count:<20}{last_fuzz_timeout_count:<20}")


def display_fuzz_config(fuzz):
    """
    打印fuzz的配置信息
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    # 打印fuzz的配置信息
    print(f"{'Attribute':<30}{'Value'}")
    print("="*60)

    # 列出Fuzz对象的配置信息
    print(f"{'In Directory':<30}{fuzz.in_dir}")
    print(f"{'Out Directory':<30}{fuzz.out_dir}")
    print(f"{'Strategy':<30}{fuzz.strategy}")
    # print(f"{'Cycle Times':<30}{fuzz.cycle_times}")
    # print(f"{'Exploration Mode':<30}{fuzz.exploration_mode}")
    # print(f"{'No New Coverage Cycle Times':<30}{fuzz.no_new_coverage_cycle_times}")
    # print(f"{'Total Execution Time':<30}{fuzz.total_execution_time}")

def display_all_seeds_info(fuzz):
    """
    打印所有种子的详细信息
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    # 检查是否已保存种子信息
    if not hasattr(fuzz, "seed_info") or len(fuzz.seed_info) == 0:
        print("尚未保存任何种子信息！请先调用save_seed_info函数保存种子信息。")
        return

    # 打印表头
    print(f"{'Seed ID':<10}{'Seed':<30}{'Depth':<10}{'Handicap':<10}{'Bitmap Size':<15}{'Execution Time':<15}{'Score':<10}")
    print("="*90)

    # 打印所有种子的详细信息
    for seed_info in fuzz.seed_info.values():
        print(f"{seed_info['seed_id']:<10}{str(seed_info['seed']):<30}{seed_info['depth']:<10}{seed_info['handicap']:<10}{seed_info['bitmap_size']:<15}{seed_info['execution_time']:<15}{seed_info['score']:<10}")

def display_result_info(fuzz):
    if not isinstance(fuzz, Fuzz):
        raise TypeError("fuzz必须是Fuzz类型")
    
    print("模糊测试执行结束")
    print(f"本次共执行种子{fuzz.exec_called_times}个，崩溃种子数量: {fuzz.total_crash_count}  超时种子数量: {fuzz.total_timeout_count}")

