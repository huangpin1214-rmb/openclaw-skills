#!/usr/bin/env python3
"""
幼儿教育教具方案生成器
根据预算自动推荐产品组合
"""

import json
import sys
import os

# 产品数据库路径
DB_PATH = os.path.expanduser('~/.openclaw/workspace/knowledge/tts-products.json')

def load_products():
    """加载产品数据库"""
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('products', [])
    except FileNotFoundError:
        print(f"❌ 产品数据库未找到: {DB_PATH}")
        return []
    except json.JSONDecodeError:
        print("❌ 产品数据库格式错误")
        return []

def filter_by_age(products, age_range):
    """根据年龄筛选产品"""
    if not age_range:
        return products
    
    age_mapping = {
        '0-3': (0, 3),
        '1-3': (1, 3),
        '2-4': (2, 4),
        '3-6': (3, 6),
        '4-7': (4, 7),
        '5-8': (5, 8),
        '6-9': (6, 9),
    }
    
    if age_range in age_mapping:
        min_age, max_age = age_mapping[age_range]
        filtered = []
        for p in products:
            age = p.get('age', '')
            # 简单判断 - 如果标注年龄包含相关数字
            if str(min_age) in age or str(max_age) in age or '3至' in age:
                filtered.append(p)
        return filtered
    return products

def filter_by_category(products, category):
    """根据分类筛选产品"""
    if not category:
        return products
    return [p for p in products if category in p.get('category', '')]

def filter_by_budget(products, budget):
    """根据预算筛选产品"""
    return [p for p in products if p.get('price', 0) <= budget]

def select_products_by_budget(products, budget, categories=None):
    """
    根据预算选择最佳产品组合
    策略：优先选择不同分类的核心产品
    """
    if categories is None:
        categories = ['数学学习', '配对学习', '户外教学', '重量和尺寸', '形状认知', '音乐系列']
    
    selected = []
    remaining_budget = budget
    
    # 按分类选择产品
    used_categories = set()
    
    # 先选择有价格的产品
    priced_products = [p for p in products if p.get('price', 0) > 0]
    
    # 核心产品优先级
    core_skus = ['TCBMA02690', 'TCBEY04785', 'TCBEY10200', 'TCBEY11335', 'TCBMOUTDOORS', 'TCBEY10642']
    
    for sku in core_skus:
        for p in priced_products:
            if p['sku'] == sku and remaining_budget >= p['price']:
                selected.append(p)
                remaining_budget -= p['price']
                break
    
    # 继续添加其他产品直到预算用完
    for p in priced_products:
        if p in selected:
            continue
        if remaining_budget >= p['price']:
            selected.append(p)
            remaining_budget -= p['price']
    
    return selected, remaining_budget

def generate_plan(age_range, budget, category=None, plan_name="教具采购方案"):
    """生成采购方案"""
    products = load_products()
    
    if not products:
        return None
    
    # 筛选
    if age_range:
        products = filter_by_age(products, age_range)
    if category:
        products = filter_by_category(products, category)
    
    # 选择产品
    selected, remaining = select_products_by_budget(products, budget)
    
    # 计算总价
    total = sum(p.get('price', 0) for p in selected)
    
    return {
        'name': plan_name,
        'age_range': age_range,
        'budget': budget,
        'category': category,
        'products': selected,
        'total': total,
        'remaining': remaining
    }

def format_plan(plan):
    """格式化方案输出"""
    if not plan:
        return "❌ 无法生成方案"
    
    output = []
    output.append(f"\n{'='*50}")
    output.append(f"📚 {plan['name']}")
    output.append(f"{'='*50}")
    
    if plan['age_range']:
        output.append(f"\n👶 目标年龄: {plan['age_range']}岁")
    output.append(f"💰 预算: ¥{plan['budget']}")
    if plan['category']:
        output.append(f"📂 分类: {plan['category']}")
    
    output.append(f"\n{'='*50}")
    output.append("📦 推荐产品")
    output.append(f"{'='*50}")
    
    if not plan['products']:
        output.append("\n暂无符合条件的产品")
    else:
        output.append(f"\n{'序号':<4} {'货号':<15} {'产品名称':<25} {'单价':<8}")
        output.append("-" * 60)
        
        for i, p in enumerate(plan['products'], 1):
            name = p.get('name', '')[:24]
            sku = p.get('sku', '')
            price = p.get('price', 0)
            output.append(f"{i:<4} {sku:<15} {name:<25} ¥{price}")
    
    output.append(f"\n{'='*50}")
    output.append(f"💵 预算合计: ¥{plan['total']}")
    output.append(f"💵 预算剩余: ¥{plan['remaining']}")
    output.append(f"{'='*50}\n")
    
    return '\n'.join(output)

def main():
    # 默认参数
    age_range = None
    budget = 5000
    category = None
    plan_name = "教具采购方案"
    
    # 解析参数
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == '--age' and i+1 < len(args):
            age_range = args[i+1]
        elif arg == '--budget' and i+1 < len(args):
            budget = int(args[i+1])
        elif arg == '--category' and i+1 < len(args):
            category = args[i+1]
        elif arg == '--name' and i+1 < len(args):
            plan_name = args[i+1]
    
    print(f"\n🎯 生成方案: 年龄 {age_range or '不限'}, 预算 ¥{budget}, 分类 {category or '不限'}")
    
    plan = generate_plan(age_range, budget, category, plan_name)
    print(format_plan(plan))

if __name__ == "__main__":
    main()
