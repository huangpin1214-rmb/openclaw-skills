#!/usr/bin/env python3
"""
PCN 自检清单生成脚本
根据 PCN 类型生成对应的自检清单

用法: python3 pcn_checklist_gen.py [PCN类型]
PCN类型: all | 封装变更 | 代工厂变更 | 规格调整 | EOL停产
"""
import sys

TEMPLATES = {
    "封装变更": {
        "items": [
            "封装尺寸对比表（含新旧封装）",
            "封装兼容 性说明（Pin-to-Pin兼容）",
            "热参数对比（热阻、结温）",
            "可靠性测试报告摘要",
            "封装认证证书（如果是供应商变更）",
            "变更后样品照片",
            "包装/标识变更说明",
        ],
        "jedec_ref": "J-STD-046 第X.X条",
        "notes": "封装变更需重点关注form-fit-function兼容性"
    },
    "代工厂变更": {
        "items": [
            "新旧代工厂对比表",
            "制造工艺差异说明",
            "质量保证协议",
            "代工厂变更确认书",
            "可靠性测试报告（HTOL/TC/HAST等）",
            "晶圆厂认证状态",
            "封装厂认证状态（如适用）",
        ],
        "jedec_ref": "J-STD-046 第X.X条",
        "notes": "代工厂变更需确保品质一致性"
    },
    "规格调整": {
        "items": [
            "参数对比表（AC/DC参数）",
            "参数测试报告（ Bench characterization）",
            "规格收紧/放宽的影响评估",
            "是否需要客户承认的判断依据",
            "数据手册更新说明",
        ],
        "jedec_ref": "J-STD-046 第X.X条",
        "notes": "规格调整需评估对客户的影响"
    },
    "EOL停产": {
        "items": [
            "停产产品型号清单",
            "最后购买日期（Last-Time-Buy）",
            "LTB窗口时长建议",
            "替代产品/方案（如有）",
            "EOL生效日期",
            "售后服务承诺",
            "数据手册保留承诺（如适用）",
        ],
        "jedec_ref": "J-STD-048",
        "notes": "EOL需给客户足够的LTB窗口时间"
    }
}

def generate_checklist(pcn_type):
    if pcn_type == "all":
        for ptype, data in TEMPLATES.items():
            print(f"\n{'='*50}")
            print(f"📋 {ptype} 自检清单")
            print(f"{'='*50}")
            print(f"规范依据: {data['jedec_ref']}")
            print(f"说明: {data['notes']}")
            print()
            for i, item in enumerate(data['items'], 1):
                print(f"  {i}. [ ] {item}")
        return

    if pcn_type not in TEMPLATES:
        print(f"未知PCN类型: {pcn_type}")
        print(f"可用类型: {', '.join(TEMPLATES.keys())}, all")
        sys.exit(1)

    data = TEMPLATES[pcn_type]
    print(f"\n📋 {pcn_type} 自检清单")
    print(f"规范依据: {data['jedec_ref']}")
    print(f"说明: {data['notes']}")
    print()
    for i, item in enumerate(data['items'], 1):
        print(f"  {i}. [ ] {item}")
    print()

def main():
    pcn_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    generate_checklist(pcn_type)

if __name__ == "__main__":
    main()
