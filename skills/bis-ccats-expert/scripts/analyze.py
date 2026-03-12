#!/usr/bin/env python3
"""
BIS ECCN 分类分析工具
帮助收集信息并生成初步分析
"""

import json
import sys

def analyze_3a090_risk(data):
    """分析 3A090 风险"""
    risk_score = 0
    factors = []
    
    # 制程节点
    node = data.get('process_node', '').lower()
    if '16nm' in node or '14nm' in node or '10nm' in node or '7nm' in node or '5nm' in node:
        risk_score += 3
        factors.append(f"先进制程节点: {node}")
    
    # 数字处理单元
    if data.get('has_digital_processing', False):
        risk_score += 3
        factors.append("包含数字处理单元")
    
    # 计算功能
    compute_funcs = data.get('compute_functions', [])
    high_risk_funcs = ['mac', 'vector', 'tensor', 'ai', 'inference', 'training', 'gpu', 'npu']
    for func in compute_funcs:
        if any(h in func.lower() for h in high_risk_funcs):
            risk_score += 2
            factors.append(f"高风险计算功能: {func}")
    
    # HBM 支持
    if data.get('has_hbm', False):
        risk_score += 3
        factors.append("支持 HBM")
    
    # Chiplet/共封装
    if data.get('has_chiplet', False):
        risk_score += 2
        factors.append("支持 Chiplet/共封装")
    
    # 数据中心定位
    datacenter = data.get('datacenter_marketing', False)
    if datacenter:
        risk_score += 3
        factors.append("数据中心/服务器营销")
    
    # AI/HPC 定位
    ai_marketing = data.get('ai_marketing', False)
    if ai_marketing:
        risk_score += 3
        factors.append("AI/HPC 营销定位")
    
    return risk_score, factors

def analyze_5a002_risk(data):
    """分析 5A002 加密风险"""
    risk_score = 0
    factors = []
    
    if data.get('has_encryption', False):
        risk_score += 4
        factors.append("包含加密功能")
        
        if data.get('encryption_user_accessible', False):
            risk_score += 2
            factors.append("用户可访问加密")
        
        if data.get('has_secure_boot', False):
            risk_score += 1
            factors.append("安全启动功能")
        
        if data.get('has_key_management', False):
            risk_score += 1
            factors.append("密钥管理功能")
    
    return risk_score, factors

def generate_preliminary_view(data):
    """生成初步分类观点"""
    results = {}
    
    # 3A090 分析
    score_3a090, factors_3a090 = analyze_3a090_risk(data)
    results['3A090'] = {
        'score': score_3a090,
        'factors': factors_3a090,
        'risk_level': '高' if score_3a090 >= 8 else ('中' if score_3a090 >= 4 else '低')
    }
    
    # 5A002 分析
    score_5a002, factors_5a002 = analyze_5a002_risk(data)
    results['5A002'] = {
        'score': score_5a002,
        'factors': factors_5a002,
        'risk_level': '高' if score_5a002 >= 5 else ('中' if score_5a002 >= 2 else '低')
    }
    
    return results

def print_analysis(data):
    """打印分析结果"""
    print("\n" + "="*60)
    print("🔍 BIS ECCN 初步分析")
    print("="*60)
    
    print(f"\n📋 产品: {data.get('product_name', 'N/A')} ({data.get('part_number', 'N/A')})")
    print(f"🔧 功能: {data.get('main_function', 'N/A')}")
    print(f"📊 制程: {data.get('process_node', 'N/A')}")
    print(f"🏢 定位: {data.get('market_positioning', 'N/A')}")
    
    results = generate_preliminary_view(data)
    
    print("\n" + "-"*60)
    print("📈 风险评估")
    print("-"*60)
    
    for eccn, result in results.items():
        print(f"\n【{eccn}】 风险等级: {result['risk_level']} (得分: {result['score']})")
        if result['factors']:
            for f in result['factors']:
                print(f"  • {f}")
        else:
            print("  ✓ 未发现风险因素")
    
    # CCATS 建议
    total_risk = results['3A090']['score'] + results['5A002']['score']
    
    print("\n" + "-"*60)
    print("📝 CCATS 申请建议")
    print("-"*60)
    
    if total_risk >= 10:
        print("⚠️  建议申请 CCATS - 高风险分类需要 BIs 确认")
    elif total_risk >= 5:
        print("🔸 建议深入分析 - 建议收集更多证据后决定")
    else:
        print("✓ 风险较低 - 可考虑 EAR99 或 3A991")
    
    print("\n" + "="*60)
    print("⚠️  注意：此分析仅供参考，不构成法律建议")
    print("="*60 + "\n")

