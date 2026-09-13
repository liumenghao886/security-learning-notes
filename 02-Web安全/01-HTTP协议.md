# 01 · HTTP 协议基础

> 日期：2026-09-11 | 标签：#Web安全 #HTTP #基础

## 1. 为什么先学 HTTP

所有 Web 攻击（SQL 注入、XSS、越权等）本质上都是：**在 HTTP 请求中构造恶意内容，观察服务器如何响应**。不理解 HTTP 的结构，就无法读懂 Burp 抓到的数据，也无法构造测试载荷。

## 2. HTTP 是什么

HTTP 是客户端（浏览器 / Python 脚本）与服务器之间的**对话规则**，一次交互 = 一个请求 + 一个响应。

## 3. 请求结构

一次请求由三部分组成：

```http
GET /index.html HTTP/1.1
Host: www.baidu.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Cookie: name=value
#请求头和请求体要空行
username=admin&password=123
```

| 部分 | 说明 |
|---|---|
| 请求行 | 方法 + 路径 + HTTP 版本 |
| 请求头 | key: value 形式的附加信息，如 Host、User-Agent、Cookie |
| 请求体 | 提交的数据，GET 通常为空，POST 用于提交表单等 |

记忆：**行 → 头 → 体**

## 4. 响应结构

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: bfe

<!DOCTYPE html> ...
```

| 部分 | 说明 |
|---|---|
| 状态行 | 包含状态码，如 200 OK |
| 响应头 | 附加信息，如 Content-Type、Server、Set-Cookie |
| 响应体 | 实际返回的内容（HTML、JSON、文件等） |

## 5. 常见请求方法

| 方法 | 用途 | 数据位置 |
|---|---|---|
| GET | 获取数据（打开网页、查询） | 拼在 URL 上 |
| POST | 提交数据（登录、注册、上传） | 放在请求体中 |

登录必须使用 POST：GET 会把账号密码暴露在 URL 中，容易出现在浏览器历史与服务器日志里。**敏感数据不放在 URL 中**是一条基本原则。

## 6. 状态码

| 状态码 | 含义 |
|---|---|
| 200 | 成功，内容正常返回 |
| 301 / 302 | 重定向（跳转） |
| 401 | 未认证（需要登录） |
| 403 | 禁止访问（资源存在但无权限） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

口诀：**2 成功、3 跳转、4 客户端问题、5 服务器问题**。

安全测试中的用途：目录扫描时靠状态码判断资源是否存在——200 可访问、403 存在但禁止、404 不存在。

## 7. 实验一：用 Python 观察真实 HTTP

代码：`code/http1.py`

```python
import requests

resp = requests.get("https://www.baidu.com")
resp.encoding = "utf-8"

print("===== 发出的请求头 =====")
print(resp.request.headers)

print("===== 状态码 =====")
print(resp.status_code)

print("===== 服务器响应头 =====")
print(resp.headers)
```

运行结果（本机实测）：

- 状态码：200
- 响应头中可观察到 Content-Type、Server、Set-Cookie 等字段
## 实验二：伪装浏览器（修改User-Agent）
```python
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}
resp = requests.get("https://www.baidu.com", headers=headers)
print(resp.request.headers["User-Agent"])
```
- 在浏览器按F12->打开开发工具->Console(控制台)—>输入：navigator.userAgent
## 实验三：404实验
```python
import requests
resp=requests.get("https://www.baidu.com/abc123")
print("状态码：",resp.status_code) #应该是404
```
## 8. 安全视角

- **Server 响应头**可能泄露服务器软件及版本，攻击者可据此查找已知漏洞
- **Set-Cookie** 通常承载会话凭证，是身份认证相关攻击的重点目标
- 请求中的**参数、请求头、Cookie** 都是攻击者可构造的位置

## 9. 遇到的问题与复盘

- 一开始混淆了"请求"和"响应"的组成，实际为：
  - 请求 = 请求行 + 请求头 + 请求体
  - 响应 = 状态行 + 响应头 + 响应体
- 用 Python 打印 `resp.request.headers` 和 `resp.headers` 可以分别看到"我发的"和"服务器回的"，是理解 HTTP 最直观的方式

## 10. 参考资料

- MDN HTTP 文档：https://developer.mozilla.org/zh-CN/docs/Web/HTTP
- PortSwigger Web Security Academy：https://portswigger.net/web-security
