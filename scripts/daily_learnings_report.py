#!/usr/bin/env python3
"""
每日学习记录总结推送脚本
检查 .learnings 目录下文件的变更，推送总结报告

运行方式:
  python3 daily_learnings_report.py

依赖:
  - 上一次的状态存储在 ~/.openclaw/workspace/.learnings/.last_report.json
  - 推送使用飞书机器人 webhook 或直接发消息
"""
import os
import json
import hashlib
from datetime import datetime

LEARNINGS_DIR = os.path.expanduser("~/.openclaw/workspace/.learnings")
LAST_REPORT_FILE = os.path.join(LEARNINGS_DIR, ".last_report.json")
STATE_FILE = os.path.join(LEARNINGS_DIR, ".file_states.json")

FILES_TO_CHECK = ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]

def get_file_state(filepath):
    """获取文件状态：修改时间 + MD5"""
    if not os.path.exists(filepath):
        return None
    mtime = os.path.getmtime(filepath)
    with open(filepath, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    return {"mtime": mtime, "md5": md5, "size": os.path.getsize(filepath)}

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def read_file_diff(filepath, since_mtime=None):
    """读取文件内容，可选只读取新增部分"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if since_mtime is None:
        return content
    # 简化处理：返回完整内容（实际可优化为只读新增行）
    return content

def build_report(new_states, old_states, last_report_time):
    """构建报告内容"""
    lines = []
    lines.append("📋 每日学习记录总结")
    lines.append(f"推送时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    has_changes = False
    for fname in FILES_TO_CHECK:
        filepath = os.path.join(LEARNINGS_DIR, fname)
        old = old_states.get(fname)
        new = new_states.get(fname)
        
        if old is None and new is not None:
            # 新文件
            has_changes = True
            lines.append(f"🆕 {fname} [新增文件]")
            content = read_file_diff(filepath)
            if content:
                lines.append(f"  记录数: {len(content.split(chr(10)))} 行")
        elif new is not None and old is None:
            has_changes = True
            lines.append(f"🆕 {fname} [首次检测]")
            content = read_file_diff(filepath)
            if content:
                lines.append(f"  记录数: {len(content.split(chr(10)))} 行")
        elif new and old and new["md5"] != old["md5"]:
            # 有变更
            has_changes = True
            lines.append(f"📝 {fname} [有更新]")
            content = read_file_diff(filepath)
            if content:
                lines.append(f"  记录数: {len(content.split(chr(10)))} 行")
        else:
            lines.append(f"➖ {fname} [无变化]")
    
    lines.append("")
    if not has_changes:
        lines.append("今日 .learnings 文件无新增变更。")
    else:
        lines.append("请查阅 .learnings 目录了解详情。")
    
    return "\n".join(lines), has_changes

def main():
    # 获取当前状态
    current_state = {}
    for fname in FILES_TO_CHECK:
        filepath = os.path.join(LEARNINGS_DIR, fname)
        state = get_file_state(filepath)
        if state:
            current_state[fname] = state
    
    # 加载上次状态
    old_state = load_last_state()
    
    # 生成报告
    report, has_changes = build_report(current_state, old_state, None)
    
    # 输出报告（供调用方处理）
    print(report)
    print(f"__HAS_CHANGES__:{has_changes}")
    
    # 保存状态
    save_state(current_state)

if __name__ == "__main__":
    main()
