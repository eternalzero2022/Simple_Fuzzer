# Simple_Fuzzer

## 项目执行流程
### 1.初始化——main.c,总程序的入口
- 项目框架看main.c了解很快就掌握了
- 启动后通过用户输入参数初始化Fuzz类(逻辑在main.c开头)
- 用户提供一个种子目录(暂未定)输出目录以及待测试程序指令，其中包含初始种子（即一些合法的程序输入，txt格式或者其它，暂未定）
- 然后系统读取这些种子并存储在队列中(也就是Fuzz类中)并且明确交互程序目标和输出日志路径

### 2. 执行(main.c的主要逻辑)
- 先判断是否完成一轮种子调度
- 从Fuzz中挑选一个种子 main.c::select_next_seed
- 进行种子变异 main.c::fuzz_one 生成种子可拓展和修改
- 运行目标程序部分代码，然后根据输入判断目标程序部分是否异常，这部分尚还未补全

### 3. 反馈并重新执行
- 根据系统时间填写输出日志——start_time, last_time和show_stats
- 根据测试结果，更新种子队列
- 进入下一轮循环


- save_data 保存信息，系统执行结束


```aiignore
--src
   |--evaluator.py : # 评估组件,评估种子质量
   |--exeluator.py : # 执行种子的组件
   |--fuzzconstants.py : # 存储项目全局变量
   |--main.py : # 项目启动的总逻辑控制，项目入口
   |--model.py : # 存放模糊测试类对象class 包含Fuzz和seedEntry种子对象
   |--mutator.py : # 变异组件, 控制种子变异策略
   |--power_scheduler.py : # 能量组件，评定种子能量，用于调度
   |--result_monitor.py : # 结果监控组件，打印种子执行情况和记录
   |--seed_scheduler.py : # 种子调度策略仓库
 
```