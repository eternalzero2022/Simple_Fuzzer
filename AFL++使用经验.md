AFL++模糊测试执行命令（均在ububtu 22.04上执行）

```
//拉取镜像
docker pull aflplusplus/aflplusplus

//启动容器，注意下面存待测试代码的文件夹路径需要加的是目录名，而不是直接的文件
docker run -ti --name 容器名称，方便管理 -v 存待测试代码的带上点杠的文件夹路径:/src aflplusplus/aflplusplus

//重新启动某个关闭的container
docker start container号

//进入某个启动的container的命令行
docker exec -it container号 /bin/bash

//容器中设置CC和CXX环境变量
export CC=/AFLplusplus/afl-cc
export CXX=/AFLplusplus/afl-cc

//接下来对项目编译。如果是cmake就按照下面方式编译。
//如果你想先用自己的项目演示一遍而不是给定的现有项目，可以先在src文件夹下创建CMakeLists.txt，内容可以为如下：（记得删除注释）
cmake_minimum_required(VERSION 3.10)
project(HelloWorld C)//指定项目名

add_executable(hello hello.c)//创建一个名为hello的可执行文件，源文件为hello.c
//如果是现有项目就不用手动创建了
//使用cmake编译项目(需要先提前创建一个build目录，存放待构建的makefile。我这里是直接在根目录下创建了一个build文件夹，不是的话可以自定义-B的内容)
mkdir /build
cmake -S /src -B /build -G "Unix Makefiles"

//此时在构建文件夹/build下应该会有cmake产物包括makefile，进入该文件夹并构建
make

//此时应该会出现可执行文件，一般是没有后缀名的文件。例如这里是hello文件

//如果是Autotools，可以按照如下方式：
//如果源文件目录下没有configure文件，但是有autogen.sh，就执行以下命令：
./autogen.sh
//此时应该就会出现configure文件。此时就执行：
./configure --disable-shared

//同样，执行make命令编译
make

//完成编译后到达这步
//如果程序从控制台输入，需要先创建一个保存种子的目录
mkdir /seeds
//然后在其中创建一些种子文件，例如input1、input2等，命名随意，其中存放的内容是即将在运行程序的时候从控制台输入的内容
echo "具体的种子输入" > input1

//创建一个存储afl输出的目录
mkdir /afl-output

//开始直接使用afl-fuzz进行模糊测试，其中-i是种子文件所在的目录，-o是afl输出目录，--后面的是命令行的输入，例如如果你要启动之前的hello程序，你就使用/build/hello，就像平时从命令行启动程序一样
/AFLplusplus/afl-fuzz -i /seeds -o /afl-output -- /build/hello

//注意，这里默认将输出结果存储在/afl-output/default文件夹下。如果你想存在default外其它文件夹名称，可以用-M main或者-S variant1 等等，其中-M表示主模糊器，-S表示从模糊器，只能有一个主但可以有多个从，例如
/AFLplusplus/afl-fuzz -i /seeds -o /afl-output -M main -- /build/hello
/AFLplusplus/afl-fuzz -i /seeds -o /afl-output -S variant1 -- /build/hello
/AFLplusplus/afl-fuzz -i /seeds -o /afl-output -M variant2 -- /build/hello

//注意，如果想要同时执行多个模糊测试程序的话，这里在一个命令行界面中是不能同时执行的，因为执行的时候命令行控制权是不在的。官方文档提到的方法是使用screen命令，但是我们这个docker是精简版docker，没有提供这种功能。要想并行执行，一种方法是你可以打开多个宿主机的终端，然后分别进入这个同一个container去执行。注意同时执行的时候不要选择同一个output文件夹

//如果要指定多个存放种子的目录，可以添加多个-i参数，例如
/AFLplusplus/afl-fuzz -i /AFLplusplus/testcases/images/jpeg -i /src/testimages -o /afl-output -- /build/hello  


//此时应该就开始模糊测试了。使用ctrl+c停止测试
//可以在afl-output目录下查看运行结果。在/crash目录下存储的就是产生了错误的输入

//绘制统计图，前提是需要足够的数据，不然绘制不了。先创建一个存放绘制图的目录
mkdir /grap
cd /afl-output（/default）
//需要在包含 plot_data的目录下执行以下命令，一般就是之前-o指定的结果文件夹下
afl-plot . /grap

//此时会在/grap中存入图片和index.html。如果在docker中无法查看，可以使用以下命令在宿主机中执行，将docker中的文件复制到宿主机上；后面的.表示宿主机位置
docker cp container号:/grap/. .
```

一些其它的选项

```
//取消运行时的UI呈现，使用日志形式输出
export AFL_NO_UI=1
//重新使用UI（其它类似的也一样的取消方式）
unset AFL_NO_UI

//设置cache大小(MB)
export AFL_TESTCACHE_SIZE=250

//设置AFL在模糊测试结束时inx最终同步操作，在长时间模糊测试中很有用
export AFL_FINAL_SYNC=1
```

一些老师给出的待编译项目的编译方法（需要提前执行前面的export CC和CXX的命令）

- cxxfilt、readelf、nm-new、objdump：在项目文件夹下直接执行configure文件，输出可执行文件在binutils目录下
- djpeg：直接使用cmake一般流程，待测程序djpeg就在构建文件夹下。它可能需要多个种子目录，最简单的做法就是直接将一个目录下的文件复制到另一个目录里
- readpng：构建容器前将老师给的sh文件夹下的build_readpng.sh复制到项目目录下，进入容器然后先使用`export AFLPP=/AFLplusplus`命令指定afl目录，然后使用./build_readpng.sh执行。具体命令是`./build_readpng.sh . /build`。前者表示源代码目录，后者表示输出目录，需要先自己手动创建一个/build目录。此时可执行文件就在/build/readpng下。如果出现bash: ./build_readpng.sh: /bin/bash^M: bad interpreter: No such file or directory这种输出就是windows换行符问题，可以使用`sed -i 's/\r$//' build_readpng.sh`命令来解决
- mjs：和readpng一样，将老师给的sh文件夹下的build_mjs.sh复制到项目目录下，然后和readpng差不多的流程去做。出现的问题都可以参考readpng的构建
- lua：直接在源文件目录下执行make，构建的结果在当前的src目录下。在执行完前面的export CC和CXX的命令后，注意这里需要进入**/src/src**目录下，也就是存放一堆.c，.h文件的目录下，进入其中的makefile，将上面的CC那一行的gcc改为afl-cc，然后在回到**上一级**的另一个Makefile使用make命令编译。将测试文件需要从git上克隆，如果无法克隆可以先转移到宿主机，然后在测试文件所在目录下用`docker cp . container号:/seeds/.`将当前目录下的测试文件转移到docker中

其它的暂时还没试，不过应该都不难。判断有没有插桩成功你只要看看编译的时候有没有出现afl-cc编译时的输出就可以了。上面提到的可能也会出现一些问题，到时候碰到问题再解决吧。