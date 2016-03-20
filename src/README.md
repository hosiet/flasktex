# 说明

这里是重新编写的程序，相比较现在在`deprecated`目录下的代码
做了一些调整，但是大方向没有变。

## 设计想法

* 归根结底，调用服务器的`latexmk`进行工作
* 使用`SQLite`存储数据
* 尽量设计为客户端——服务器模式，为未来网页应用、客户端应用打基础
* 模块化

# API 设计

注：以下内容未经整理、未经确定。

e.g. (/flasktex)/api/1.0/

以上应当作为公共前缀。下面是实际使用的列表：

## 通用格式

返回的JSON的第一个`"success":`表示该请求的正常与否，后面的
`"status_string"`是对请求状态的说明性文字。

注意：Bundle 压缩文件格式为`tar.gz`，且使用`PAX tar`.

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

注：应当返回XML.

如果出错，返回标准500页面？（暂定）

正常情况下，返回202 Accepted

```
{
    "status": true,
    "status_string": "success",
    "worker_id": 5,/* only when success */
    "retrieve_id": asdv9324
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
            "timeout": 60,
            "entryfile": "main.tex"
        },
    "type": "separated",
    "files":
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
    ]
}
```

另一种方式也是传输被 targz 打包过后的文件与文件夹，与 xmlbundle 类似。
```
{
    "request":
        {
            "worker": "xelatex",
            "timeout": 60,
            "entryfile": "main.tex"
        },
    "type": "bundle",
    "content":
        {
            "content_type": "base64",
             "content": "BASE64 ENCODED TEXT"
        }
}
```

### 返回格式

和XMLBUNDLE相同

## 内容查询

### 工作状态查询

#### 请求格式

* GET `/api/1.0/result/<int:id>/status`

#### 返回格式


```
{
    "status":true,
    "status_string":"XXXX",
    "worker_status": "X" /* "R":running, "S":success, "F":failure, "N":nonexist */
}
```

### 结果查询

GET `/api/1.0/result/<int:id>/pdf?retrieve_id=<int:retrieve_id>`

Returns:

`Content-Disposition: inline; filename="output.pdf"`

Result may be:

200 OK for ok
202 Accepted for processing
403 Forbidden for wrong retrieve id
<!--410 Gone for deleted id-->
404 Not Found for non-existent record

暂时不支持断点续传。

## 其它操作
### 删除工作信息

DELETE `/api/1.0/result/<int:id>/pdf?retrieve_id=<int:retrieve_id>`

Results may be:

403 Forbidden for bad retrieve id
204 No Content for successful work
404 Not Found for non-existent record
#### 请求格式
#### 返回格式
