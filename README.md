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

## 快速开始
### 环境构建
环境构建前，需要先确保已经拥有了经过afl插桩编译过的程序。如果程序还没有经过afl插桩编译，需要**先将项目目录下的Dockerfile修改为如下内容**。如果已经拥有afl插桩编译过的程序则**可跳过**修改Dockerfile。
```
# 使用 Python 3.10.12 作为基础镜像
FROM aflplusplus/aflplusplus

# 安装 make 和 build-essential
RUN apt-get update && apt-get install -y python3 python3-pip cmake libtool make build-essential llvm clang file binutils && apt-get clean

RUN mkdir /SimpleFuzzer

# 设置工作目录
WORKDIR /SimpleFuzzer

# 复制当前目录的内容到 /SimpleFuzzer 目录
COPY . .

# 安装 requirements.txt 中的依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV CC=/AFLplusplus/afl-cc
ENV CXX=/AFLplusplus/afl-cc

ENTRYPOINT ["/bin/bash"]

```


快速打包为Docker镜像：
```
docker build -t simplefuzzer:latest .
```
打包完成后，可以启动这个镜像。如果想要将待测程序放入镜像，只需要添加-v参数
```
docker run -it -v “<your_program_path>:/src” --name simplefuzzer simplefuzzer:latest
```
如果不想使用Docker，也可以在Linux环境中直接使用，需要确保拥有可执行python环境，且完整安装requirements.txt中的依赖项。可以使用如下命令安装
```
pip install -r requirements.txt
```

### AFL插桩编译
注意：如果你已经拥有了使用afl插桩编译的程序，或在上一步中没有修改Dockerfile，则跳过此板块，进入“执行模糊测试”板块。

在使用simplefuzzer前，需要确保待测程序已经经过afl插桩编译。如果还未插桩编译，docker环境中也配置了afl的编译环境（使用上一板块中修改过后的Dockerfile进行构建），AFL++相关组件位于/AFLplusplus下。

在docker容器中使用cmake或autotools编译时，自动使用afl-cc插桩编译，环境已经配置好了对应的环境变量。如果想要切换其它编译组件，只需要修改环境变量CC和CXX的值为对应编译组件即可。例如，如果希望使用afl-clang-fast编译，只需要执行如下命令：
```
export CC=/AFLplusplus/afl-clang-fast
export CXX=/AFLplusplus/afl-clang-fast
```
### 执行模糊测试
在项目工作目录下（`/SimpleFuzzer`），执行以下命令：
```
python3 fuzz.py -i <seeds_directory> --cmd="<program_start_command>"
```
只需要将其中的seeds_directory替换为种子文件路径、将program_start_command替换为待测程序启动命令即可。

项目提供了一个非常简单的程序和种子文件，只需要复制以下代码即可执行：
```
python3 fuzz.py -i ./seeds_example  --cmd="./program/calculator"
```

默认会在`./fuzz_output/default`下保存执行结果。该目录下`stats.csv`保存模糊测试执行过程中的状态记录，`crash_seeds`和`timeout_seeds`分别保存产生崩溃的种子和产生超时的种子，plot目录下存储本次执行的覆盖率随时间变化曲线图。

用户如果想要修改执行结果保存路径，可以使用-o参数修改执行结果保存主目录，并使用-n参数指定任务名称，即修改主保存目录下的子目录。例如使用如下命令：
```
python3 fuzz.py -o ./my_output_dic -n calculator [...]
```
则输出目录被指定为./my_output_dic/calculator。

如果希望在程序启动命令中指定种子文件的路径，可以使用'@@'标志。例如
```
python3 fuzz.py -i /seeds --cmd="./calculator @@"
```
此时，在执行待测程序时，命令就会被替换为/seeds目录下具体存在的种子文件，例如`./calculator /seeds/seed1.txt`

如果想要切换种子调度策略，可以使用-s参数指定。存在两种种子调度策略：OLD和COVERAGE，分别表示顺序选择和基于覆盖率选择，默认使用COVERAGE。例如，如果使用以下命令：
```
python3 fuzz.py [...] -s OLD
```
则会切换为OLD调度策略，即顺序选择策略。

完整示例：在项目目录下，我们提供了一组可供执行的示例程序。
```
python3 fuzz.py -i program_examples/compiled/src/mjs-2.20.0/tests -o my_outputs -n mjs -s COVERAGE --cmd="program_examples/compiled/src/mjs-2.20.0/build/mjs/mjs -f @@"
```
则该命令会对mjs进行模糊测试，使用COVERAGE策略，种子目录为program_examples/compiled/src/mjs-2.20.0/tests，输出结果将保存在./my_outputs/mjs目录下

