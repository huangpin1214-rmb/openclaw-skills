#!/usr/bin/env python3
"""
8D Report Generator
芯片 Fabless 公司客户问题 8D 报告生成工具
"""

import sys
import os

TEMPLATE = """
================================================================================
                         8D 问题分析报告
================================================================================

报告编号: {report_no}
报告日期: {report_date}
客户名称: {customer_name}
产品型号: {product_model}
批次号: {batch_no}

================================================================================
                              D0: 紧急措施
================================================================================
发现时间: {discovery_time}
问题现象: {issue_description}

围堵措施:
- 库存隔离: {inventory_quarantine}
- 在途追溯: {transit_trace}
- 客户端排查: {customer_check}

紧急程度: □紧急 □高 □中 □低

================================================================================
                              D1: 团队组建
================================================================================
8D 团队成员:

| 角色 | 姓名 | 部门 | 职责 |
|------|------|------|------|
| 组长 | {leader_name} | {leader_dept} | 统筹协调 |
| 技术 | {tech_name} | {tech_dept} | 技术分析 |
| 质量 | {quality_name} | {quality_dept} | 质量跟进 |
| 工程 | {engineering_name} | {engineering_dept} | 产线支持 |
| 市场 | {sales_name} | {sales_dept} | 客户沟通 |

================================================================================
                              D2: 问题描述
================================================================================
问题分类: □功能异常 □性能偏差 □可靠性 □外观 □包装 □其他

问题详细描述:
{issue_detail}

影响范围:
- 客户端不良数量: {customer_defect_qty}
- 客户端不良率: {customer_defect_rate}%
- 库存隔离数量: {quarantine_qty}
- 预估损失金额: {estimated_loss}

问题发生流程图:
{problem_flow}

================================================================================
                              D3: 临时措施
================================================================================
已采取的临时措施:

| 措施 | 实施日期 | 负责人 | 状态 |
|------|----------|--------|------|
| {temp_action_1} | {temp_date_1} | {temp_owner_1} | □完成 □进行中 |
| {temp_action_2} | {temp_date_2} | {temp_owner_2} | □完成 □进行中 |
| {temp_action_3} | {temp_date_3} | {temp_owner_3} | □完成 □进行中 |

临时措施效果评估:
{temp_effect}

================================================================================
                              D4: 根本原因分析
================================================================================
分析工具: □5Why □鱼骨图 □FTA □FMEA □其他

5Why 分析:
1. 为什么发生? {why1}
2. 为什么? {why2}
3. 为什么? {why3}
4. 为什么? {why4}
5. 根本原因: {root_cause}

鱼骨图分析:
- 人: {cause_man}
- 机: {cause_machine}
- 料: {cause_material}
- 法: {cause_method}
- 环: {cause_environment}

根本原因确认:
{root_cause_confirm}

================================================================================
                              D5: 长期措施
================================================================================
长期纠正措施:

| 措施 | 计划完成日期 | 负责人 | 验证方式 |
|------|--------------|--------|----------|
| {perm_action_1} | {perm_date_1} | {perm_owner_1} | {perm_verify_1} |
| {perm_action_2} | {perm_date_2} | {perm_owner_2} | {perm_verify_2} |
| {perm_action_3} | {perm_date_3} | {perm_owner_3} | {perm_verify_3} |

================================================================================
                              D6: 实施与验证
================================================================================
措施实施计划:

阶段1 (T+{stage1_days}天):
{stage1_plan}

阶段2 (T+{stage2_days}天):
{stage2_plan}

验证结果:
{verification_result}

效果确认:
{effect_confirmation}

================================================================================
                              D7: 预防措施
================================================================================
预防类似问题再次发生的措施:

1. 设计优化: {prevention_design}
2. 流程优化: {prevention_process}
3. 体系完善: {prevention_system}
4. 培训计划: {prevention_training}

================================================================================
                              D8: 团队认可
================================================================================
8D 关闭条件确认:

- □所有措施已完成并验证有效
- □客户对报告内容无异议
- □相关文档已归档

团队成员签字:

| 角色 | 签字 | 日期 |
|------|------|------|
| 组长 | _________ | _________ |
| 技术 | _________ | _________ |
| 质量 | _________ | _________ |
| 客户 | _________ | _________ |

报告状态: □待客户确认 □已关闭

================================================================================
                              附件清单
================================================================================
{attachments}

================================================================================
"""

def generate_8d_report(issue_info):
    """生成 8D 报告"""
    from datetime import datetime
    
    report_no = issue_info.get('report_no', f"8D-{datetime.now().strftime('%Y%m%d')}-001")
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    # 默认值
    data = {
        'report_no': report_no,
        'report_date': report_date,
        'customer_name': issue_info.get('customer_name', '【请填写】'),
        'product_model': issue_info.get('product_model', '【请填写】'),
        'batch_no': issue_info.get('batch_no', '【请填写】'),
        'discovery_time': issue_info.get('discovery_time', '【请填写】'),
        'issue_description': issue_info.get('issue_description', '【请填写】'),
        'inventory_quarantine': issue_info.get('inventory_quarantine', '待确认'),
        'transit_trace': issue_info.get('transit_trace', '待确认'),
        'customer_check': issue_info.get('customer_check', '待确认'),
        'leader_name': issue_info.get('leader_name', '【请填写】'),
        'leader_dept': issue_info.get('leader_dept', '【请填写】'),
        'tech_name': issue_info.get('tech_name', '【请填写】'),
        'tech_dept': issue_info.get('tech_dept', '【请填写】'),
        'quality_name': issue_info.get('quality_name', '【请填写】'),
        'quality_dept': issue_info.get('quality_dept', '【请填写】'),
        'engineering_name': issue_info.get('engineering_name', '【请填写】'),
        'engineering_dept': issue_info.get('engineering_dept', '【请填写】'),
        'sales_name': issue_info.get('sales_name', '【请填写】'),
        'sales_dept': issue_info.get('sales_dept', '【请填写】'),
        'issue_detail': issue_info.get('issue_detail', '【请填写】'),
        'customer_defect_qty': issue_info.get('customer_defect_qty', '0'),
        'customer_defect_rate': issue_info.get('customer_defect_rate', '0'),
        'quarantine_qty': issue_info.get('quarantine_qty', '0'),
        'estimated_loss': issue_info.get('estimated_loss', '0'),
        'problem_flow': issue_info.get('problem_flow', '【请填写】'),
        'temp_action_1': issue_info.get('temp_action_1', '【请填写】'),
        'temp_date_1': issue_info.get('temp_date_1', '【请填写】'),
        'temp_owner_1': issue_info.get('temp_owner_1', '【请填写】'),
        'temp_action_2': issue_info.get('temp_action_2', ''),
        'temp_date_2': issue_info.get('temp_date_2', ''),
        'temp_owner_2': issue_info.get('temp_owner_2', ''),
        'temp_action_3': issue_info.get('temp_action_3', ''),
        'temp_date_3': issue_info.get('temp_date_3', ''),
        'temp_owner_3': issue_info.get('temp_owner_3', ''),
        'temp_effect': issue_info.get('temp_effect', '【请填写】'),
        'why1': issue_info.get('why1', '【请填写】'),
        'why2': issue_info.get('why2', '【请填写】'),
        'why3': issue_info.get('why3', '【请填写】'),
        'why4': issue_info.get('why4', '【请填写】'),
        'root_cause': issue_info.get('root_cause', '【请填写】'),
        'cause_man': issue_info.get('cause_man', ''),
        'cause_machine': issue_info.get('cause_machine', ''),
        'cause_material': issue_info.get('cause_material', ''),
        'cause_method': issue_info.get('cause_method', ''),
        'cause_environment': issue_info.get('cause_environment', ''),
        'root_cause_confirm': issue_info.get('root_cause_confirm', '【请填写】'),
        'perm_action_1': issue_info.get('perm_action_1', '【请填写】'),
        'perm_date_1': issue_info.get('perm_date_1', '【请填写】'),
        'perm_owner_1': issue_info.get('perm_owner_1', '【请填写】'),
        'perm_verify_1': issue_info.get('perm_verify_1', '【请填写】'),
        'perm_action_2': issue_info.get('perm_action_2', ''),
        'perm_date_2': issue_info.get('perm_date_2', ''),
        'perm_owner_2': issue_info.get('perm_owner_2', ''),
        'perm_verify_2': issue_info.get('perm_verify_2', ''),
        'perm_action_3': issue_info.get('perm_action_3', ''),
        'perm_date_3': issue_info.get('perm_date_3', ''),
        'perm_owner_3': issue_info.get('perm_owner_3', ''),
        'perm_verify_3': issue_info.get('perm_verify_3', ''),
        'stage1_days': issue_info.get('stage1_days', '7'),
        'stage1_plan': issue_info.get('stage1_plan', '【请填写】'),
        'stage2_days': issue_info.get('stage2_days', '30'),
        'stage2_plan': issue_info.get('stage2_plan', '【请填写】'),
        'verification_result': issue_info.get('verification_result', '【请填写】'),
        'effect_confirmation': issue_info.get('effect_confirmation', '【请填写】'),
        'prevention_design': issue_info.get('prevention_design', '【请填写】'),
        'prevention_process': issue_info.get('prevention_process', '【请填写】'),
        'prevention_system': issue_info.get('prevention_system', '【请填写】'),
        'prevention_training': issue_info.get('prevention_training', '【请填写】'),
        'attachments': issue_info.get('attachments', '【请附上相关测试数据、分析报告等】'),
    }
    
    return TEMPLATE.format(**data)

