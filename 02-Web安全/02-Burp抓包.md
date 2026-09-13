# 02 · Burp Suite 抓包
> 日期：2026-9-13  | 标签：#Web安全 #BurpSuite #抓包 

## 1.今天学了什么
学会了怎么用burp拦截整个HTTP请求并修改浏览器与服务器的HTTP通信

## 2.什么是抓包
Burp可以作为中间人拦截浏览器发送给服务器的请求，并且可以修改和看

## 3.环境
工具：BurpSuit
方式：temporary project->next->默认设置->Start Burp

## 4.我的操作步骤
- 1.点击Proxy（代理）->Intercept on->Open browser->输入网址“https://baidu.com” ->
打不开->点击forward->打开网址
- 2.点HTTP history->选中状态码为200，点击鼠标右键->Send to Repeater
- Repeater（重放器） = 把信复印一份拿到自己桌上，可以随便涂改、反复寄出去，看对方怎么回

## 5.实验：修改请求路径
- 原始请求：（写 GET / HTTP/1.1）
- 修改为：（写 GET /abc123 HTTP/1.1）
- 结果：（状态码从 200 变成 404）
- 我的结论：（服务器找不到这个路径，所以返回 404）

## 6.我的理解
渗透测试的步骤：抓包->改包->重放->看反应

## 7.踩坑记录
1.Intercept is on 时网页打不开：因为请求被 Burp 拦住了，点 Forward 放行后页面才加载

## 8.下一步
学习SQL注入
