计算机有各种各样的交互接口，但为了充分利用计算机的能力，我们回到了文字接口：shell
试试ls
肯定很好奇他具体是怎么工作的,他的解析方式是：第一个单词是要执行的程序，之后的单词作为传递给程序的参数
目前很多东西不用去理解，这是一个探索的过程，只要知道他存在于这个环境中就好
echo 命令
echo $PATH
which echo
/bin/echo $PATH
":"是环境路径的分隔方式，换一个更好的方式
echo $PATH | tr ":" "\n"
cd pwd mkdir之类的

程序间创建连接
> |
通配
? *分别匹配一个或多个
{}公共字串，自动展开
eg:mv *.{py,sh} folder

常用情形：
# 查找所有名称为src的文件夹
find . -name src -type d
# 查找所有文件夹路径中包含test的python文件
find . -path '*/test/*.py' -type f
# 查找前一天修改的所有文件
find . -mtime -1
# 查找所有大小在500k至10M的tar.gz文件
find . -size +500k -size -10M -name '*.tar.gz'
# 删除全部扩展名为.tmp 的文件
find . -name '*.tmp' -exec rm {} \;


| 阶段 | 输入 | 输出 | GCC 选项 | 关键命令示例 | 文件内容 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **预处理** | `hello.c` | `hello.i` | `-E` | `gcc -E hello.c -o hello.i` | 纯文本 C 代码 |
| **编译** | `hello.i` | `hello.s` | `-S` | `gcc -S hello.i -o hello.s` | 汇编代码 |
| **汇编** | `hello.s` | `hello.o` | `-c` | `gcc -c hello.s -o hello.o` | 二进制目标代码 |
| **链接** | `hello.o` (+库) | `hello` | (无) | `gcc hello.o -o hello` | 最终可执行文件 |



strace -e trace=openat gcc -E hello.c -o hello.i 2>&1 | grep -v ENOENT



---

## 1. 查看程序如何使用环境变量

### 方法一：使用 `strace` 跟踪系统调用
```bash
# 查看程序读取环境变量的系统调用
strace -e trace=execve,getenv,getauxval ./your_program

# 或者更广泛地查看所有可能与环境变量相关的调用
strace -e trace=file ./your_program 2>&1 | grep -i env
```


### 方法三：查看进程的环境变量空间
```bash
# 查看任意运行中进程的环境变量
cat /proc/$(pidof your_program)/environ | tr '\0' '\n'

# 或者使用 strings 命令
strings /proc/$(pidof your_program)/environ
```



## 2. 查看程序如何接收命令行参数

### 方法一：使用 `strace` 观察程序启动
```bash
# 重点观察 execve 系统调用，它包含了参数和环境变量
strace -e trace=execve ./your_program arg1 arg2
```

**示例输出**：
```
execve("./your_program", ["./your_program", "arg1", "arg2"], 0x7ffd... /* 58 vars */) = 0
```
这里清楚显示了：
- 第一个参数：程序路径
- 第二个参数：参数数组
- 第三个参数：环境变量指针


### 方法三：在汇编级别观察
```bash
# 编译并查看汇编代码
gcc -S test_args.c
cat test_args.s

# 或者反汇编
objdump -d test_args | grep -A20 "<main>"
```

观察 main 函数如何接收参数：
- x86-64: `rdi` (argc), `rsi` (argv), `rdx` (envp)
- x86-32: 通过栈传递

### 方法四：使用 GDB 查看参数内存布局
```bash
gdb ./test_args
(gdb) break main
(gdb) run arg1 arg2
(gdb) print argc
(gdb) print argv[0]@argc  # 查看所有参数
(gdb) x/10s argv[0]       # 查看字符串内容
(gdb) x/20s envp[0]       # 查看环境变量
```

---


(base) ➜  26_recruit git:(main) ✗ env | grep /bin | tr ":" "\n"

(base) ➜  26_recruit git:(main) ✗ strace ./hello | grep -v '[A-Z]'


## 1. `/proc` 文件系统是什么？

### 1.1 基本概念
`/proc` 是一个**虚拟文件系统**（procfs），它不占用磁盘空间，而是内核数据的接口。通过读取 `/proc` 中的文件，可以获取系统和进程的实时信息。

