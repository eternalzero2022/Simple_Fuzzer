import subprocess
import time
import mmap
import os
from model import Fuzz, SeedEntry

def perform_dry_run(fuzz):
    """
    执行所有初始种子，更新种子的执行时间、覆盖率等信息。
    :param fuzz: Fuzz实例
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    for seed in fuzz.seed_queue:
        if not isinstance(seed, SeedEntry):
            raise TypeError('种子必须是SeedEntry类型')

        # 构建执行命令，替换输入种子路径
        cmd = fuzz.cmd.replace('@@', seed.file_path)

        # 创建共享内存来存储覆盖率信息
        # 设定共享内存的大小（以字节为单位）
        coverage_size = 1024 * 1024  # 假设使用1MB大小的共享内存
        shared_mem = mmap.mmap(-1, coverage_size)  # 创建匿名共享内存

        # 设置环境变量，目标程序会读取这个环境变量来获取共享内存地址
        os.environ["COVERAGE_SHM"] = str(shared_mem.fileno())

        try:
            start_time = time.time()

            # 执行目标程序，捕获输出和错误
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=fuzz.timeout)

            end_time = time.time()

            # 计算执行时间
            exec_time = end_time - start_time
            seed.exec_time = exec_time

            # 更新种子覆盖率等信息
            if result.returncode == 0:
                # 假设目标程序会在共享内存中存储覆盖率信息
                coverage_data = shared_mem[:coverage_size]
                coverage_size = len(coverage_data)  # 这里你可以根据覆盖率数据的实际结构进行分析
                seed.coverage = coverage_size

                print(f"种子 {seed.file_path} 执行成功，时间：{exec_time:.2f}s，覆盖率大小：{coverage_size}")

            else:
                print(f"种子 {seed.file_path} 执行失败，错误码：{result.returncode}")

        except subprocess.TimeoutExpired:
            seed.timeout_count += 1
            print(f"种子 {seed.file_path} 执行超时")

        except Exception as e:
            print(f"执行种子 {seed.file_path} 时出错: {str(e)}")

        finally:
            # 关闭共享内存
            shared_mem.close()


def perform_dry_run1(fuzz):

    """
    先将当前种子队列中的所有种子执行一遍，更新种子队列中的信息以及fuzz统计信息，主要是更新每个种子的执行时间和覆盖位图大小
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO