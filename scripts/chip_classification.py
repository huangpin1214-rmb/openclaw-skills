#!/usr/bin/env python3
"""
芯片 EAR99 分类判断工具
用于判断芯片是否属于 EAR99 分类，或需要更严格的许可证要求
以及判断是否"不受 EAR 管辖"
"""

import json
import sys

# 常见芯片 ECCN 分类参考（简化版）
CHIP_ECCN_REFERENCE = {
    "3A001": {
        "name": "电子集成电路",
        "description": "特定参数的集成电路",
        "sub_categories": {
            "a.1": "辐射加固集成电路",
            "a.2": "存储芯片（超参数阈值）",
            "a.3": "微波/毫米波集成电路",
            "a.4": "模数转换器（超参数）",
            "a.5": "高性能集成电路（AI/GPU等）",
            "a.6": "射频/微波功率放大器",
            "a.7": "光纤相关集成电路",
            "a.9": "其他特定参数集成电路",
            "a.10": "多芯片模块",
            "a.11": "高速数据转换器",
            "a.12": "氮化镓/碳化硅基集成电路",
            "a.13": "集成芯片",
        },
    },
    "3A002": {
        "name": "通用集成电路",
        "description": "微处理器、存储芯片等通用集成电路",
    },
    "3A003": {
        "name": "定时/频率发生器",
        "description": "特定参数的时间/频率产生设备",
    },
    "3A991": {
        "name": "电子设备/组件（不控制）",
        "description": "不满足3A001参数的消费级/商业级芯片",
    },
    "EAR99": {
        "name": "未在CCL上列出的物品",
        "description": "不受其他ECCN管辖但仍受EAR管辖的物品",
    },
    "不受EAR管辖": {
        "name": "不受EAR管辖",
        "description": "不属于EAR管辖范围的物品，无需出口许可证",
    }
}

# 常见芯片的分类判断
COMMON_CHIP_CLASSIFICATIONS = {
    # AI/GPU - 需要许可证
    "nvidia_a100": {"eccn": "3A001.a.5", "status": "需要许可证", "note": "高性能计算芯片"},
    "nvidia_h100": {"eccn": "3A001.a.5", "status": "需要许可证", "note": "高性能计算芯片"},
    "nvidia_h20": {"eccn": "3A001.a.5", "status": "需要许可证", "note": "中国特供版，仍受控"},
    "intel_gaudi": {"eccn": "3A001.a.5", "status": "需要许可证", "note": "AI加速器"},
    
    # 存储芯片 - 视参数而定
    "hbm": {"eccn": "3A001.a.2", "status": "高带宽内存需许可", "note": "HBM2e及以上"},
    
    # 消费级芯片 - EAR99
    "stm32": {"eccn": "EAR99", "status": "消费级MCU", "note": "32位MCU一般EAR99"},
    "esp32": {"eccn": "EAR99", "status": "消费级IoT", "note": "WiFi+蓝牙芯片"},
    "intel_core": {"eccn": "EAR99", "status": "消费级CPU", "note": "消费级处理器"},
    "amd_ryzen": {"eccn": "EAR99", "status": "消费级CPU", "note": "消费级处理器"},
    
    # 中国特定
    "华为麒麟": {"eccn": "3A001", "status": "需具体型号", "note": "高端手机SoC可能受控"},
    "中芯国际": {"eccn": "3A001+实体清单", "status": "受严格限制", "note": "SMIC制造需许可"},
    "长江存储": {"eccn": "3A001.a.2+实体清单", "status": "已列入", "note": "YMTC受严格限制"},
}


def print_header():
    print("=" * 60)
    print("🔬 芯片 EAR99 分类判断工具")
    print("=" * 60)
    print()


