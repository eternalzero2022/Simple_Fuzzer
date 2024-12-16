# Simple Fuzzer的入口程序

import argparse
import signal
import time
import os

from src.model import Fuzz, SeedEntry
from src.seed_scheduler import select_next_seed, finished_one_cycle, start_new_fuzz_cycle
from src.mutator import fuzz_one
from src.result_monitor import show_stats, save_data, outdir_init
from src.executor import perform_dry_run
from src.evaluator import save_coverage_plot, display_fuzz_config, display_result_info
from src.fuzzconstants import FuzzConstants

def check_afl_in_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            if b'afl' in content:
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

def signal_hanlder(signum, frame):
    """
    信号处理函数，用于处理SIGINT信号
    :param signum: 信号编号
    :param frame: 栈帧
    """
    Fuzz.stop_fuzzing = True

def is_directory_locked(directory):
    """检查目录是否被锁定"""
    lock_file = os.path.join(directory, 'lockfile.lock')
    return os.path.exists(lock_file)

def lock_directory(directory):
    """锁定目录"""
    if not os.path.exists(directory):
        os.makedirs(directory,exist_ok=True)
    lock_file = os.path.join(directory, 'lockfile.lock')
    with open(lock_file, 'w') as f:
        f.write('locked')  # 创建锁文件

def unlock_directory(directory):
    """解锁目录"""
    lock_file = os.path.join(directory, 'lockfile.lock')
    if os.path.exists(lock_file):
        os.remove(lock_file)  # 删除锁文件


# if __name__ == '__main__':
def main(args):

    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_hanlder)

    # # 创建解析器
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', type=str, help='种子输入目录')
    # parser.add_argument('-o', type=str, help='执行结果输出目录')
    # parser.add_argument('--cmd', type=str, help='程序执行命令')
    # parser.add_argument('-s', type=str, help='种子调度策略')
    # parser.add_argument('-n', type=str, help='任务名称')

    # args = parser.parse_args()

    if args.i is None:
        args.i = input('请输入种子输入目录：')



        # args.i = '../seeds_example'
    if args.o is None:
        # args.o = input('请输入执行结果输出目录：')
        args.o = "./fuzz_output"

    if args.cmd is None:
        args.cmd = input('请输入程序启动命令：')


    # # 将args.cmd中所有@@替换为种子输入目录
    # absolute_path = os.path.abspath(args.i)
    # args.cmd = args.cmd.replace('@@', absolute_path)


    if args.s is None:
        args.s = 'COVERAGE'

    if args.n is None or len(args.n) == 0:
        args.n = "default"

    # 定义并初始化Fuzz实例
    fuzz = Fuzz(args.i, args.o, args.cmd, args.s, args.n)

    display_fuzz_config(fuzz)

    path_tmp = args.cmd.split()
    file_to_execute_path = os.path.abspath(path_tmp[0])
    if not check_afl_in_binary(file_to_execute_path):
        print("错误：待执行程序未经过afl-cc插桩编译")
        exit(1)
    else:
        print("待执行程序已经过afl插桩编译")



    if not fuzz.read_seed_from_in_dir():
        print('种子读取失败')
        exit(1)

    if fuzz.seed_queue:
        print('已读取到', len(fuzz.seed_queue), '个种子')
        fuzz.last_fuzz_finds_count = len(fuzz.seed_queue)
    else:
        print('请提供至少一个有效的初始种子')
        exit(1)

        # 检查该输出文件夹是否被使用
    if is_directory_locked(os.path.join(fuzz.out_dir, fuzz.task_name)):
        print(f"Error: 任务目录{os.path.abspath(os.path.join(fuzz.out_dir, fuzz.task_name))}正在被其它模糊程序使用！请先尝试修改任务名称或关闭其它模糊程序")
        exit(1)
    else:
        lock_directory(os.path.join(fuzz.out_dir, fuzz.task_name))

    try:

        outdir_init(fuzz)
        
        perform_dry_run(fuzz)

        print(f"种子队列长度：",len(fuzz.seed_queue))

        print('即将进行模糊测试')
        time.sleep(1)

        # 记录模糊开始时候的时间
        fuzz.program_start_time = time.time()
        fuzz.program_run_time = 0;

        # 最开始的时候执行一次保存工作
        save_data(fuzz)

        # 获取当前时间，将其转化为整数
        current_time = time.time()
        start_time = int(current_time)
        last_time = start_time

        while not Fuzz.stop_fuzzing:
            # 循环执行模糊过程直到接收到停止指令
            # 先判断是否执行完毕了队列的一轮循环
            if finished_one_cycle(fuzz):
                start_new_fuzz_cycle(fuzz)


            fuzz_succeed = False

            # 每次当当前种子被跳过，且当前种子还存在时，就会进入循环
            while True:
                fuzz.fuzz_times_in_cycle += 1

                # 选择种子
                fuzz.current_seed = select_next_seed(fuzz)
                if fuzz.current_seed is None:
                    # 如果没有种子了，就退出循环
                    break

                if not isinstance(fuzz.current_seed, SeedEntry):
                    raise TypeError('Error: 种子必须是SeedEntry类型')
                # 执行变异
                fuzz_succeed = fuzz_one(fuzz)

                # 更新当前种子的信息
                c_seed = fuzz.current_seed
                c_seed.has_fuzzed = fuzz_succeed
                c_seed.fuzz_times += 1
                if fuzz_succeed:
                    c_seed.finds_count += fuzz.last_fuzz_finds_count
                    fuzz.last_cycle_finds_count += fuzz.last_fuzz_finds_count
                    c_seed.crash_count += fuzz.last_fuzz_crash_count
                    c_seed.timeout_count += fuzz.last_fuzz_timeout_count
                else:
                    c_seed.skipped_times += 1

                if fuzz_succeed or fuzz.current_seed is None or Fuzz.stop_fuzzing or finished_one_cycle(fuzz):
                    # 如果变异成功或者当前种子为None或者接收到停止指令，就退出循环
                    break

            # 根据时间间隔输出日志信息
            current_time = time.time()
            fuzz.program_run_time = current_time - fuzz.program_start_time

            if current_time >= int(last_time)+FuzzConstants.stats_show_interval_sec:
                show_stats(fuzz)
                last_time = int(current_time)

    except Exception as e:
        print(e)
    finally:
        print('即将进行模糊测试结束工作')
        display_result_info(fuzz)
        unlock_directory(os.path.join(fuzz.out_dir, fuzz.task_name))
        save_data(fuzz)
        save_coverage_plot(fuzz)
        exit(0)

