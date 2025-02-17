# DNS Transfer Test

## 介绍

该脚本用于批量测试目标域名是否存在 DNS 域传送漏洞 (Zone Transfer)。

DNS 域传送漏洞可能导致攻击者获取域名的完整 DNS 记录，从而泄露敏感信息，如子域名、服务器 IP、邮件服务器等。

## 功能

- 读取 `domains.txt` 文件中的域名列表。
- 查询域名的 NS（Name Server）记录。
- 尝试对每个 NS 服务器执行 AXFR（DNS Zone Transfer）。
- 结果保存为 `dns_transfer_result.html`。

## 依赖环境

- Python 3.x
- `dnspython` 库

### 安装依赖：
```bash
pip install dnspython
```

## 使用方法

### 1. 准备域名列表文件

创建 `domains.txt` 文件，输入要测试的域名，每行一个，例如：

```
example.com
test.com
vulnerable-site.com
```

### 2. 运行脚本

运行以下命令来执行 DNS 域传送测试：

```bash
python dns_transfer_test.py
```

### 3. 查看测试结果

运行成功后，会在当前目录生成 `dns_transfer_result.html` 文件，可以在浏览器中打开该文件查看测试结果。

## 结果说明

- **成功**：域名存在 DNS 域传送漏洞，能够获取到完整的 DNS 记录。
- **失败**：域传送被拒绝，说明该域名未受影响。
- **NS 解析失败**：无法解析该域名的 NS 记录，可能是域名不存在或 DNS 解析错误。

## 示例输出

### 终端示例

```bash
$ python dns_transfer_test.py
[+] 正在测试 example.com
    -> NS 服务器: ns1.example.com
    -> 尝试 AXFR 传送...
    -> 成功！发现 50 条 DNS 记录

[+] 正在测试 test.com
    -> NS 服务器: ns1.test.com
    -> 尝试 AXFR 传送...
    -> 失败，域传送被拒绝
```

### HTML 报告示例

```html
<!DOCTYPE html>
<html>
<head><title>DNS 域传送测试结果</title></head>
<body>
<h2>DNS 域传送测试结果</h2>
<table border="1">
<tr><th>域名</th><th>NS 服务器</th><th>测试结果</th></tr>
<tr><td>example.com</td><td>ns1.example.com</td><td style='color: red;'>成功！获取到 50 条记录</td></tr>
<tr><td>test.com</td><td>ns1.test.com</td><td style='color: green;'>失败，域传送被拒绝</td></tr>
</table>
</body>
</html>
```

## 免责声明

该工具仅供安全研究和渗透测试用途，请勿用于非法目的！使用本工具造成的任何法律责任由用户自行承担。
