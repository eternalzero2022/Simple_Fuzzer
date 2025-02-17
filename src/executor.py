import subprocess
import time
import mmap
import os
import tempfile
import sysv_ipc
import ctypes
from src.model import Fuzz, SeedEntry
from src.fuzzconstants import FuzzConstants

def perform_dry_run(fuzz):
    """
    执行所有初始种子，更新种子的执行时间、覆盖率等信息。
    :param fuzz: Fuzz实例
    """
    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    
    # 创建共享内存
    key = 5678
    shm_size = FuzzConstants.shm_size
    fuzz.shm = sysv_ipc.SharedMemory(key,sysv_ipc.IPC_CREAT, size=shm_size)
    shm_id = fuzz.shm.id
    os.environ[FuzzConstants.shm_env_var] = str(shm_id)
    
    for seed in fuzz.seed_queue:
        if not isinstance(seed, SeedEntry):
            raise TypeError('种子必须是SeedEntry类型')
        
        print(f"即将执行种子id={seed.id}")

        # 构建执行命令，替换输入种子路径
        cmd = fuzz.exec_command
        input_from_file = False

        # 判断命令中有没有“@@”字符，如果有的话，在fuzz.in_dir表示的目录下创建一个.seed_tmp的文件
        if "@@" in cmd:
            input_from_file = True
            filepath = os.path.join(fuzz.in_dir,".temp_seed")
            with open(filepath, "wb") as f:
                f.write(seed.seed)
            filepath = os.path.abspath(filepath)
            cmd = cmd.replace("@@",filepath)
            # print("替换后cmd为：",cmd)




        # 将共享内存区域置为0
        empty_data = b'\x00' * shm_size
        fuzz.shm.write(empty_data)

        # 设置环境变量，目标程序会读取这个环境变量来获取共享内存地址


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
                print(f"初始种子id{seed.id}[{seed.file_path}]执行成功")
                fuzz.total_execution_time += exec_time
                fuzz.execution_entry_count += 1
                # 假设目标程序会在共享内存中存储覆盖率信息
                message = fuzz.shm.read()

                # coverage_data就是种子覆盖率图
                coverage_data = message[:shm_size]

                # 更新覆盖率位图
                if len(fuzz.bitmap) == len(coverage_data):
                    fuzz.bitmap = bytes(a | b for a, b in zip(coverage_data, fuzz.bitmap))
                else:
                    raise ValueError("新种子覆盖率位图与总覆盖率位图长度必须相同")
                fuzz.bitmap_size = sum(1 for byte in fuzz.bitmap if byte > 0)
                # print(f"此时的覆盖率位图大小：{fuzz.bitmap_size}")

                coverage_size = sum(1 for byte in coverage_data if byte > 0)
                seed.bitmap_size = coverage_size
                fuzz.total_bitmap_size += coverage_size
                fuzz.bitmap_entry_count += 1

                # print(f"种子 {seed.id} 执行成功，时间：{exec_time:.2f}s，覆盖率大小：{coverage_size}")

            else:
                # print(f"种子 {seed.id} 执行失败，错误码：{result.returncode}")
                print(f"警告：初始种子id{seed.id}[{seed.file_path}]执行失败，忽略该种子")
                # fuzz.remove_seed(seed)
                seed.need_delete = True
                
                pass

        except subprocess.TimeoutExpired:
            seed.timeout_count += 1
            # print(f"种子 {seed.id} 执行超时")
            print(f"警告：初始种子id{seed.id}[{seed.file_path}]执行超时，忽略该种子")
            # fuzz.remove_seed(seed)
            seed.need_delete = True


        except Exception as e:
            seed.crash_count += 1
            print(f"执行种子 {seed.id} 时出错: {str(e)}")
            seed.need_delete = True

        finally:
            # 关闭共享内存
            if(os.path.isfile(os.path.join(fuzz.in_dir,".temp_seed"))):
                os.remove(os.path.join(fuzz.in_dir,".temp_seed"))
            # shm.remove()
            # shm.detach()

    # 删除所有需要删除的项
    fuzz.remove_seed()


