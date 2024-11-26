# Simple Fuzzer的入口程序

import argparse
import signal
import time

from model import Fuzz, SeedEntry
from seed_scheduler import select_next_seed, finished_one_cycle, start_new_fuzz_cycle
from mutator import fuzz_one
from result_monitor import show_stats, save_data
from executor import perform_dry_run


def signal_hanlder(signum, frame):
    """
    信号处理函数，用于处理SIGINT信号
    :param signum: 信号编号
    :param frame: 栈帧
    """
    Fuzz.stop_fuzzing = True


if __name__ == '__main__':

    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_hanlder)

    # 创建解析器
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='种子输入目录')
    parser.add_argument('-o', type=str, help='执行结果输出目录')
    parser.add_argument('--cmd', type=str, help='程序执行命令')
    parser.add_argument('-s', type=str, help='种子调度策略')

    args = parser.parse_args()

    if args.i is None:
        args.i = input('请输入种子输入目录：')
        # args.i = '../seeds_example'
    if args.o is None:
        args.o = input('请输入执行结果输出目录：')

    if args.cmd is None:
        args.cmd = input('请输入程序启动命令：')

    # 将args.cmd中所有@@替换为种子输入目录
    args.cmd = args.cmd.replace('@@', args.i)

    if args.s is None:
        args.s = 'COVERAGE'

    # 定义并初始化Fuzz实例
    fuzz = Fuzz(args.i, args.o, args.cmd, args.s)

    if not fuzz.read_seed_from_in_dir():
        print('种子读取失败')
        exit(0)

    if fuzz.seed_queue:
        print('已读取到', len(fuzz.seed_queue), '个种子')
        fuzz.last_fuzz_finds_count = len(fuzz.seed_queue)
    else:
        print('请提供至少一个有效的初始种子')
        exit(0)
    perform_dry_run(fuzz)

    print('即将进行模糊测试')
    time.sleep(1)

    # 获取当前时间，将其转化为整数
    current_time = time.time()
    start_time = int(current_time)
    last_time = start_time

    while not Fuzz.stop_fuzzing:
        # 循环执行模糊过程直到接收到停止指令
        # 先判断是否执行完毕了队列的一轮循环
        if finished_one_cycle(fuzz):
            start_new_fuzz_cycle(fuzz)

        fuzz.fuzz_times_in_cycle += 1

        fuzz_succeed = False

        # 每次当当前种子被跳过，且当前种子还存在时，就会进入循环
        while True:
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

            if fuzz_succeed or fuzz.current_seed is None or Fuzz.stop_fuzzing:
                # 如果变异成功或者当前种子为None或者接收到停止指令，就退出循环
                break

        # 根据时间间隔输出日志信息
        current_time = time.time()
        if current_time >= int(last_time)+1:
            show_stats(fuzz)
            last_time = int(current_time)

    print('即将进行模糊测试结束工作')
    save_data(fuzz)
    exit(0)

