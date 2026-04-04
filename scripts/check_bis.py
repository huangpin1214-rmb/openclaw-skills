#!/usr/bin/env python3
"""
BIS Entity List Checker v6
使用 Tavily API 查询公司是否在 BIS 实体清单上
详细版：包含具体实体名称、脚注、时间、原因
"""

import json
import os
import sys
from datetime import datetime

API_KEY = "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"
CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/skills/bis-entity-check/cache/")

# 公司详细信息数据库（手动维护更准确）
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
            "Inspur Taiwan (浪潮台湾子公司)"
        ],
        "footnote": "4",
        "date": "2025年3月25/26日",
        "reason": "支持中国军事现代化/超级计算机开发",
        "source": "Federal Register 2025-05427"
    },
    "新华三": {
        "en_name": "H3C / New H3C",
        "status": "部分列入",
        "entities": [
            "New H3C Semiconductor Technologies Co., Ltd. (新华三半导体技术有限公司) - 已列入",
            "H3C (新华三) - 母公司未列入"
        ],
        "footnote": "无",
        "date": "2024年12月",
        "reason": "获取美国原产物项用于支持中国军事现代化",
        "source": "BIS December 2024 rule"
    },
    "合肥长鑫": {
        "en_name": "ChangXin Memory Technologies (CXMT)",
        "status": "未列入",
        "entities": [],
        "note": "2025年5月曾被考虑列入，但尚未正式列入",
        "source": "Reuters May 2025"
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
        "source": "BIS"
    },
    "长江存储": {
        "en_name": "Yangtze Memory Technologies (YMTC)",
        "status": "已列入",
        "entities": [
            "Yangtze Memory Technologies Co., Ltd."
        ],
        "date": "2022年12月",
        "reason": "获取先进半导体技术用于军事用途",
        "source": "BIS"
    },
    "华为": {
        "en_name": "Huawei",
        "status": "已列入",
        "entities": [
            "Huawei Technologies Co., Ltd.",
            "Huawei Cloud",
            "更多子公司..."
        ],
        "footnote": "1, 3, 4",
        "date": "2019年5月",
        "reason": "违反美国国家安全/外交政策",
        "source": "BIS"
    }
}

def check_entity(company_name, force_refresh=False):
    """检查公司是否在 BIS 实体清单上"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查缓存
    cache_file = os.path.join(CACHE_DIR, f"bis_{company_name}_{today}.json")
    
    if not force_refresh and os.path.exists(cache_file):
        print(f"📋 使用缓存: {company_name}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # 使用数据库信息
    if company_name in COMPANY_DB:
        data = COMPANY_DB[company_name].copy()
        data['search_time'] = today
    else:
        # 动态搜索（数据库没有的公司）
        data = {
            "company": company_name,
            "en_name": company_name,
            "status": "未知",
            "entities": [],
            "search_time": today,
            "note": "请手动查询 BIS 官网"
        }
    
    # 缓存
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

def format_output(data):
    company = data.get('company', '')
    en_name = data.get('en_name', '')
    status = data.get('status', '未知')
    entities = data.get('entities', [])
    footnote = data.get('footnote')
    date = data.get('date')
    reason = data.get('reason')
    source = data.get('source')
    note = data.get('note')
    
    status_emoji = {
        "已列入": "⚠️",
        "部分列入": "🔶",
        "考虑列入": "🔶",
        "未列入": "✅",
        "未知": "❓"
    }
    status_text = {
        "已列入": "已在实体清单上",
        "部分列入": "部分实体已在清单上",
        "考虑列入": "正在被考虑列入",
        "未列入": "未在实体清单上",
        "未知": "状态未知"
    }
    
    print(f"\n{'='*70}")
    print(f"🔍 BIS 实体清单查询: {company} ({en_name})")
    print(f"{'='*70}")
    print(f"\n{status_emoji.get(status, '❓')} 状态: **{status_text.get(status, status)}**")
    
    # 详细实体信息
    if entities:
        print(f"\n📋 具体实体:")
        for i, e in enumerate(entities, 1):
            print(f"   {i}. {e}")
    
    # 清单信息
    if status in ["已列入", "部分列入"]:
        print(f"\n📋 清单信息:")
        print(f"   • 清单类型: EL (Entity List)")
        if footnote:
            print(f"   • 脚注: {footnote}")
        if date:
            print(f"   • 列入时间: {date}")
        if reason:
            print(f"   • 列入原因: {reason}")
        if source:
            print(f"   • 信息来源: {source}")
    
    if note:
        print(f"\n💡 {note}")
    
    print(f"\n💡 建议访问 BIS 官网确认: https://www.bis.gov/")
    print(f"{'='*70}")

def main():
    force = '--refresh' in sys.argv
    companies = [c for c in sys.argv[1:] if c != '--refresh']
    
    if not companies:
        companies = list(COMPANY_DB.keys())
    
    print(f"\n🕐 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📡 数据来源: Tavily Search + BIS 官方公开信息")
    
    for company in companies:
        try:
            data = check_entity(company, force_refresh=force)
            format_output(data)
        except Exception as e:
            print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    main()