def print_classification_guide():
    """打印分类判断指南"""
    print("📋 芯片 ECCN 分类判断指南")
    print("-" * 60)
    
    print("""
【完整判断流程 - 三层分类】

┌─────────────────────────────────────────────────────────────┐
│  第1层: 是否受 EAR 管辖? (§734.2)                            │
├─────────────────────────────────────────────────────────────┤
│  需要满足两个条件:                                          │
│    1. 发生了出口/再出口/转移(in-country)行为                │
│    2. 物品受 EAR 管辖                                        │
│                                                             │
│  不受 EAR 管辖的情况 (可以直接出口):                        │
│    ✓ 100% 非美国来源 (无美国元素)                           │
│    ✓ 在美国境外制造且不包含美国技术/软件                   │
│    ✓ 公开可获取的技术/软件 (publicly available)            │
│    ✓ 特定类别的物品 (见 §734.3)                            │
│                                                             │
│  → 如果"否": 不受 EAR 管辖，无需出口许可证                  │
│  → 如果"是": 继续 Step 2                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第2层: CCL 上是否有对应 ECCN?                              │
├─────────────────────────────────────────────────────────────┤
│  查 Commerce Control List (Part 774 Supplement 1)          │
│  常见芯片对应 ECCN:                                         │
│    - 3A001: 特定参数集成电路                               │
│    - 3A002: 通用集成电路                                   │
│    - 3A003: 定时/频率发生器                                │
│                                                             │
│  → 如果"是": 按该 ECCN 要求处理 (需要许可证)                │
│  → 如果"否": 继续 Step 3                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  第3层: EAR99 还是需要许可证?                               │
├─────────────────────────────────────────────────────────────┤
│  Step 3a: 是否为军事最终用途/用户?                          │
│    - §744.21 军事最终用途                                   │
│    - §744.22 军事最终用户 (Footnote 1)                     │
│    → 如果"是": 需要许可证                                   │
│                                                             │
│  Step 3b: 是否在实体清单上?                                 │
│    - 查 BIS Entity List (Part 764 Supplement 4)            │
│    → 如果"是": 需要许可证                                   │
│                                                             │
│  → 如果"否": EAR99 (仍需许可证，但按个案审查)               │
└─────────────────────────────────────────────────────────────┘

【不受 EAR 管辖的典型场景】

1. De Minimis 规则 (§734.4):
   - 美国含量 < 10% (非管制目的地)
   - 美国含量 < 25% (非苏联/非出售权国家)
   → 如果满足: 不受 EAR 管辖

2. 美国境外再出口:
   - 产品在美国境外生产
   - 不包含任何美国技术/软件
   → 如果满足: 不受 EAR 管辖

3. 公开可获取 (§734.7, §734.8):
   - 公开出版的技术/软件
   - 不涉及特定受控技术
   → 如果满足: 不受 EAR 管辖

4. 特定豁免:
   - 某些消费级产品
   - 某些政府间协议下的物品
   → 需要查具体规定

【分类结果总结】

┌────────────┬────────────────────┬────────────────────────────┐
│ 分类       │ 是否需要许可证    │ 说明                      │
├────────────┼────────────────────┼────────────────────────────┤
│ 不受EAR管辖│ ❌ 不需要          │ 不受EAR管辖，直接出口    │
│ 3A001等    │ ✅ 需要            │ CCL上有明确ECCN           │
│ EAR99      │ ⚠️ 需个案审查      │ 不在CCL上，但仍受管辖    │
│ 实体清单   │ ✅ 需要            │ 在实体清单上，需严格审查 │
└────────────┴────────────────────┴────────────────────────────┘
""")
    print()