### 1.2 `/proc` 的目录结构
```bash
# 查看 /proc 的主要内容
ls /proc/

# 典型内容：
1/     100/   101/   ...    # 数字目录代表进程ID
cpuinfo                     # CPU信息
meminfo                     # 内存信息
version                     # 内核版本
filesystems                 # 支持的文件系统
modules                     # 已加载的内核模块
mounts                      # 挂载信息
self                        # 当前进程的符号链接
thread-self                 # 当前线程的符号链接
```

## 2. 如何查看子进程的系统调用

### 2.1 使用 `strace -f` 跟踪子进程
```bash
# 跟踪进程及其所有子进程
strace -f -o trace.log bash -c "ls | wc -l"

# 只跟踪特定的系统调用
strace -f -e trace=execve,fork,clone bash -c "ls && pwd"

# 实时查看
strace -f -p <父进程PID>
```



## 3. `/proc` 中能获取的进程信息

### 3.1 进程基本信息
```bash
# 查看进程1（init进程）的信息
ls /proc/1/

# 重要文件：
cmdline     # 命令行参数
environ     # 环境变量
exe         # 执行文件链接
cwd         # 当前工作目录
fd/         # 打开的文件描述符
status      # 进程状态信息
statm       # 内存使用统计
maps        # 内存映射区域
```

### 3.2 实际查看示例
```bash
# 查看当前shell的信息
echo "当前Shell PID: $$"
ls /proc/$$/

# 查看进程状态
cat /proc/$$/status | head -20

# 查看内存映射
cat /proc/$$/maps | head -10

# 查看打开的文件
ls -la /proc/$$/fd/
```

## 4. 从 `/proc` 获取的具体信息类型

### 4.1 进程状态信息 (`/proc/pid/status`)
```bash
# 查看详细状态
cat /proc/$$/status

# 重要字段：
# Name:   进程名
# State:  运行状态（R-running, S-sleeping, Z-zombie）
# Pid:    进程ID
# PPid:   父进程ID
# Uid:    用户ID
# Gid:    组ID
# VmSize: 虚拟内存大小
# VmRSS:  物理内存使用
```

### 4.2 内存映射信息 (`/proc/pid/maps`)
```bash
# 查看内存布局
cat /proc/$$/maps

# 示例输出：
# 55a0a0b7a000-55a0a0b7c000 r--p 00000000 08:01 123456 /bin/bash
# 55a0a0b7c000-55a0a0bdf000 r-xp 00002000 08:01 123456 /bin/bash
# 55a0a0bdf000-55a0a0be3000 r--p 00085000 08:01 123456 /bin/bash
# 7ffd12345000-7ffd12366000 rw-p 00000000 00:00 0       [stack]

# 各字段含义：
# 地址范围       权限 偏移 设备  inode  文件路径
# start-end      perms offset dev inode pathname
```

### 4.3 文件描述符信息 (`/proc/pid/fd/`)
```bash
# 查看打开的文件
ls -la /proc/$$/fd/



## 6. 高级应用：调试多进程程序

### 6.1 跟踪特定的子进程
```bash
# 方法1：通过父进程跟踪所有子进程
strace -f -o all_children.log python3 -c "
import os
import time

def child():
    print(f'Child PID: {os.getpid()}')
    time.sleep(2)

if os.fork() == 0:
    child()
else:
    time.sleep(3)
"



## 7. `/proc` 中的系统级信息

### 7.1 系统状态监控
# CPU信息
cat /proc/cpuinfo | grep -E "processor|model name|cpu MHz"

# 内存信息
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable"

# 系统负载
cat /proc/loadavg

# 内核参数
cat /proc/sys/kernel/pid_max  # 最大PID值


cat /proc/3321/environ |tr "\0:" "\n"| less

# 硬件视角的操作系统
计算机就是一个电路，那他的初始状态是什么
firmware,
规定前512字节（也就是主引导扇区），如果最后两个字节是0x55和0xaa,就认为是可以启动的。那么firmware将他加载到0x7c00

printf '\xeb\xfe\x90%0.s' {1..509} | cat - <(printf '\x55\xaa') > mbr.bin && qemu-system-x86_64 -hda mbr.bin
