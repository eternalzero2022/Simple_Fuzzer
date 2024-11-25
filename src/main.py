# Simple Fuzzer的入口程序

import argparse



# 创建解析器
parser = argparse.ArgumentParser()
parser.add_argument('-i',type=str,help='种子输入目录')
parser.add_argument('-o',type=str,help='执行结果输出目录')

args = parser.parse_args()

if args.i is None:
    args.i = input('请输入种子输入目录：')

if args.o is None:
    args.o = input('请输入执行结果输出目录：')

print(args.i)
print(args.o)