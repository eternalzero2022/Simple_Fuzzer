# 使用 ubuntu:22.04 作为基础镜像
FROM ubuntu:22.04

# 设置环境变量以避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装 make 和 build-essential
RUN sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirrors.ustc.edu.cn/ubuntu|g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y python3 python3-pip cmake libtool make build-essential llvm clang file binutils \
    && apt-get clean


RUN mkdir /SimpleFuzzer

# 设置工作目录
WORKDIR /SimpleFuzzer

# 复制当前目录的内容到 /SimpleFuzzer 目录
COPY . /SimpleFuzzer

# 安装 requirements.txt 中的依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV CC=/AFLplusplus/afl-cc
ENV CXX=/AFLplusplus/afl-cc

ENTRYPOINT ["/bin/bash"]
