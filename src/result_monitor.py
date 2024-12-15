# 执行结果监控组件
from model import Fuzz, SeedEntry
from fuzzconstants import FuzzConstants

import os
import json
import csv

def outdir_init(fuzz):
    """
    初始化CSV文件。如果文件存在，则清空文件内容；如果不存在，则创建新文件。
    :param file_path: CSV文件的路径
    :return: 无
    """
    dirpath = os.path.join(fuzz.out_dir, fuzz.task_name)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath,exist_ok=True)
    csv_file_path = os.path.join(dirpath, "stats.csv")
    if os.path.exists(csv_file_path):
        # 如果文件存在，清空文件内容
        open(csv_file_path, 'w').close()
        print(f"历史记录文件 '{csv_file_path}' 已清空。")
    else:
        # 如果文件不存在，创建新文件
        with open(csv_file_path, 'w') as f:
            pass  # 创建空文件

        # 遍历目录中的所有文件
    crash_seed_dic = os.path.join(dirpath,"crash_seeds")
    if not os.path.exists(crash_seed_dic):
        os.makedirs(crash_seed_dic,exist_ok=True)
    for filename in os.listdir(crash_seed_dic):
        files_path = os.path.join(crash_seed_dic, filename)
        # 检查是否是文件
        if os.path.isfile(files_path):
            os.remove(files_path)  # 删除文件

    timeout_seed_dic = os.path.join(dirpath,"timeout_seeds")
    if not os.path.exists(timeout_seed_dic):
        os.makedirs(timeout_seed_dic,exist_ok=True)
    for filename in os.listdir(timeout_seed_dic):
        files_path = os.path.join(timeout_seed_dic, filename)
        # 检查是否是文件
        if os.path.isfile(files_path):
            os.remove(files_path)  # 删除文件

def show_stats(fuzz):
    """
    打印执行过程中的统计信息，以日志的形式打印在控制台上
    :param fuzz: Fuzz实例
    :return: 无
    :分行展示当前fuzz状态
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    fuzz.status_show_count += 1

    # print(f"当前循环次数: {fuzz.cycle_times}")
    # print(f"当前执行种子数: {len(fuzz.seed_queue)}")
    # print(f"新发现的种子数: {fuzz.last_fuzz_finds_count}")
    # print(f"当前崩溃种子数: {fuzz.last_fuzz_crash_count}")
    # print(f"当前超时种子数: {fuzz.last_fuzz_timeout_count}")
    # print(f"当前总覆盖率位图大小: {fuzz.total_bitmap_size}")
    # print(f"当前执行时间: {fuzz.total_execution_time}")
    # print(f"当前执行次数: {fuzz.execution_entry_count}")
    # print(f"当前种子的能量总分: {fuzz.total_score}")
    # print(f"当前没有发现新覆盖率的循环次数: {fuzz.no_new_coverage_cycle_times}")
    # print(f"当前探索模式: {fuzz.exploration_mode}")
    # print(f"当前覆盖率位图大小：{fuzz.bitmap_size}")

    print(f"[*] Log_{fuzz.status_show_count} time:{fuzz.program_run_time:.2f}s (exec_count={fuzz.exec_called_times}  crash={fuzz.total_crash_count}  timeout={fuzz.total_timeout_count}  bitmap_size={fuzz.bitmap_size}  cycle_times={fuzz.cycle_times}  cycles_no_new_coverage={fuzz.no_new_coverage_cycle_times})")


# def save_data(fuzz):
#     """
#     保存执行过程中的数据以json格式到本地文件中
#     :param fuzz: Fuzz实例
#     :return: 无
#     """
#     if not isinstance(fuzz, Fuzz):
#         raise TypeError('fuzz必须是Fuzz类型')

#     filepath = os.path.join(fuzz.out_dir, fuzz.task_name)
#     # 创建输出文件夹
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)

#     # 将一些统计数据保存为JSON文件
#     stats_data = {
#         "cycle_times": fuzz.cycle_times,
#         "total_bitmap_size": fuzz.total_bitmap_size,
#         "total_execution_time": fuzz.total_execution_time,
#         "execution_entry_count": fuzz.execution_entry_count,
#         "total_score": fuzz.total_score,
#         "no_new_coverage_cycle_times": fuzz.no_new_coverage_cycle_times,
#         "exploration_mode": fuzz.exploration_mode,
#         "last_fuzz_finds_count": fuzz.last_fuzz_finds_count,
#         "last_fuzz_crash_count": fuzz.last_fuzz_crash_count,
#         "last_fuzz_timeout_count": fuzz.last_fuzz_timeout_count,
#     }

#     # 保存当前的统计数据到JSON文件
#     datafile_name = f"stats{FuzzConstants.data_file_count}.json"
#     FuzzConstants.data_file_count += 1
#     with open(os.path.join(filepath, datafile_name), "w") as f:
#         json.dump(stats_data, f, indent=4)

def save_data(fuzz):
    """
    保存执行过程中的数据以CSV格式到本地文件中
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    filepath = os.path.join(fuzz.out_dir, fuzz.task_name)
    # 创建输出文件夹
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    # CSV文件路径
    csv_file_path = os.path.join(filepath, "stats.csv")

    # 将一些统计数据保存为CSV文件
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
        "bitmap_size": fuzz.bitmap_size,
        "program_run_time": fuzz.program_run_time
    }


    # 如果CSV文件不存在，写入表头
    file_exists = os.path.isfile(csv_file_path)
    hasHeader = True
    if file_exists:
        with open(csv_file_path, 'r', newline='') as csvfile:
            first_line = csvfile.readline()  # 读取第一行
            if not first_line.strip():  # 检查第一行是否为空
                hasHeader = False

    with open(csv_file_path, mode='a', newline='') as csvfile:
        fieldnames = stats_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not (file_exists and hasHeader):
            writer.writeheader()  # 写入表头

        writer.writerow(stats_data)  # 写入当前的统计数据

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


def save_crash_seed(seed, fuzz):
    if not isinstance(seed, SeedEntry):
        raise TypeError("seed必须是SeedEntry类型")

    if not isinstance(fuzz, Fuzz):
        raise TypeError("fuzz必须是Fuzz类型")
    
    dicPath = os.path.join(fuzz.out_dir, fuzz.task_name, "crash_seeds")
    if not os.path.exists(dicPath):
        os.makedirs(dicPath)

    # 存储seed
    filename = f"id={seed.id}_time={fuzz.program_run_time:.2f}s_depth={seed.depth}_bitmapSize={seed.bitmap_size}"
    filepath = os.path.join(dicPath,filename)
    with open(filepath,"wb") as f:
        f.write(seed.seed)

def save_timeout_seed(seed, fuzz):
    if not isinstance(seed, SeedEntry):
        raise TypeError("seed必须是SeedEntry类型")

    if not isinstance(fuzz, Fuzz):
        raise TypeError("fuzz必须是Fuzz类型")
    
    dicPath = os.path.join(fuzz.out_dir, fuzz.task_name, "timeout_seeds")
    if not os.path.exists(dicPath):
        os.makedirs(dicPath)

    # 存储seed
    filename = f"id={seed.id}_time={fuzz.program_run_time:.2f}s_depth={seed.depth}_bitmapSize={seed.bitmap_size}"
    filepath = os.path.join(dicPath,filename)
    with open(filepath,"wb") as f:
        f.write(seed.seed)

    

