import dns.resolver
import dns.query
import dns.zone
import time
import os

# 读取域名列表
def read_domains(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# 获取域名的 NS 服务器
def get_ns_servers(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return []

# 尝试 DNS 域传送
def test_dns_transfer(domain, ns_server):
    try:
        xfr = dns.query.xfr(ns_server, domain, timeout=10)
        zone = dns.zone.from_xfr(xfr)
        if zone:
            records = "\n".join(zone.to_text().split("\n")[:20])  # 只显示前 20 行
            return f"✅ **成功**（部分记录）：\n<pre>{records}</pre>"
    except dns.exception.FormError:
        return "❌ **不允许域传送**（Transfer failed）"
    except dns.query.TransferError:
        return "❌ **传送失败**（可能被拒绝）"
    except dns.resolver.NoAnswer:
        return "❌ **没有返回 NS 记录**"
    except Exception as e:
        return f"⚠️ **未知错误**：{str(e)}"
    return "❌ **传送失败**（未知原因）"

# 生成 HTML 报告
def generate_html_report(results, output_file="dns_transfer_report.html"):
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>DNS 域传送测试报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .success {{ color: green; }}
            .fail {{ color: red; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; background: #f4f4f4; padding: 5px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h2>DNS 域传送测试报告</h2>
        <table>
            <tr>
                <th>域名</th>
                <th>NS 服务器</th>
                <th>测试结果</th>
            </tr>
            {results}
        </table>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✅] 测试完成，报告已生成：{output_file}")

# 主函数
def main():
    domains = read_domains("domains.txt")
    results = ""

    for domain in domains:
        ns_servers = get_ns_servers(domain)
        if not ns_servers:
            results += f"<tr><td>{domain}</td><td>❌ 获取失败</td><td class='fail'>无法解析 NS 记录</td></tr>\n"
            continue

        for ns_server in ns_servers:
            print(f"[🔍] 正在测试 {domain} 的 NS 服务器：{ns_server} ...")
            result = test_dns_transfer(domain, ns_server)
            results += f"<tr><td>{domain}</td><td>{ns_server}</td><td>{result}</td></tr>\n"
            time.sleep(1)  # 避免触发安全机制

    generate_html_report(results)

if __name__ == "__main__":
    main()

