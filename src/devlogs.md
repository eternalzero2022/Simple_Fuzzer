# 开发日志
## 进度安排
- 2024.11.26 完成源码阅读，程序构建规划
- 2024.11.27 搭建整体框架
- 2024.12.01 完成种子排序/能量调度组件，开始变异/执行组件
- 2024.12.05 完成变异组件
- 2024.12.09 完成测试执行组件
- 2024.12.12 完成执行结果监控组件
- 2024.12.13 完成评估组件
- 2024.12.14 修复可能存在的bug
- 2024.12.16 编译待测程序，并对待测程序执行24小时模糊测试

## 任务分配
- 沈王寻：整体框架搭建、种子排序组件、能量调度组件、项目完成后的查漏补缺、待测程序编译
- 蔡如峰：变异组件
- 刘恒宇：测试执行组件
- 陈文鸿：执行结果监控组件、评估组件

## 开发难题
### 如何避免不同模块间的相互循环依赖？
将类型定义和常量定义分别提取为单独的模块，保证不同模块对类型和常量的依赖是单项的


### AFL++源码区分old_seed_selection和其它调度策略的代码太过冗余，常常使用很多if来对old_seed_selection进行处理
将old_seed_selection与其它调度策略的实现统一放在种子选择函数中，并为不同调度策略提供不同的具体实现，避免其它部分的代码与old_seed_selection发生耦合

### 如何实现根据命令行输入来动态采取不同种子调度策略，同时避免策略与统计数据模块的相互依赖？
使用统一的种子调度函数，将策略作为形参传递，根据形参的值调用不同的函数。这样做虽然会产生控制耦合，但是在可接收范围内


### 希望为种子调度增加随机性，但是AFL++源码中的加权随机数计算方式较为复杂，涉及到大小队列以及数组指针等的复杂操作
使用简单的依据能量调度组件计算得到的分数除以全部种子的分数总和作为被选中的概率，结合随机数进行加权随机选择

### 每次循环开始都需要针对每个种子计算score，计算开销太大
由于seed本身的许多属性在执行完毕后即确定，因此在没有改变队列元素的时候不需要重新计算分数。通过设置queue_changed参数指定队列元素是否被改变，只有当其值为True的时候才进行种子分数的重新计算。同时将已经计算完毕的概率数组存储在统计数据结构中，在队列元素没有改变的时候可以直接使用，无需重新计算概率数组。

### 如何从afl-cc插桩过的程序中进行交互并获取覆盖率信息
通过网络搜索可知，afl-fuzz通过启动一个fork server，与插桩程序进行交互，而afl-fuzz通过管道与fork server交互，无需负责主动fork子进程。而覆盖率的信息则通过共享内存的方式设定环境变量来写入，并可以在fork server中读取

### fork server部分内容较为复杂，难以实现
省略fork server的大部分步骤，利用python的subprocess模块来执行给定的命令启动程序，并读取覆盖率信息。

### 使用mmap设置的共享内存似乎无法被插桩后的程序获取，也不会修改共享内存
插桩后的程序通过shmat函数来将共享内存的标识符转化为地址，来获取这块共享内存。mmap设置的标识符并不能用于shmat。需要使用python中的sysv_ipc库的相关函数实现共享内存的分配

### 如何从每次位图更新total_bitmap_size总和中提取当次覆盖率位图信息
基于更新次数很大且覆盖率的上升性，使用总平均覆盖率位图可以较为接近地模拟当次覆盖率信息avg_bitmap_size = data["total_bitmap_size"] / data["execution_entry_count"]

### 使用makefile运行python难以传递带空格的参数，且将用户中断视为异常
放弃使用makefile，通过在项目根目录下新建fuzz.py来作为启动程序

### 如何让docker打包环境能够提供afl-cc插桩的环境
使用aflplusplus作为docker的基础镜像，并在docker中安装python环境。

### 如何让项目在打包为docker前就在项目目录下提供插桩过的待测程序
先将待测程序挂载到aflplusplus的docker镜像中，执行编译后再将待测程序复制到项目目录下
