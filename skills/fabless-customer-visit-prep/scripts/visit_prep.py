#!/usr/bin/env python3
"""
Fabless客户拜访准备工具
帮助生成拜访记录、管理客户信息
"""

import os
import json
import sys
from datetime import datetime

CUSTOMER_DIR = os.path.expanduser("~/.openclaw/workspace/customers")

def create_visit_record(customer_name, visitor="", date=None):
    """创建拜访记录模板"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    customer_dir = os.path.join(CUSTOMER_DIR, customer_name)
    os.makedirs(customer_dir, exist_ok=True)
    
    filename = os.path.join(customer_dir, f"visit_{date}.md")
    
    content = f"""# 客户拜访记录 - {customer_name}

## 客户信息
- **公司名称**：{customer_name}
- **拜访人**：
- **拜访时间**：{date}

## 产品导入情况

| 产品型号 | 应用场景 | 用量 | 渠道 | 备注 |
|----------|----------|------|------|------|
|          |          |      |      |      |

## 历史问题

| 问题描述 | 发生时间 | 处理状态 | 客诉单号 | 备注 |
|----------|----------|----------|----------|------|
|          |          |          |          |      |

## 新项目需求

| 项目名称 | 产品需求 | 用量预测 | 时间节点 | 备注 |
|----------|----------|----------|----------|------|
|          |          |          |          |      |

## 质量要求

- **质量标准** (AQL/PPM)：
- **可靠性要求**：
- **客诉响应时效**：

## 竞争情况

- **竞争对手**：
- **客户评价**：

## 商务与供应

- **价格预期**：
- **供货要求**：
- **代理渠道**：

## 环保/合规

- **环保标准**：
- **原产地要求**：

## 拜访纪要

### 客户反馈

### 讨论要点

## 待跟进事项

- [ ]

## 下次拜访计划

- 日期：
- 目的：
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建拜访记录: {filename}")
    return filename

def list_customers():
    """列出所有客户"""
    if not os.path.exists(CUSTOMER_DIR):
        print("暂无客户记录")
        return
    
    customers = [d for d in os.listdir(CUSTOMER_DIR) 
                 if os.path.isdir(os.path.join(CUSTOMER_DIR, d))]
    
    if not customers:
        print("暂无客户记录")
        return
    
    print(f"\n已有 {len(customers)} 个客户:\n")
    for c in sorted(customers):
        print(f"  • {c}")

def list_visits(customer_name):
    """列出某客户的拜访记录"""
    customer_dir = os.path.join(CUSTOMER_DIR, customer_name)
    
    if not os.path.exists(customer_dir):
        print(f"未找到客户: {customer_name}")
        return
    
    visits = [f for f in os.listdir(customer_dir) if f.startswith('visit_')]
    
    if not visits:
        print(f"暂无拜访记录: {customer_name}")
        return
    
    print(f"\n{customer_name} 拜访记录:\n")
    for v in sorted(visits):
        print(f"  • {v.replace('visit_', '').replace('.md', '')}")

def main():
    if len(sys.argv) < 2:
        print("""
📋 Fabless客户拜访准备工具

用法:
  python3 visit_prep.py new <客户名称>              新建拜访记录
  python3 visit_prep.py list                         列出所有客户
  python3 visit_prep.py visits <客户名称>            列出客户拜访记录

示例:
  python3 visit_prep.py new "华为技术"
  python3 visit_prep.py list
  python3 visit_prep.py visits "华为技术"
        """)
        return
    
    command = sys.argv[1]
    
    if command == "new":
        if len(sys.argv) < 3:
            print("请输入客户名称")
            sys.exit(1)
        customer = sys.argv[2]
        create_visit_record(customer, "")
    
    elif command == "list":
        list_customers()
    
    elif command == "visits":
        if len(sys.argv) < 3:
            print("请输入客户名称")
            sys.exit(1)
        list_visits(sys.argv[2])
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
