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


def execute_seed(seed, fuzz):
    """
    将seed作为种子，输入执行，更新种子的执行时间、覆盖率等信息，以及fuzz整体的total_bitmap_size，bitmap_entry_count和total_execution_time，execution_entry_count。
    需要在覆盖率数据发生更新时调用执行结果监控组件的函数保存数据
    :param seed: 表示种子的比特串，并不是SeedEntry
    :param fuzz: Fuzz实例
    :return: 一个dictionary，包含new_coverage, crash和timeout三个键，如果种子具备对应特性就将其设为true，否则为false
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')

    # 创建共享内存
    key = 5678
    shm_size = 256 * 256
    shm = sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREAT, size=shm_size)
    shm_id = shm.id

    # 将共享内存区域置为0
    empty_data = b'\x00' * shm_size
    shm.write(empty_data)

    # 设置环境变量，目标程序会读取这个环境变量来获取共享内存地址
    os.environ[FuzzConstants.shm_env_var] = str(shm_id)

    # 初始化结果字典
    result_dict = {"new_coverage": False, "crash": False, "timeout": False}

    try:
        # 构建执行命令
        cmd = fuzz.exec_command

        start_time = time.time()

        # 执行目标程序，捕获输出和错误
        process = subprocess.run(cmd, shell=True, input=seed, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=FuzzConstants.exec_timeout)

        end_time = time.time()

        # 计算执行时间
        exec_time = end_time - start_time
        fuzz.total_execution_time += exec_time
        fuzz.execution_entry_count += 1

        if process.returncode == 0:
            # 假设目标程序会在共享内存中存储覆盖率信息
            message = shm.read()
            coverage_data = message[:shm_size]

            # 计算覆盖率
            coverage_size = sum(1 for byte in coverage_data if byte > 0)
            if coverage_size > 0:
                result_dict["new_coverage"] = True
                fuzz.total_bitmap_size += coverage_size
                fuzz.bitmap_entry_count += 1

            print(f"种子执行成功，时间：{exec_time:.2f}s，覆盖率大小：{coverage_size}")

        else:
            # 记录崩溃
            result_dict["crash"] = True
            print(f"种子执行失败，错误码：{process.returncode}")

    except subprocess.TimeoutExpired:
        result_dict["timeout"] = True
        print(f"种子执行超时")

    except Exception as e:
        result_dict["crash"] = True
        print(f"执行种子时发生错误: {str(e)}")

    finally:
        # 关闭共享内存
        shm.detach()

    return result_dict