def interactive_mode():
    """交互式生成 8D 报告"""
    print("\n" + "="*60)
    print("       8D 问题分析报告生成器 - 交互模式")
    print("="*60 + "\n")
    
    info = {}
    
    # 基本信息
    print("【基本信息】")
    info['customer_name'] = input("客户名称: ").strip()
    info['product_model'] = input("产品型号: ").strip()
    info['batch_no'] = input("批次号: ").strip()
    info['discovery_time'] = input("发现时间: ").strip()
    info['issue_description'] = input("问题描述: ").strip()
    
    print("\n【影响范围】")
    info['customer_defect_qty'] = input("客户端不良数量: ").strip()
    info['customer_defect_rate'] = input("客户端不良率(%): ").strip()
    info['quarantine_qty'] = input("隔离数量: ").strip()
    info['estimated_loss'] = input("预估损失金额: ").strip()
    
    print("\n【D1 团队成员】")
    info['leader_name'] = input("组长姓名: ").strip()
    info['leader_dept'] = input("组长部门: ").strip()
    info['tech_name'] = input("技术负责人: ").strip()
    info['tech_dept'] = input("技术部门: ").strip()
    
    print("\n【D4 根本原因分析 - 5Why】")
    info['why1'] = input("Why 1 (为什么发生?): ").strip()
    info['why2'] = input("Why 2: ").strip()
    info['why3'] = input("Why 3: ").strip()
    info['why4'] = input("Why 4: ").strip()
    info['root_cause'] = input("根本原因: ").strip()
    
    print("\n【D5 长期措施】")
    info['perm_action_1'] = input("长期措施1: ").strip()
    info['perm_date_1'] = input("计划完成日期: ").strip()
    info['perm_owner_1'] = input("负责人: ").strip()
    info['perm_verify_1'] = input("验证方式: ").strip()
    
    # 生成报告
    report = generate_8d_report(info)
    
    # 保存文件
    output_file = f"8D_Report_{info['customer_name']}_{info['product_model']}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已生成: {output_file}")
    print("\n" + "="*60)
    print(report)

def main():
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("""
8D Report Generator - 8D 问题分析报告生成器

用法:
  python3 generate_8d.py              # 交互模式
  python3 generate_8d.py --info       # 显示模板信息

输出:
  8D_Report_客户名_产品型号.txt
            """)
        else:
            print("生成 8D 报告...")
            report = generate_8d_report({})
            print(report)
    else:
        # 交互模式
        interactive_mode()

if __name__ == "__main__":
    main()
