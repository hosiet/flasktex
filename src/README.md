
## 编程逻辑：又一个历史想法

1. 在`/var/spool/flasktex`下面的子文件夹排列队列，等待处理。
2. 子目录的名称应当为当前UNIX时间的浮点数表示。
3. 加锁应当体现在子目录下的`.lock`文件，使用`fcntl`同时加锁。
4. 守护进程每1min自我唤醒一次（信号），也可以通过一个命名管道。
5. 命名管道为`/var/run/flasktex/wakeup`。
6. 守护进程pid文件应当为`/var/run/flasktex/flasktexd.pid`。
7. 管道写入以回车符`\n`为结尾的命令进行控制。`wakeup`进行一次扫描。
8. 限制只能由`www-data`用户写入文件，且无人可以读入该文件。

# Restful API 设计

e.g. (/flasktex)/api/1.0/

以上应当作为公共前缀。下面是实际使用的列表：

## 通用格式

返回的JSON的第一个`"success":`表示该请求的正常与否，后面的
`"status_string"`是对请求状态的说明性文字。

## 内容提交

### XMLBUNDLE提交

#### 请求格式

* POST `/submit/xmlbundle`

提交符合格式的XML字符串，格式如下：

```
<xmlbundle>
    <request>
        <worker>xelatex</worker>
        <timeout>60</timeout>
        <entryfile>main.tex</entryfile>
    </request>
    <bundle>BASE64_STR</bundle>
    <!-- 可能有多个文件 -->
</xmlbundle>
```

#### 返回格式

```
{
    "status": true,
    "status_string": "success",
    "worker_id": 5/* only when success */
}
```

### JSON提交

#### 请求格式

* POST `/submit/json`, `/submit`

```
{
    "request":
        {
            "worker": "xelatex",
            "timeout": 60
        },
    [
        {
            "file": "filename.tex",
            "content":
            {
                "content_type": "base64",
                "content": "BASE64 ENCODED TEXT"
            }
        },
        {}
}
```

### 返回格式

和XMLBUNDLE相同

## 内容查询

### 工作状态查询

#### 请求格式

* GET `/result/<int:id>/status`

#### 返回格式


```
{
    "status":true,
    "status_string":"XXXX",
    "worker_status": "X" /* "R":running, "S":success, "F":failure, "N":nonexist */
}
```

### 结果查询

## 其它操作
### 删除工作信息
#### 请求格式
#### 返回格式