### 进阶使用
在src/fuzzconstants.py中，定义了一些程序执行过程中会使用的常量。其中，用户可修改的常量位于`# custom constants`注释的下方。用户可以通过修改文件中的这些常量，来自定义模糊测试过程中的一些配置。

以下是可供修改的常量列表：
|常量|说明|默认值|
|---|---|---|
|stats_show_interval_sec|每次控制台输出两条日志信息之间的间隔（单位：秒）|10|
|max_crash_seeds_saved|执行结果目录下最多可以保存的崩溃种子的数量|100|
|max_timeout_seeds_saved|执行结果目录下最多可以保存的超时种子的数量|100|
|exec_timeout|测试用例执行超时判断标准（单位：秒）|3|
|same_score|是否为每个种子分配相同变异机会|False|

### 更多示例程序
除了项目目录下`program`下的简单程序`calculator`和初始种子目录`seeds_example`外，项目还额外提供了十个真实世界中的程序，供程序进行模糊测试使用。

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
#### 1.接收用户输出并初始化，进入整体任务循环(fuzz.py，main.py)
- fuzz.py接收用户传递的参数，并将参数传递给main.py并执行
- main.py负责初始化，包括解析用户参数，确定种子输入输出文件、命令
、任务名称等信息
- 初始化种子输出目录，清空已有内容并标记目录为正在使用
- 获取初始种子、检查待执行程序是否是被插桩程序
- 进入整体模糊测试任务循环，不断生成变异种子执行并获取结果

#### 2. 种子调度(main.py, seed_scheduler.py, power_scheduler.py)
- 在模糊测试每轮循环的开始
- 调用seed_scheduler.py判断是否完成一轮调度层循环，若是，则进入一轮新的调度层循环（每轮循环会记录种子发现个数，作为上一轮循环结果信息，调度层循环也作为测试进度依据）
- 进入一轮变异层循环
- 调用seed_scheduler.py中的函数依照种子调度策略选择下一个要执行变异的种子
- 种子调度策略分为OLD和COVERAGE，若为OLD，则按顺序选择下一个；若为COVERAGE，则优先选择产生了新覆盖的种子，如果没有新覆盖种子则依据得分进行加权随机选择
- 种子得分在power_scheduler.py中，基于种子覆盖率大小、执行时间、深度以及是否最近生成来计算
- 若返回None，则表明本轮调度层循环已选择完所有种子

#### 3. 变异(mutator.py)
- 选择完毕下一个变异的种子后，main调用mutator.py的变异函数，对种子进行变异，返回是否产生新的变异种子
- mutator.py基于种子得分分配种子变异次数
- 每次变异随机选择位翻转、算术操作、有趣值覆盖以及随机多种变异叠加进行变异
- 将变异后的种子输入执行组件(executor.py)执行

#### 4. 执行(executor.py)
- 将获得的变异种子输入待测程序执行
- 开辟一块共享内存，作为获取插桩后程序执行覆盖率的方式
- 依据执行结果更新种子的覆盖率、执行时间，并更新覆盖率位图
- 根据执行返回值判断是否正常执行或崩溃或超时，并将结果返回变异组件

#### 5. 变异结果记录(mutator.py, result_monitor.py)
- mutator.py获取变异结果进行处理
- 如果产生新覆盖率则加入种子队列
- 如果产生崩溃或超时，则通过result_monitor.py记录该种子
- 如果没有产生新覆盖率，则采用splice变异对种子再次变异，获取执行结果
- 将变异是否有新种子加入种子队列返回给main.py

#### 6. 更新变异信息(main.py, result_monitor.py)
- main.py依据变异结果，更新模糊测试的全局属性，包括本轮循环的发现的新种子、特殊种子个数
- 依据是否产生新的新覆盖种子，决定是否继续变异层循环，直到产生了新覆盖种子或是外部的调度层循环结束或是收到用户中断
- 变异层循环结束后，在控制台中打印日志
- 重新开始一轮调度层循环

#### 7. 结束处理(main.py, result_monitor.py, evaluator.py)
- 收到用户中断或是其它异常时，进入结束处理阶段
- 展示模糊测试结果，解除目录占用状态
- result_monitor.py最后保存一轮模糊测试信息
- evaluator依据模糊测试的覆盖率变化绘制覆盖率变化曲线图