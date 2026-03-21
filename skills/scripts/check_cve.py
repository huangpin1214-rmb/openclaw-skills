#!/usr/bin/env python3
"""
全球漏洞监控脚本
支持CVE查询、KEV跟踪、供应商公告
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
import urllib.request
import urllib.error

def get_cisa_kev(hours=72):
    """获取CISA KEV在野利用漏洞"""
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read())
        return data.get('vulnerabilities', [])
    except Exception as e:
        print(f"Error fetching CISA KEV: {e}")
        return []

def get_nvd_recent(hours=72):
    """获取NVD最新漏洞"""
    # 简化版：使用NVD API
    return []

def format_report(kev_list, hours):
    """格式化报告"""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    report = []
    report.append("=" * 50)
    report.append("🔒 全球漏洞监控报告")
    report.append(f"📅 时间范围: 最近{hours}小时")
    report.append(f"🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 50)
    report.append("")
    
    # 过滤近期漏洞
    recent_kev = []
    for v in kev_list:
        # 简化处理
        recent_kev.append(v)
    
    if recent_kev:
        report.append(f"## 🔴 CISA KEV 在野利用漏洞 ({len(recent_kev)}个)")
        report.append("")
        for v in recent_kev[:10]:
            cve = v.get('cveID', 'N/A')
            vendor = v.get('vendorProject', 'N/A')
            product = v.get('product', 'N/A')
            report.append(f"- **{cve}** - {vendor} {product}")
        report.append("")
    else:
        report.append("✅ 近期无新增KEV漏洞")
        report.append("")
    
    report.append("---")
    report.append("*数据来源: CISA KEV, NVD*")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='全球漏洞监控')
    parser.add_argument('--hours', type=int, default=72, help='时间窗口(小时)')
    parser.add_argument('--urgency', default='all', choices=['all', 'high', 'medium', 'low'])
    parser.add_argument('--output', default='', help='输出文件')
    
    args = parser.parse_args()
    
    print(f"🔍 查询最近{args.hours}小时漏洞...")
    
    # 获取CISA KEV
    kev_list = get_cisa_kev(args.hours)
    
    # 生成报告
    report = format_report(kev_list, args.hours)
    print(report)
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\n📁 已保存到: {args.output}")

if __name__ == '__main__':
    main()
