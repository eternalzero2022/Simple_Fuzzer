# 数据结构定义组件
import os
from abc import ABC, abstractmethod
from fuzzconstants import FuzzConstants


class Fuzz:
    """
    Fuzz核心数据类，包含了各种需要的配置信息和种子队列。
    必要时可以添加属性和方法。
    """

    def __init__(self, in_dir, out_dir, exec_command, strategy, task_name):
        """
        初始化Fuzz类
        :param in_dir: 种子目录
        :param out_dir: 结果输出目录
        :param exec_command: 执行命令
        :param strategy: 种子调度策略
        """
        self.in_dir = in_dir  # 种子目录
        self.out_dir = out_dir  # 结果输出目录
        self.exec_command = exec_command  # 执行命令
        self.task_name =  task_name  # 任务名称，用于确定结果输出目录的位置
        self.strategy = strategy  # 种子调度策略
        self.seed_queue = []  # 种子队列
        self.current_seed = None  # 当前种子，在每次变异前或每次开始新的队列循环时更新，在变异时可以直接使用
        self.fuzz_times_in_cycle = 0  # 当前队列循环内的fuzz次数
        self.cycle_times = 0  # 队列的循环次数
        self.no_new_coverage_cycle_times = 0  # 没有新的覆盖率的循环次数
        self.prev_queue_size = 0  # 上一次循环结束时的队列大小
        self.exploration_mode = True  # 探索模式标志，在覆盖率较低以及长时间没有新的覆盖率时开启。这个属性具体使不使用就看变异模块了
        self.new_seed_queue = []  # 新发现的种子队列，存储的内容均是包含在seed_queue中的内容，不允许在发现新种子时只添加进该队列而不添加进seed_queue中。由变异模块负责添加，由种子选择模块负责删除。
        self.last_fuzz_finds_count = 0  # 上一次fuzz发现的新种子数量
        self.last_fuzz_crash_count = 0  # 上一次fuzz发现的新崩溃数量
        self.last_fuzz_timeout_count = 0  # 上一次fuzz发现的新超时数量
        self.total_crash_count = 0  # 总共发现的新崩溃数量
        self.total_timeout_count = 0  # 总共发现的新超时数量
        self.last_cycle_finds_count = 0  # 上一次循环发现的新种子数量
        self.bitmap = bytes(FuzzConstants.shm_size)  # 覆盖率位图，其中的每一个字节都表示一条路径，如果这个字节大于0则说明这条路径被执行过
        self.bitmap_size = 0  # 覆盖率位图中大于0的字节的数量
        self.total_bitmap_size = 0  # 总位图大小
        self.bitmap_entry_count = 0  # 计算过位图的种子项的数量
        self.total_execution_time = 0  # 总执行时间
        self.execution_entry_count = 0  # 计算过执行时间的种子项的数量，目前理论上这个值和bitmap_entry_count应该是一样的
        # self.to_refresh_score_seed_queue = []  # 需要重新计算性能分数的种子队列，初始时以及在被种子选择选中时需要重新计算分数
        self.queue_changed = False  # 队列是否发生变化的标志，在COVERAGE策略下使用，用于判断是否需要重新计算性能分数
        self.select_probabilities = []  # 种子选择概率列表，在COVERAGE策略下使用，用于根据种子的性能分数计算概率
        self.total_score = 0  # 总分数，在COVERAGE策略下使用，用于计算总分数
        self.seed_info = {}
        self.program_start_time = 0; # 程序开始执行的绝对时间
        self.program_run_time = 0; # 程序从开始执行到现在的执行时间，从进入fuzz循环时开始
        self.status_show_count = 0;
        self.exec_called_times = 0; # 调用执行组件总次数
        

    stop_fuzzing = False  # 停止fuzzing标志

    def add_seed(self, seed_entry):
        """
        添加种子到种子队列和新种子队列中，参数必须是SeedEntry类型
        :param seed_entry: 种子队列项
        """
        if not isinstance(seed_entry, SeedEntry):
            raise TypeError('种子必须是QueueEntry类型')
        self.seed_queue.append(seed_entry)
        self.new_seed_queue.append(seed_entry)
        self.queue_changed = True

    def read_seed_from_in_dir(self):
        """
        从种子目录中读取种子文件，并添加到队列中
        """
        for root, dirs, files in os.walk(self.in_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        seed_entry = SeedEntry(content, 0)
                        self.add_seed(seed_entry)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    return False
        return True


# 队列项
class SeedEntry:
    """
    种子队列项，包含种子和深度等属性
    """

    id = 0

    def __init__(self, seed, depth, handicap=0):
        """
        种子队列项初始化
        :param seed: 初始输入
        :param depth:
        """
        self.file_path = None
        self.id = SeedEntry.id
        SeedEntry.id += 1
        self.seed = seed
        self.depth = depth
        self.has_fuzzed = False
        self.fuzz_times = 0  # fuzz的次数
        self.execution_time = 0  # 执行时间
        self.skipped_times = 0
        self.finds_count = 0
        self.crash_count = 0
        self.timeout_count = 0
        self.bitmap_size = 0
        self.perf_score = 0  # 性能分数
        self.handicap = handicap  #  产生这个种子时当前所处的循环次数，越是晚则越大
