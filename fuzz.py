import argparse

from src import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='种子输入目录')
    parser.add_argument('-o', type=str, help='执行结果输出目录')
    parser.add_argument('--cmd', type=str, help='程序执行命令')
    parser.add_argument('-s', type=str, help='种子调度策略')
    parser.add_argument('-n', type=str, help='任务名称')

    args = parser.parse_args()

    main.main(args)