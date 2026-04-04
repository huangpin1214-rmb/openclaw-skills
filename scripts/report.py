#!/usr/bin/env python3
"""
生成 BIS 实体清单报告
"""

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
    "华为": {
        "en_name": "Huawei Technologies",
        "status": "已列入",
        "entities": [
            "Huawei Technologies Co., Ltd. (华为技术有限公司)",
            "Huawei Cloud (华为云)",
            "Huawei Device Co., Ltd.",
            "Huawei Digital Technologies (Suzhou) Co., Ltd.",
            "Shanghai Huawei Technologies Co., Ltd.",
            "更多子公司... (累计超100家关联实体被列入)"
        ],
        "footnote": "1, 3, 4",
        "date": "2019年5月16日（首批68家）\n2019年8月（追加46家）\n后续多次追加",
        "reason": "违反美国国家安全和外交政策；与伊朗交易；孟晚舟事件；获取美国技术用于军事用途",
        "source": "BIS Entity List - Multiple Rules",
        "additional_info": [
            "FootNote 1: 最严格限制，适用于军事最终用户",
            "FootNote 3:  presumption of denial（推定拒绝）",
            "FootNote 4: 涉及国家安全的实体，需严格审查",
            "特别限制：外国产品直接出口规则 (FDP Rule) 专门针对华为"
        ]
    }
}

def generate_report(company_name):
    data = COMPANY_DB.get(company_name)
    if not data:
        return f"未找到 {company_name} 的信息"
    
    print(f"\n{'='*70}")
    print(f"📋 {company_name} ({data['en_name']}) - BIS 实体清单查询报告")
    print(f"{'='*70}")
    
    # 状态
    status_emoji = {"已列入": "⚠️", "部分列入": "🔶", "未列入": "✅"}
    print(f"\n状态: {status_emoji.get(data['status'], '❓')} **{data['status']}**")
    
    # 实体列表
    if data.get('entities'):
        print(f"\n📋 列入实体（{len(data['entities'])}家）:")
        for i, e in enumerate(data['entities'], 1):
            print(f"   {i}. {e}")
    
    # 清单信息
    print(f"\n📋 清单信息:")
    print(f"   • 清单类型: EL (Entity List)")
    if data.get('footnote'):
        print(f"   • 脚注: {data['footnote']}")
    if data.get('date'):
        print(f"   • 列入时间: {data['date']}")
    if data.get('reason'):
        print(f"   • 列入原因: {data['reason']}")
    if data.get('source'):
        print(f"   • 信息来源: {data['source']}")
    
    # 额外信息
    if data.get('additional_info'):
        print(f"\n📌 特别说明:")
        for info in data['additional_info']:
            print(f"   • {info}")
    
    if data.get('note'):
        print(f"\n💡 {data['note']}")
    
    print(f"\n💡 BIS 官网: https://www.bis.gov/")
    print(f"{'='*70}")

if __name__ == "__main__":
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "华为"
    generate_report(company)
