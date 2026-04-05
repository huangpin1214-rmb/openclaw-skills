#!/usr/bin/env python3
"""
PCN 客户反馈追踪与 Checklist 迭代脚本

当用户反馈"客户说缺少XX信息"时，使用此脚本记录反馈，
并自动更新自检清单。

用法:
  python3 pcn_feedback_tracker.py add "<反馈内容>"
  python3 pcn_feedback_tracker.py list
  python3 pcn_feedback_tracker.py update-checklist
"""
import sys
import os
from datetime import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback_log.md")
CHECKLIST_UPDATES_FILE = os.path.join(os.path.dirname(__file__), "checklist_updates.md")

def add_feedback(content):
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- 反馈: {content}\n")
    print(f"✅ 已记录反馈: {content}")

def list_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        print("暂无反馈记录")
        return
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        print(f.read())

def update_checklist():
    if not os.path.exists(FEEDBACK_FILE):
        print("暂无反馈，无法更新清单")
        return
    print("请告诉我：")
    print("1. 反馈对应的检查项编号")
    print("2. 如何更新该检查项")
    print("\n示例: 编号3更新为'变更描述（含新旧版本参数对比表）— 已根据客户反馈优化'")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add":
        if len(sys.argv) < 3:
            print("用法: add \"<反馈内容>\"")
            sys.exit(1)
        add_feedback(sys.argv[2])
    elif cmd == "list":
        list_feedback()
    elif cmd == "update-checklist":
        update_checklist()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