def query_chip(chip_name):
    """查询芯片分类"""
    chip_lower = chip_name.lower()
    
    if chip_lower in COMMON_CHIP_CLASSIFICATIONS:
        info = COMMON_CHIP_CLASSIFICATIONS[chip_lower]
        print(f"🔍 查询: {chip_name}")
        print("-" * 40)
        print(f"  ECCN: {info['eccn']}")
        print(f"  状态: {info['status']}")
        print(f"  说明: {info['note']}")
        print()
        return
    
    found = False
    for key, info in COMMON_CHIP_CLASSIFICATIONS.items():
        if key in chip_lower or chip_lower in key:
            print(f"🔍 可能匹配: {key}")
            print("-" * 40)
            print(f"  ECCN: {info['eccn']}")
            print(f"  状态: {info['status']}")
            print(f"  说明: {info['note']}")
            print()
            found = True
    
    if not found:
        print(f"❓ 未找到 '{chip_name}' 的分类数据")
        print()
        print("=" * 60)
        print("📝 为准确定性，请提供以下信息：")
        print("=" * 60)
        print("""
【判断需要的信息】

1. 芯片型号/规格
   例如: CPU, GPU, MCU, FPGA, 存储芯片等

2. 生产地（关键！）
   例如: 美国/欧洲/中国/台湾/日本/韩国

3. 是否包含美国技术/软件？
   例如: 是/否/不确定

4. 出口目的地
   例如: 中国/俄罗斯/欧洲/美国

5. 最终用途
   例如: 消费电子/工业/超算/军工

6. 最终用户
   例如: 民营企业/科研机构/政府/军队
""")
        print("=" * 60)
        print("💡 示例查询:")
        print("   python3 chip_classification.py --interactive")
        print("=" * 60)


def show_eccn_list():
    """显示常见 ECCN 列表"""
    print("📦 常见芯片相关 ECCN 列表")
    print("-" * 60)
    
    for eccn, info in CHIP_ECCN_REFERENCE.items():
        print(f"\n【{eccn}】{info['name']}")
        print(f"  说明: {info['description']}")
        if 'sub_categories' in info:
            print("  子类:")
            for sub, desc in info['sub_categories'].items():
                print(f"    - {sub}: {desc}")
    
    print()


def interactive_mode():
    """交互式问答模式"""
    print()
    print("=" * 60)
    print("🔬 芯片 EAR99 分类判断 - 交互式问答")
    print("=" * 60)
    print()
    
    print("📝 请回答以下问题，以便我准确定性：")
    print("-" * 60)
    
    # Q1: 芯片类型
    print("\n【问题1】芯片类型是什么？")
    print("   例如: CPU, GPU, AI加速器, MCU, 存储芯片, FPGA, 射频芯片等")
    chip_type = input("   请输入: ").strip()
    
    # Q2: 生产地
    print("\n【问题2】芯片在哪里生产的？")
    print("   例如: 美国, 欧洲, 中国, 台湾, 日本, 韩国等")
    origin = input("   请输入: ").strip()
    
    # Q3: 美国技术含量
    print("\n【问题3】是否包含美国技术/软件/设备？")
    print("   例如: 是, 否, 不确定, <10%, >10%")
    us_tech = input("   请输入: ").strip()
    
    # Q4: 出口目的地
    print("\n【问题4】出口目的地是哪里？")
    print("   例如: 中国, 俄罗斯, 欧洲, 美国等")
    destination = input("   请输入: ").strip()
    
    # Q5: 最终用途
    print("\n【问题5】最终用途是什么？")
    print("   例如: 消费电子, 工业, 超算, 军工, 航天等")
    end_use = input("   请输入: ").strip()
    
    # Q6: 最终用户
    print("\n【问题6】最终用户是谁？")
    print("   例如: 民营企业, 科研机构, 政府, 军队等")
    end_user = input("   请输入: ").strip()
    
    # 分析判断
    print("\n" + "=" * 60)
    print("📊 分析结果")
    print("=" * 60)
    print()
    print(f"  芯片类型: {chip_type}")
    print(f"  生产地: {origin}")
    print(f"  美国技术: {us_tech}")
    print(f"  目的地: {destination}")
    print(f"  最终用途: {end_use}")
    print(f"  最终用户: {end_user}")
    print()
    print("-" * 60)
    
    # 判断逻辑
    result = analyze_classification(
        chip_type, origin, us_tech, destination, end_use, end_user
    )
    
    print()
    print("🎯 分类结果:")
    print("-" * 60)
    print(f"  {result['classification']}")
    print()
    print(f"  说明: {result['description']}")
    print()
    print(f"  许可证要求: {result['license']}")
    print()


