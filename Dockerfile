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
