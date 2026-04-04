#!/usr/bin/env python3
"""
BIS Entity List Checker v8
使用 BIS 官方 Excel 数据（1069条中国实体）作为内置数据库
支持任意公司查询，自动记录到飞书 Bitable，包含合规流程判断
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime

API_KEY = "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"
CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/skills/bis-entity-check/cache/")
OFFICIAL_DB_FILE = os.path.join(CACHE_DIR, "bis_china_official_db.json")
ALIAS_MAP_FILE = os.path.join(CACHE_DIR, "chinese_alias_map.json")

# 加载 BIS 官方数据库
def load_official_db():
    """加载 BIS 官方数据库"""
    if os.path.exists(OFFICIAL_DB_FILE):
        with open(OFFICIAL_DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_alias_map():
    """加载中文别名映射"""
    if os.path.exists(ALIAS_MAP_FILE):
        with open(ALIAS_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

OFFICIAL_DB = load_official_db()
CHINESE_ALIAS = load_alias_map()

def search_bis_tavily(company_name):
    """使用 Tavily 搜索 BIS 相关信息"""
    query = f"{company_name} BIS entity list EAR site:bis.gov OR site:federalregister.gov"
    
    payload = json.dumps({
        "api_key": API_KEY,
        "query": query,
        "max_results": 5,
        "include_answer": True
    })
    
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())

def judge_compliance(data):
    """判断是否需要触发合规流程"""
    status = data.get("status", "")
    footnote = data.get("footnote", "")
    policy = data.get("policy", "")
    
    if status == "已列入":
        if "拒绝" in policy or "denial" in policy.lower():
            return "⚠️ 拒绝政策，建议强烈触发合规审查"
        elif "推定拒绝" in policy:
            return "⚠️ 推定拒绝，建议触发合规审查"
        else:
            return "⚠️ 建议触发合规审查"
    elif status == "部分列入":
        return "🔶 部分实体已列入，建议触发合规审查"
    elif status == "未列入":
        return "✅ 无需触发合规流程"
    else:
        return "❓ 请手动判断"

def check_entity(company_name, force_refresh=False):
    """检查公司是否在 BIS 实体清单上"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 缓存检查
    cache_file = os.path.join(CACHE_DIR, f"bis_{company_name}_{today}.json")
    
    if not force_refresh and os.path.exists(cache_file):
        print(f"📋 使用缓存: {company_name}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # 优先使用官方数据库
    result = None
    
    # 1. 精确匹配英文名
    if company_name in OFFICIAL_DB:
        result = OFFICIAL_DB[company_name].copy()
        result['company'] = company_name
        result['source'] = "BIS官方Excel数据（精确匹配）"
    # 2. 中文别名映射
    elif company_name in CHINESE_ALIAS:
        en_name = CHINESE_ALIAS[company_name]
        if en_name and en_name in OFFICIAL_DB:
            result = OFFICIAL_DB[en_name].copy()
            result['company'] = company_name
            result['source'] = f"BIS官方Excel数据（中文别名映射→{en_name}）"
        elif en_name is None:
            # 明确知道不在清单中
            result = {
                "company": company_name,
                "status": "未列入",
                "en_name": company_name,
                "footnote": "-",
                "date": "-",
                "reason": "明确不在BIS Entity List中",
                "policy": "正常审批",
                "search_time": today,
                "source": "中文别名映射确认"
            }
    # 3. 模糊匹配英文名
    else:
        for key, value in OFFICIAL_DB.items():
            if company_name.lower() in key.lower() or key.lower() in company_name.lower():
                result = value.copy()
                result['company'] = company_name
                result['source'] = f"BIS官方Excel数据（模糊匹配→{key}）"
                break
    
    if result:
        result['search_time'] = today
        # 确保字段完整
        result.setdefault('footnote', '-')
        result.setdefault('date', '-')
        result.setdefault('reason', '-')
        result.setdefault('policy', '-')
    else:
        # 动态搜索
        print(f"🔍 数据库未收录，动态查询: {company_name}")
        try:
            search_result = search_bis_tavily(company_name)
            answer = search_result.get("answer", "").lower()
            
            if "entity list" in answer and ("added" in answer or "202" in answer):
                status = "已列入"
            elif "not on" in answer or "not listed" in answer or "removed" in answer:
                status = "未列入"
            else:
                status = "未知"
            
            result = {
                "company": company_name,
                "status": status,
                "en_name": company_name,
                "footnote": "待核实",
                "date": "待核实",
                "reason": "请访问 BIS 官网确认",
                "policy": "待核实",
                "search_time": today,
                "source": "Tavily 搜索"
            }
        except Exception as e:
            result = {
                "company": company_name,
                "status": "查询失败",
                "en_name": company_name,
                "footnote": "-",
                "date": "-",
                "reason": f"查询出错: {str(e)}",
                "policy": "-",
                "search_time": today,
                "source": "Tavily 搜索失败"
            }
    
    # 缓存
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

def format_output(data):
    """格式化输出"""
    company = data.get('company', '')
    en_name = data.get('en_name', '')
    status = data.get('status', '未知')
    footnote = data.get('footnote', '-')
    date = data.get('date', '-')
    reason = data.get('reason', '-')
    policy = data.get('policy', '-')
    source = data.get('source', '-')
    
    status_emoji = {
        "已列入": "⚠️",
        "部分列入": "🔶",
        "未列入": "✅",
        "未知": "❓",
        "查询失败": "❌"
    }
    status_text = {
        "已列入": "已在 BIS 实体清单上",
        "部分列入": "部分实体已在清单上",
        "未列入": "未在 BIS 实体清单上",
        "未知": "状态未知，请手动核实",
        "查询失败": "查询失败，请手动核实"
    }
    
    print(f"\n{'='*70}")
    print(f"🔍 BIS 实体清单查询: {company}")
    print(f"{'='*70}")
    print(f"\n{status_emoji.get(status, '❓')} 状态: **{status_text.get(status, status)}**")
    
    # 合规建议
    print(f"\n📌 合规建议: **{judge_compliance(data)}**")
    
    # 详细信息
    if status in ["已列入", "部分列入"]:
        print(f"\n📋 清单信息:")
        print(f"   • 英文名: {en_name}")
        print(f"   • 列入时间: {date}")
        print(f"   • 许可审查政策: {policy}")
        if footnote and footnote != '-':
            print(f"   • 脚注: {footnote}")
        if reason and reason != '-':
            print(f"   • 列入原因: {reason}")
    
    print(f"\n📊 数据来源: {source}")
    print(f"\n🌐 BIS 官网查询: https://www.bis.gov/")
    print(f"{'='*70}")
    
    return data

def export_for_feishu(data):
    """导出适合飞书记录的格式"""
    return {
        "查询公司": data.get('company', ''),
        "英文名": data.get('en_name', ''),
        "状态": data.get('status', '未知'),
        "列入时间": data.get('date', '-'),
        "列入原因": data.get('reason', '-'),
        "许可证政策": data.get('policy', '-'),
        "脚注": data.get('footnote', '-'),
        "合规建议": judge_compliance(data),
        "查询时间": data.get('search_time', datetime.now().strftime('%Y-%m-%d')),
        "数据来源": data.get('source', 'Tavily 搜索')
    }

def main():
    force = '--refresh' in sys.argv
    companies = [c for c in sys.argv[1:] if c != '--refresh']
    
    if not companies:
        print("用法: python3 check_bis.py <公司名> [--refresh]")
        print(f"内置数据库: BIS官方Excel（{len(OFFICIAL_DB)}条记录）")
        print("示例: python3 check_bis.py 华为 --refresh")
        return
    
    print(f"\n🕐 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 数据库: BIS官方Excel（{len(OFFICIAL_DB)}条记录）")
    
    results = []
    for company in companies:
        try:
            data = check_entity(company.strip(), force_refresh=force)
            format_output(data)
            results.append(export_for_feishu(data))
        except Exception as e:
            print(f"❌ 查询失败: {company} - {e}")
    
    # 输出 JSON 格式供外部调用
    if results:
        print(f"\n📦 JSON 输出（供飞书记录用）:")
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
