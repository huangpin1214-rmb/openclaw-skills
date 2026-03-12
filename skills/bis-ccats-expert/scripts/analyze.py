#!/usr/bin/env python3
"""
BIS ECCN 分析工具
帮助分析芯片产品的出口管制分类
"""

import sys
import json

def analyze_3a090(product_info):
    """分析 3A090 先进计算控制"""
    risks = []
    excludes = []
    
    # 检查制程节点
    node = product_info.get('process_node', '').lower()
    if '16' in node or '14' in node or '10' in node or '7' in node or '5' in node:
        risks.append("制程节点 ≤16nm，可能触发 3A090")
    elif node:
        excludes.append(f"制程节点 {node} 不在先进节点范围")
    
    # 检查计算单元
    compute_units = product_info.get('compute_units', [])
    if any(u in compute_units for u in ['cpu', 'gpu', 'npu', 'dsp', 'fpga', 'accelerator']):
        risks.append("包含数字处理单元 (CPU/GPU/NPU/FPGA)")
    elif compute_units and 'none' not in compute_units:
        risks.append("包含计算单元")
    else:
        excludes.append("无数字处理单元")
    
    # 检查 AI/ML 功能
    ai_functions = product_info.get('ai_functions', [])
    if any(f in ai_functions for f in ['mac', 'vector', 'tensor', 'inference', 'training', 'ai']):
        risks.append("具有 AI/ML 相关功能 (MAC/向量/张量/推理)")
    
    # 检查 HBM
    if product_info.get('hbm', False):
        risks.append("支持 HBM，高带宽内存")
    else:
        excludes.append("不支持 HBM")
    
    # 检查 Chiplet
    if product_info.get('chiplet', False) or product_info.get('copackaged', False):
        risks.append("支持 Chiplet/共封装集成")
    
    # 检查数据中心定位
    datacenter = product_info.get('datacenter', False)
    if datacenter:
        risks.append("定位数据中心/服务器使用")
    else:
        excludes.append("非数据中心定位")
    
    # 检查 AI 营销
    ai_marketing = product_info.get('ai_marketing', False)
    if ai_marketing:
        risks.append("营销中包含 AI/HPC/服务器加速相关描述")
    
    # 判断：风险因素多于排除因素时才是 likely
    recommendation = 'unlikely_3a090'
    if len(risks) > len(excludes) and len(risks) > 0:
        recommendation = 'likely_3a090'
    elif len(risks) > 0:
        recommendation = 'possible_3a090'
    
    return {
        'risks': risks,
        'excludes': excludes,
        'recommendation': recommendation
    }

def analyze_5a002(product_info):
    """分析 5A002 加密控制"""
    risks = []
    excludes = []
    
    # 检查加密功能
    if product_info.get('encryption', False):
        enc_type = product_info.get('encryption_type', '')
        if enc_type in ['user_accessible', 'hardware', 'secure_boot', 'key_management']:
            risks.append(f"具有用户可访问加密功能: {enc_type}")
        else:
            risks.append("具有加密功能，需进一步评估")
    else:
        excludes.append("无加密功能")
    
    # 检查安全功能
    security = product_info.get('security_features', [])
    if any(s in security for s in ['secure_boot', 'tamper', '物理安全']):
        risks.append("具有安全功能")
    
    return {
        'risks': risks,
        'excludes': excludes,
        'recommendation': 'likely_5a002' if risks else 'unlikely_5a002'
    }

def analyze_3a001(product_info):
    """分析 3A001 特定集成电路"""
    # 3A001 包含多种特定类型的集成电路
    # 需要具体性能参数才能评估
    return {
        'risks': ['如满足特定性能参数可能受控'],
        'excludes': [],
        'recommendation': 'need_more_info'
    }

def analyze_ear99(product_info):
    """分析 EAR99"""
    # EAR99 是最不严格的分类
    
    # 排除其他 ECCN 后可以考虑 EAR99
    return {
        'criteria_met': [],
        'criteria_not_met': [],
        'recommendation': 'possible_ear99'
    }

def generate_classification_view(product_info):
    """生成初步分类观点"""
    
    results = {
        '3a090': analyze_3a090(product_info),
        '5a002': analyze_5a002(product_info),
        '3a001': analyze_3a001(product_info),
        'ear99': analyze_ear99(product_info)
    }
    
    # 总结
    summary = {
        'likely_eccn': [],
        'possible_eccn': [],
        'unlikely_eccn': [],
        'confidence': 'low'
    }
    
    for eccn, result in results.items():
        rec = result.get('recommendation', '')
        if 'likely' in rec and 'unlikely' not in rec:
            summary['likely_eccn'].append(eccn.upper())
        elif 'possible' in rec:
            summary['possible_eccn'].append(eccn.upper())
        else:
            summary['unlikely_eccn'].append(eccn.upper())
    
    # 计算置信度
    if len(summary['likely_eccn']) >= 2:
        summary['confidence'] = 'high'
    elif summary['possible_eccn']:
        summary['confidence'] = 'medium'
    
    return results, summary

