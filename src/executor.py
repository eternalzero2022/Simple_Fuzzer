import subprocess
import time
import mmap
import os
import tempfile
import sysv_ipc
import ctypes
from model import Fuzz, SeedEntry
from fuzzconstants import FuzzConstants

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
        cmd = fuzz.exec_command

        # 创建共享内存
        key = 5678
        shm_size = 256 * 256
        shm = sysv_ipc.SharedMemory(key,sysv_ipc.IPC_CREAT, size=shm_size)
        shm_id = shm.id

        # 将共享内存区域置为0
        empty_data = b'\x00' * shm_size
        shm.write(empty_data)

        # 设置环境变量，目标程序会读取这个环境变量来获取共享内存地址
        os.environ[FuzzConstants.shm_env_var] = str(shm_id)

        try:

            start_time = time.time()

            # 执行目标程序，捕获输出和错误
            result = subprocess.run(cmd, shell=True, input=seed.seed, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=FuzzConstants.exec_timeout)

            end_time = time.time()

            # 计算执行时间
            exec_time = end_time - start_time
            seed.execution_time = exec_time

            

            # 更新种子覆盖率等信息
            if result.returncode == 0:
                # 假设目标程序会在共享内存中存储覆盖率信息
                message = shm.read()

                # coverage_data就是种子覆盖率图
                coverage_data = message[:shm_size]

                coverage_size = sum(1 for byte in coverage_data if byte > 0)
                seed.bitmap_size = coverage_size

                print(f"种子 {seed.id} 执行成功，时间：{exec_time:.2f}s，覆盖率大小：{coverage_size}")

            else:
                print(f"种子 {seed.id} 执行失败，错误码：{result.returncode}")

        except subprocess.TimeoutExpired:
            seed.timeout_count += 1
            print(f"种子 {seed.id} 执行超时")

        except Exception as e:
            seed.crash_count += 1
            print(f"执行种子 {seed.id} 时出错: {str(e)}")

        finally:
            # 关闭共享内存
            shm.detach()


def perform_dry_run1(fuzz):

    """
    先将当前种子队列中的所有种子执行一遍，更新种子队列中的信息以及fuzz统计信息，主要是更新每个种子的执行时间和覆盖位图大小
    :param fuzz: Fuzz实例
    :return: 无
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    # TODO