
## 编程逻辑

1. 在`/var/spool/flasktex`下面的子文件夹排列队列，等待处理。
2. 子目录的名称应当为当前UNIX时间的浮点数表示。
3. 加锁应当体现在子目录下的`.lock`文件，使用`fcntl`同时加锁。
4. 守护进程每1min自我唤醒一次（信号），也可以通过一个命名管道。
5. 命名管道为`/var/run/flasktex/wakeup`。
6. 守护进程pid文件应当为`/var/run/flasktex/flasktexd.pid`。
7. 管道写入以回车符`\n`为结尾的命令进行控制。`wakeup`进行一次扫描。
8. 限制只能由`www-data`用户写入文件，且无人可以读入该文件。