def generate_missing_info_list(product_info):
    """生成缺失信息清单"""
    required = [
        ('product_name', '产品名称'),
        ('part_number', '型号/料号'),
        ('primary_function', '主要功能'),
        ('process_node', '制程节点'),
        ('package_type', '封装类型'),
        ('compute_units', '计算单元'),
        ('hbm', 'HBM 支持'),
        ('chiplet', 'Chiplet 支持'),
        ('encryption', '加密功能'),
        ('datacenter', '数据中心定位'),
    ]
    
    missing = []
    for field, name in required:
        if not product_info.get(field):
            missing.append(name)
    
    return missing

def main():
    if len(sys.argv) < 2:
        print("""
🔍 BIS ECCN 分析工具

用法:
  python3 analyze.py --part-number <型号> --function <功能> --node <节点> --compute <计算单元> --hbm <y/n> --datacenter <y/n> --encryption <y/n>

参数:
  --part-number       产品型号
  --function         主要功能 (compute/interface/power/control/other)
  --node             制程节点 (如 14nm, 28nm, 7nm)
  --compute          是否包含计算单元 (cpu/gpu/npu/dsp/fpga/none)
  --hbm              是否支持 HBM (y/n)
  --chiplet          是否支持 Chiplet (y/n)
  --datacenter       是否定位数据中心 (y/n)
  --ai-marketing     是否有 AI 营销 (y/n)
  --encryption       是否有加密功能 (y/n)

示例:
  python3 analyze.py --function interface --node 28nm --compute none --hbm n --datacenter n --encryption n
        """)
        return
    
    # 解析参数
    args = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith('--') and i + 1 < len(sys.argv):
            key = sys.argv[i][2:]
            value = sys.argv[i + 1]
            args[key] = value
            i += 2
        else:
            i += 1
    
    # 转换参数
    product_info = {
        'part_number': args.get('part-number', '未知'),
        'primary_function': args.get('function', 'other'),
        'process_node': args.get('node', ''),
        'compute_units': args.get('compute', 'none').split(',') if args.get('compute') else [],
        'hbm': args.get('hbm', 'n').lower() == 'y',
        'chiplet': args.get('chiplet', 'n').lower() == 'y',
        'copackaged': args.get('chiplet', 'n').lower() == 'y',
        'datacenter': args.get('datacenter', 'n').lower() == 'y',
        'ai_marketing': args.get('ai-marketing', 'n').lower() == 'y',
        'encryption': args.get('encryption', 'n').lower() == 'y',
    }
    
    print(f"\n📋 产品: {product_info['part_number']}")
    print(f"   功能: {product_info['primary_function']}")
    print(f"   节点: {product_info['process_node']}")
    print(f"   计算单元: {product_info['compute_units']}")
    print(f"   HBM: {product_info['hbm']}")
    print(f"   数据中心: {product_info['datacenter']}")
    print(f"   加密: {product_info['encryption']}")
    
    # 分析
    results, summary = generate_classification_view(product_info)
    missing = generate_missing_info_list(product_info)
    
    print(f"\n{'='*50}")
    print("📊 ECCN 分析结果")
    print(f"{'='*50}")
    
    for eccn, result in results.items():
        print(f"\n### {eccn.upper()}")
        if result.get('risks'):
            print("  ⚠️  风险因素:")
            for r in result['risks']:
                print(f"     - {r}")
        if result.get('excludes'):
            print("  ✅ 排除因素:")
            for e in result['excludes']:
                print(f"     - {e}")
    
    print(f"\n{'='*50}")
    print("📈 分类总结")
    print(f"{'='*50}")
    print(f"  可能 ECCN: {', '.join(summary['likely_eccn']) or '无'}")
    print(f"  待确认: {', '.join(summary['possible_eccn']) or '无'}")
    print(f"  不太可能: {', '.join(summary['unlikely_eccn']) or '无'}")
    print(f"  置信度: {summary['confidence']}")
    
    if missing:
        print(f"\n⚠️  缺失信息:")
        for m in missing:
            print(f"     - {m}")
    
    # CCATS 建议
    print(f"\n{'='*50}")
    print("💡 CCATS 申请建议")
    print(f"{'='*50}")
    
    if '3a090' in summary['likely_eccn'] or '5a002' in summary['likely_eccn']:
        print("  建议：考虑申请 CCATS 以获得官方分类确认")
    elif summary['confidence'] == 'low':
        print("  建议：收集更多技术信息后再评估")
    else:
        print("  建议：可能适用 EAR99，但建议咨询专业律师")

if __name__ == "__main__":
    main()
