#!/usr/bin/env python3
"""
BIS Entity List Checker v7 (bis-entity-check)
使用 Tavily API 查询公司是否在 BIS 实体清单上
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

# 内置公司数据库（已知公司，精确匹配）
COMPANY_DB = {
    "浪潮": {
        "en_name": "Inspur",
        "status": "已列入",
        "entities": [
            "Inspur (Beijing) Electronic Information Industry Co., Ltd.",
            "Inspur Electronic Information Industry Co., Ltd.",
            "Inspur Electronic Information (Hong Kong) Co., Ltd.",
            "Inspur (HK) Electronics Co., Ltd.",
            "Inspur Software Co., Ltd.",
            "Inspur Taiwan"
        ],
        "footnote": "4",
        "date": "2025年3月25/26日",
        "reason": "支持中国军事现代化/超级计算机开发",
        "license_policy": "推定拒绝（需逐案审查，2026年后松动）",
        "compliance_action": "触发合规审查流程",
        "source": "Federal Register 2025-05427"
    },
    "新华三": {
        "en_name": "H3C / New H3C",
        "status": "部分列入",
        "entities": [
            "New H3C Semiconductor Technologies Co., Ltd. (新华三半导体技术有限公司)"
        ],
        "footnote": "无",
        "date": "2024年12月",
        "reason": "获取美国原产物项用于支持中国军事现代化",
        "license_policy": "推定拒绝",
        "compliance_action": "触发合规审查流程（子公司已列入）",
        "source": "BIS December 2024"
    },
    "合肥长鑫": {
        "en_name": "CXMT / ChangXin Memory",
        "status": "未列入",
        "entities": [],
        "footnote": "-",
        "date": "-",
        "reason": "-",
        "license_policy": "正常审批",
        "compliance_action": "无需触发（未列入）",
        "source": "待核实"
    },
    "中芯国际": {
        "en_name": "SMIC",
        "status": "已列入",
        "entities": [
            "Semiconductor Manufacturing International Corporation (SMIC)"
        ],
        "footnote": "4",
        "date": "2020年12月",
        "reason": "与军事最终用户有关联",
        "license_policy": "推定拒绝（2026年后逐案审查）",
        "compliance_action": "触发合规审查流程",
        "source": "BIS"
    },
    "长江存储": {
        "en_name": "YMTC / Yangtze Memory",
        "status": "已列入",
        "entities": [
            "Yangtze Memory Technologies Co., Ltd."
        ],
        "footnote": "4",
        "date": "2022年12月",
        "reason": "获取先进半导体技术用于军事用途",
        "license_policy": "推定拒绝",
        "compliance_action": "触发合规审查流程",
        "source": "BIS"
    },
    "华为": {
        "en_name": "Huawei",
        "status": "已列入",
        "entities": [
            "Huawei Technologies Co., Ltd.",
            "Huawei Cloud",
            " Huawei Device Co., Ltd.",
            "更多子公司..."
        ],
        "footnote": "1, 3, 4",
        "date": "2019年5月",
        "reason": "违反美国国家安全/外交政策",
        "license_policy": "推定拒绝（最严格）",
        "compliance_action": "强烈建议触发合规审查（列入最早，脚注最多）",
        "source": "BIS"
    }
}

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

def parse_tavily_result(company_name, search_result):
    """从 Tavily 搜索结果中提取 BIS 信息"""
    answer = search_result.get("answer", "")
    results = search_result.get("results", [])
    
    # 判断是否在清单上
    status = "未知"
    entities = []
    footnote = ""
    date = ""
    reason = ""
    license_policy = ""
    compliance_action = ""
    
    # 简单关键词判断
    answer_lower = answer.lower()
    results_text = " ".join([r.get("content", "") for r in results]).lower()
    
    if "entity list" in answer_lower or "entity list" in results_text:
        if "added" in answer_lower or "added" in results_text or "2024" in answer or "2025" in answer or "2026" in answer:
            status = "已列入"
        elif "not on" in answer_lower or "not listed" in answer_lower or "removed" in answer_lower:
            status = "未列入"
        elif "footnote" in answer_lower:
            status = "已列入"
    
    # 提取脚注
    for r in results:
        content = r.get("content", "")
        if "footnote" in content.lower() and "entity" in content.lower():
            import re
            fn_match = re.search(r"Footnote\s*(\d+)", content, re.I)
            if fn_match:
                footnote = fn_match.group(1)
            break
    
    return {
        "company": company_name,
        "en_name": company_name,
        "status": status,
        "entities": entities,
        "footnote": footnote,
        "date": date or "待核实",
        "reason": reason or "请访问 BIS 官网确认",
        "license_policy": license_policy or "待核实",
        "compliance_action": compliance_action or "请手动判断",
        "note": "数据来自 Tavily 搜索，建议访问 BIS 官网核实"
    }

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
    
    # 优先使用内置数据库
    if company_name in COMPANY_DB:
        data = COMPANY_DB[company_name].copy()
        data['company'] = company_name  # 确保公司名正确显示
        data['search_time'] = today
        data['source'] = "内置数据库（精确）"
    else:
        # 动态搜索
        print(f"🔍 数据库未收录，动态查询: {company_name}")
        try:
            search_result = search_bis_tavily(company_name)
            data = parse_tavily_result(company_name, search_result)
            data['search_time'] = today
        except Exception as e:
            data = {
                "company": company_name,
                "en_name": company_name,
                "status": "查询失败",
                "entities": [],
                "footnote": "-",
                "date": "-",
                "reason": f"查询出错: {str(e)}",
                "license_policy": "-",
                "compliance_action": "无法判断，请手动查询",
                "note": "请访问 BIS 官网手动核实"
            }
    
    # 缓存
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

def judge_compliance(data):
    """判断是否需要触发合规流程"""
    status = data.get("status", "")
    footnote = data.get("footnote", "")
    compliance_action = data.get("compliance_action", "")
    
    if status == "已列入":
        return "⚠️ " + compliance_action
    elif status == "部分列入":
        return "🔶 " + compliance_action
    elif status == "未列入":
        return "✅ 无需触发合规流程"
    else:
        return "❓ 请手动判断"
    
def judge_license_policy(data):
    """判断许可证政策"""
    footnote = data.get("footnote", "")
    
    if footnote in ["1", "3", "4"]:
        return "推定拒绝（最严格，需充分理由）"
    elif footnote:
        return "逐案审查"
    else:
        return "正常审批"

def format_output(data):
    """格式化输出"""
    company = data.get('company', '')
    en_name = data.get('en_name', '')
    status = data.get('status', '未知')
    entities = data.get('entities', [])
    footnote = data.get('footnote', '-')
    date = data.get('date', '-')
    reason = data.get('reason', '-')
    license_policy = data.get('license_policy', '-')
    compliance_action = data.get('compliance_action', '-')
    source = data.get('source', '-')
    note = data.get('note', '')
    
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
    
    # 合规建议（醒目展示）
    if status in ["已列入", "部分列入"]:
        print(f"\n📌 合规建议: **{judge_compliance(data)}**")
    
    # 详细实体信息
    if entities:
        print(f"\n📋 具体实体:")
        for i, e in enumerate(entities, 1):
            print(f"   {i}. {e}")
    
    # 清单信息
    if status in ["已列入", "部分列入"]:
        print(f"\n📋 清单信息:")
        print(f"   • 清单类型: EL (Entity List)")
        print(f"   • 脚注: {footnote}")
        print(f"   • 列入时间: {date}")
        print(f"   • 列入原因: {reason}")
        print(f"   • 许可证政策: {judge_license_policy(data)}")
        print(f"   • 信息来源: {source}")
    
    if note:
        print(f"\n💡 {note}")
    
    print(f"\n🌐 BIS 官网查询: https://www.bis.gov/")
    print(f"{'='*70}")
    
    return data

def export_for_feishu(data):
    """导出适合飞书记录的格式"""
    return {
        "查询公司": data.get('company', ''),
        "英文名": data.get('en_name', ''),
        "状态": data.get('status', '未知'),
        "具体实体": "；".join(data.get('entities', [])) or "-",
        "脚注": data.get('footnote', '-'),
        "列入时间": data.get('date', '-'),
        "列入原因": data.get('reason', '-'),
        "许可证政策": judge_license_policy(data),
        "合规建议": judge_compliance(data),
        "查询时间": data.get('search_time', datetime.now().strftime('%Y-%m-%d')),
        "数据来源": data.get('source', 'Tavily 搜索')
    }

def main():
    force = '--refresh' in sys.argv
    companies = [c for c in sys.argv[1:] if c != '--refresh']
    
    if not companies:
        print("用法: python3 check_bis.py <公司名> [--refresh]")
        print("示例: python3 check_bis.py 浪潮 --refresh")
        print("内置公司:", list(COMPANY_DB.keys()))
        return
    
    print(f"\n🕐 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
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