def interactive_mode():
    """交互式问答模式"""
    print("\n🖥️  BIS ECCN 分类分析 - 交互模式")
    print("请回答以下问题（直接回车跳过）\n")
    
    data = {}
    
    data['product_name'] = input("产品名称: ").strip() or "N/A"
    data['part_number'] = input("型号/料号: ").strip() or "N/A"
    data['main_function'] = input("主要功能: ").strip() or "N/A"
    
    print("\n--- 技术规格 ---")
    data['process_node'] = input("制程节点 (如 7nm, 14nm): ").strip() or "未知"
    
    has_cpu = input("是否包含 CPU/GPU/NPU/DSP/FPGA? (y/n): ").strip().lower() == 'y'
    data['has_digital_processing'] = has_cpu
    
    compute_funcs = input("计算功能 (MAC/向量/张量/AI推理等，逗号分隔): ").strip()
    data['compute_functions'] = [f.strip() for f in compute_funcs.split(',')] if compute_funcs else []
    
    data['has_hbm'] = input("是否支持 HBM? (y/n): ").strip().lower() == 'y'
    data['has_chiplet'] = input("是否支持 Chiplet/共封装? (y/n): ").strip().lower() == 'y'
    
    print("\n--- 市场定位 ---")
    data['datacenter_marketing'] = input("是否定位数据中心/服务器? (y/n): ").strip().lower() == 'y'
    data['ai_marketing'] = input("是否定位 AI/HPC? (y/n): ").strip().lower() == 'y'
    data['market_positioning'] = "数据中心/AI" if data['datacenter_marketing'] or data['ai_marketing'] else "其他"
    
    print("\n--- 加密/安全 ---")
    data['has_encryption'] = input("是否包含加密功能? (y/n): ").strip().lower() == 'y'
    if data['has_encryption']:
        data['encryption_user_accessible'] = input("用户可访问加密? (y/n): ").strip().lower() == 'y'
        data['has_secure_boot'] = input("有安全启动? (y/n): ").strip().lower() == 'y'
        data['has_key_management'] = input("有密钥管理? (y/n): ").strip().lower() == 'y'
    
    print_analysis(data)

def main():
    if len(sys.argv) == 1:
        interactive_mode()
    elif sys.argv[1] == '--help':
        print("""
BIS ECCN 分类分析工具

用法:
  python3 analyze.py              # 交互模式
  python3 analyze.py --interactive  # 交互模式
  python3 analyze.py --sample       # 使用示例数据

或直接传入 JSON 数据:
  python3 analyze.py '{"process_node": "7nm", "has_digital_processing": true}'
        """)
    elif sys.argv[1] == '--sample':
        sample_data = {
            'product_name': '示例芯片',
            'part_number': 'SAMPLE-001',
            'main_function': '网络接口控制器',
            'process_node': '7nm',
            'has_digital_processing': True,
            'compute_functions': ['packet processing'],
            'has_hbm': False,
            'has_chiplet': False,
            'datacenter_marketing': True,
            'ai_marketing': False,
            'market_positioning': '数据中心',
            'has_encryption': False
        }
        print_analysis(sample_data)
    else:
        # 尝试解析 JSON
        try:
            data = json.loads(sys.argv[1])
            print_analysis(data)
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

if __name__ == "__main__":
    main()
