# Simple_Fuzzer

## 项目设计方案
### 项目架构
总体结构如下：
```aiignore
--fuzz.py # 项目入口
--src
   |--evaluator.py : # 评估组件,评估种子质量
   |--executor.py : # 执行种子的组件
   |--fuzzconstants.py : # 存储项目全局变量
   |--main.py : # 项目整体循环的总逻辑控制组件
   |--model.py : # 存放模糊测试类对象class 包含Fuzz和seedEntry种子对象
   |--mutator.py : # 变异组件, 控制种子变异策略
   |--power_scheduler.py : # 能量组件，评定种子能量，用于调度
   |--result_monitor.py : # 结果监控组件，打印种子执行情况和记录
   |--seed_scheduler.py : # 种子调度策略仓库
 
```
模糊测试中每个不同的组件被分成不同的python文件，每一个组件负责模糊测试中的一项任务。

### 项目类层次设计
整体来看，fuzz.py和main.py位于类层次的上层，统筹整个模糊程序的启动和循环流转；mutator.py位于类层次的中层，负责处理模糊测试中单个种子的多个业务；seed_scheduler.py、power_scheduler.py、executor.py、result_monitor.py、evaluator.py位于类层次的较低层，负责处理模糊测试中的某个具体业务，而fuzzconstants.py、model.py位于类层次的最底层，是对数据类型的定义和常量的定义，被其它组件所依赖。

#### 上层类
fuzz.py作为程序入口，接收程序启动参数，并执行main.py。

main.py位于业务代码程序的最上层，负责整个项目执行循环的控制，包括控制对初始种子进行预执行（依赖于executor.py），选择下一个执行变异的种子（依赖于seed_scheuler.py），执行变异并获取变异结果（依赖于mutator.py），并输出日志和保存执行状态（依赖于result_monitor.py），程序结束时输出覆盖率曲线图（依赖于evaluator.py）。

#### 中层类
mutator.py的层次位于中层，负责响应main.py的调用执行一次变异，根据种子分数决定种子变异次数（基于power_scheduler.py）并让执行组件执行变异后的种子（依赖于executor.py），同时根据执行组件的执行结果对种子进行保存或记录信息（依赖于result_monitor.py）。

#### 较低层类
seed_scheduler.py层次位于较低层，负责根据当前种子总体执行情况来选择下一次变异的种子。会使用种子的分数作为依据之一（依赖power_scheduler.py）

power_scheduler.py层次位于较低层，负责计算当前种子的表现分数。用于提供种子调度的依据和变异的依据。

executor.py层次位于中层，负责响应mutator的调用，将种子输入到目标程序并执行，返回执行结果。同时响应main.py的调用，负责对初始种子进行预执行。

result_monitor.py层次位于中层，负责响应mutator.py的调用保存执行信息并保存特殊种子；同时响应main.py的调用并在控制台实时输出日志

evaluator.py层次位于中层，负责在最后响应main.py的调用并绘制本次模糊测试的覆盖率曲线图，并进行保存

#### 底层类
model.py是类型定义文件，定义模糊测试中需要使用的数据类型，被其它组件依赖

fuzzconstants.py存储模糊测试中使用到的常量，对其进行统一管理

通过提取出类型定义文件和常量定义文件，避免组件之间的循环依赖

### 项目执行流程
#### 1.接收用户输出并初始化，进入整体任务循环(fuzz.c，main.c)
- fuzz.py接收用户传递的参数，并将参数传递给main.py并执行
- main.py负责初始化，包括解析用户参数，确定种子输入输出文件、命令
、任务名称等信息
- 初始化种子输出目录，清空已有内容并标记目录为正在使用
- 获取初始种子、检查待执行程序是否是被插桩程序
- 进入整体模糊测试任务循环，不断生成变异种子执行并获取结果

#### 2. 整体任务循环(main.c)
- 先判断是否完成一轮种子调度
- 从Fuzz中挑选一个种子 main.c::select_next_seed
- 进行种子变异 main.c::fuzz_one 生成种子可拓展和修改
- 运行目标程序部分代码，然后根据输入判断目标程序部分是否异常，这部分尚还未补全

#### 3. 反馈并重新执行
- 根据系统时间填写输出日志——start_time, last_time和show_stats
- 根据测试结果，更新种子队列
- 进入下一轮循环


- save_data 保存信息，系统执行结束


