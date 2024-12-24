class FuzzConstants:
    """
    常量类，包含各种程序运行时的常量
    用户可以修改custom constants注释之后的常量
    """
    exploration_switch_cycle_times_notfound = 10  # 当连续n个循环未发现新覆盖率时开启探索模式
    exploration_switch_cycle_times_begin = 30  # 如果循环次数未达到n则持续开启探索模式
    exploration_switch_coverage = 0.35  # 如果覆盖率低于n则持续开启探索模式
    cal_score_based_on_handicap = True  # 是否基于handicap计算分数，也就是越先执行到的则越快执行
    data_file_count = 0
    shm_env_var = "__AFL_SHM_ID"
    shm_size = 256*256
    not_modify_title_bytes_when_mutating = True

    # custom constants
    stats_show_interval_sec = 10 #  每次控制台输出两条日志信息之间的间隔（单位：秒）

    max_crash_seeds_saved = 100 #  执行结果目录下最多可以保存的崩溃种子的数量

    max_timeout_seeds_saved = 100 # 执行结果目录下最多可以保存的超时种子的数量

    exec_timeout = 3 #  测试用例执行超时判断标准（单位：秒）

    same_score = False  # 是否为每个种子分配相同变异机会
 