def execute_seed(seed, fuzz):
    """
    将seed作为种子，输入执行，更新种子的执行时间、覆盖率等信息，以及fuzz整体的total_bitmap_size，bitmap_entry_count和total_execution_time，execution_entry_count。
    需要在覆盖率数据发生更新时调用执行结果监控组件的函数保存数据
    :param seed: 要执行种子的SeedEntry
    :param fuzz: Fuzz实例
    :return: 一个dictionary，包含new_coverage, crash和timeout三个键，如果种子具备对应特性就将其设为true，否则为false
    """

    if not isinstance(fuzz, Fuzz):
        raise TypeError('fuzz必须是Fuzz类型')
    
    if not isinstance(seed, SeedEntry):
        raise TypeError('seed必须是SeedEntry类型')
    
    fuzz.exec_called_times += 1

    try:
        # 创建共享内存
        # key = 5678
        shm_size = 256 * 256
        # shm = sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREAT, size=shm_size)
        shm_id = fuzz.shm.id

        # 将共享内存区域置为0
        empty_data = b'\x00' * shm_size
        fuzz.shm.write(empty_data)

        # 设置环境变量，目标程序会读取这个环境变量来获取共享内存地址
        # os.environ[FuzzConstants.shm_env_var] = str(shm_id)

        # 初始化结果字典
        result_dict = {"new_coverage": False, "crash": False, "timeout": False}

        input_from_file = False


        # 构建执行命令
        cmd = fuzz.exec_command

        # 判断命令中有没有“@@”字符，如果有的话，在fuzz.in_dir表示的目录下创建一个.seed_tmp的文件
        if "@@" in cmd:
            input_from_file = True
            filepath = os.path.join(fuzz.in_dir,".temp_seed")
            with open(filepath, "wb") as f:
                f.write(seed.seed)
            filepath = os.path.abspath(filepath)
            cmd = cmd.replace("@@",filepath)

        start_time = time.time()

        # shm_id = fuzz.shm.id
        # os.environ[FuzzConstants.shm_env_var] = str(shm_id)

        # 执行目标程序，捕获输出和错误
        process = subprocess.run(cmd, shell=True, input=seed.seed, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=FuzzConstants.exec_timeout)

        end_time = time.time()

        # 计算执行时间
        exec_time = end_time - start_time
        seed.execution_time = exec_time


        if process.returncode == 0:
            fuzz.total_execution_time += exec_time
            fuzz.execution_entry_count += 1

            # 假设目标程序会在共享内存中存储覆盖率信息
            message = fuzz.shm.read()
            coverage_data = message[:shm_size]

            # 计算覆盖率
            coverage_size = sum(1 for byte in coverage_data if byte > 0)
            seed.bitmap_size = coverage_size
            fuzz.total_bitmap_size += coverage_size
            fuzz.bitmap_entry_count += 1

            # print(f"种子执行成功，时间：{exec_time:.2f}s，覆盖率大小：{coverage_size}")

            # 更新覆盖率位图
            
            if len(fuzz.bitmap) == len(coverage_data):
                fuzz.bitmap = bytes(a | b for a, b in zip(coverage_data, fuzz.bitmap))
            else:
                raise ValueError("新种子覆盖率位图与总覆盖率位图长度必须相同")
            

            
            # 判断是否产生了新的覆盖率
            new_bitmap_size = sum(1 for byte in fuzz.bitmap if byte > 0)
            # print(f"此时的覆盖率位图大小：{new_bitmap_size}")
            if new_bitmap_size > fuzz.bitmap_size:
                fuzz.bitmap_size = new_bitmap_size
                result_dict["new_coverage"] = True

                # 记录程序到现在的相对执行时间
                current_time = time.time()
                fuzz.program_run_time = current_time - fuzz.program_start_time


        else:
            # 记录崩溃
            result_dict["crash"] = True
        
            # print(f"种子执行失败，错误码：{process.returncode}")

    except subprocess.TimeoutExpired:
        result_dict["timeout"] = True
        # print(f"种子执行超时")

    except Exception as e:
        result_dict["crash"] = True

    finally:
        # 关闭共享内存
        if(os.path.isfile(os.path.join(fuzz.in_dir,".temp_seed"))):
            os.remove(os.path.join(fuzz.in_dir,".temp_seed"))
        # shm.remove()
        # shm.detach()

    return result_dict