def analyze_classification(chip_type, origin, us_tech, destination, end_use, end_user):
    """根据输入信息分析分类"""
    
    origin_lower = origin.lower()
    us_tech_lower = us_tech.lower()
    dest_lower = destination.lower()
    end_use_lower = end_use.lower()
    end_user_lower = end_user.lower()
    
    # 判断1: 是否受 EAR 管辖
    # 如果100%非美来源，且不含美技术
    if ("欧洲" in origin or "日本" in origin or "韩国" in origin or "台湾" in origin) and \
       ("否" in us_tech or "0%" in us_tech or "无" in us_tech):
        # 检查De Minimis
        if "中国" in destination or "俄罗斯" in destination:
            if "是" in us_tech or "不确定" in us_tech or ">" in us_tech:
                # 可能需要许可证
                pass
            else:
                return {
                    "classification": "🎉 不受 EAR 管辖",
                    "description": "100%非美来源，不含美国技术/软件，不受EAR管辖",
                    "license": "❌ 无需出口许可证"
                }
        else:
            return {
                "classification": "🎉 不受 EAR 管辖",
                "description": "100%非美来源，不含美国技术/软件，不受EAR管辖",
                "license": "❌ 无需出口许可证"
            }
    
    # 判断2: 军事用途/用户
    if "军工" in end_use_lower or "军事" in end_use_lower or \
       "军队" in end_user_lower or "军方" in end_user_lower or \
       "政府" in end_user_lower:
        return {
            "classification": "⚠️ 需要许可证 (军事用途/用户)",
            "description": "军事最终用途或最终用户，需要出口许可证",
            "license": "✅ 需要出口许可证 (可能推定拒绝)"
        }
    
    # 判断3: 超算/高性能计算
    if "超算" in end_use_lower or "高性能计算" in end_use_lower or \
       "ai" in chip_type.lower() or "gpu" in chip_type.lower() or \
       "加速器" in chip_type:
        return {
            "classification": "⚠️ 需要许可证 (3A001)",
            "description": "高性能集成电路，受 CCL 3A001 控制",
            "license": "✅ 需要出口许可证"
        }
    
    # 判断4: 检查是否在实体清单上（简化判断）
    entity_list_keywords = ["华为", "中芯", "smic", "长江存储", "ymtc", "浪潮", "新华三", "国防", "军工"]
    if any(kw in end_user_lower for kw in entity_list_keywords):
        return {
            "classification": "⚠️ 需要许可证 (实体清单)",
            "description": "最终用户在实体清单上或与军事相关",
            "license": "✅ 需要出口许可证 (严格审查)"
        }
    
    # 默认: EAR99
    return {
        "classification": "📋 EAR99",
        "description": "不在 CCL 上，但仍受 EAR 管辖，需个案审查",
        "license": "⚠️ 可能需要许可证 (个案审查)"
    }


def main():
    print_header()
    
    if len(sys.argv) == 1:
        print_classification_guide()
        print("\n【使用方式】")
        print("  python3 chip_classification.py <芯片型号>        # 快速查询")
        print("  python3 chip_classification.py --guide        # 显示判断指南")
        print("  python3 chip_classification.py --list        # 显示 ECCN 列表")
        print("  python3 chip_classification.py --interactive # 交互式问答")
        print()
        print("【示例】")
        print("  python3 chip_classification.py nvidia_h100")
        print("  python3 chip_classification.py stm32")
        print("  python3 chip_classification.py 华为麒麟")
        print()
        print("=" * 60)
        print("⚠️  首次使用请阅读上方判断指南，了解需要提供的信息")
        print("=" * 60)
    elif sys.argv[1] == "--guide":
        print_classification_guide()
    elif sys.argv[1] == "--list":
        show_eccn_list()
    elif sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        query_chip(sys.argv[1])


if __name__ == "__main__":
    main()