class FuzzConstants:
    """
    常量类，包含各种常量
    """
    exploration_switch_cycle_times_notfound = 10  # 当连续n个循环未发现新覆盖率时开启探索模式
    exploration_switch_cycle_times_begin = 30  # 如果循环次数未达到n则持续开启探索模式
    exploration_switch_coverage = 0.35  # 如果覆盖率低于n则持续开启探索模式
    cal_score_based_on_handicap = True  # 是否基于handicap计算分数，也就是越先执行到的则越快执行
    same_score = True  # 每一个种子分数是否相同

    exec_timeout = 3

    # status_show_count = 0
    data_file_count = 0

    shm_env_var = "__AFL_SHM_ID"
    shm_size = 256*256
