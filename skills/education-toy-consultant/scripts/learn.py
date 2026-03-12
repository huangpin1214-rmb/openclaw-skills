#!/usr/bin/env python3
"""
幼儿教育教具知识学习工具
用于增量添加新产品到知识库
"""

import json
import sys
import os

DB_PATH = os.path.expanduser('~/.openclaw/workspace/knowledge/tts-products.json')

def load_products():
    """加载现有产品"""
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('products', [])
    except:
        return []

def save_products(products):
    """保存产品到数据库"""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump({'products': products}, f, ensure_ascii=False, indent=2)

def add_product(sku, name, category, material, spec, age, price, desc):
    """添加单个产品"""
    products = load_products()
    
    # 检查是否已存在
    for p in products:
        if p['sku'] == sku:
            print(f"⚠️ 产品 {sku} 已存在，将更新")
            p.update({
                'name': name, 'category': category, 'material': material,
                'spec': spec, 'age': age, 'price': price, 'desc': desc
            })
            save_products(products)
            print(f"✅ 产品 {sku} 已更新")
            return
    
    # 添加新产品
    new_product = {
        'sku': sku, 'name': name, 'category': category,
        'material': material, 'spec': spec, 'age': age,
        'price': price, 'desc': desc
    }
    products.append(new_product)
    save_products(products)
    print(f"✅ 新产品 {sku} 已添加")

def import_from_excel(excel_path):
    """从 Excel 导入产品（需先提取到 JSON）"""
    # 这个功能需要先把 Excel 解析好
    print("请先使用 Excel 解析工具提取产品，再调用 add 命令添加")
    print(f"当前数据库: {DB_PATH}")

def list_products(category=None):
    """列出产品"""
    products = load_products()
    if category:
        products = [p for p in products if category in p.get('category', '')]
    
    print(f"\n📦 共 {len(products)} 款产品")
    for p in products:
        print(f"  {p['sku']} | {p['name'][:30]} | ¥{p.get('price', 'N/A')}")
    print()

def search_products(keyword):
    """搜索产品"""
    products = load_products()
    results = [p for p in products if keyword.lower() in p['name'].lower() or keyword in p['sku']]
    
    print(f"\n🔍 搜索 '{keyword}': 找到 {len(results)} 款")
    for p in results:
        print(f"  {p['sku']} | {p['name'][:30]} | {p.get('category', '')} | ¥{p.get('price', 'N/A')}")
    print()

def stats():
    """统计信息"""
    products = load_products()
    
    # 按分类统计
    categories = {}
    price_ranges = {'0-500': 0, '500-1500': 0, '1500-3000': 0, '3000+': 0}
    
    for p in products:
        cat = p.get('category', '未分类')
        categories[cat] = categories.get(cat, 0) + 1
        
        price = p.get('price', 0)
        if price <= 500:
            price_ranges['0-500'] += 1
        elif price <= 1500:
            price_ranges['500-1500'] += 1
        elif price <= 3000:
            price_ranges['1500-3000'] += 1
        else:
            price_ranges['3000+'] += 1
    
    print(f"\n📊 产品统计")
    print(f"  总计: {len(products)} 款")
    print(f"\n  按分类:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")
    print(f"\n  按价格:")
    for range_name, count in price_ranges.items():
        print(f"    ¥{range_name}: {count}")
    print()

def main():
    if len(sys.argv) < 2:
        print("""
📚 幼儿教育教具知识学习工具

用法:
  python3 learn.py add <sku> <name> <category> <material> <spec> <age> <price> <desc>
  python3 learn.py list [--category 分类]
  python3 learn.py search <关键词>
  python3 learn.py stats
  python3 learn.py import <excel路径>

示例:
  python3 learn.py add TCB001 "测试产品" "数学系列" "泡沫" "10cm" "3-6岁" 500 "产品描述"
  python3 learn.py list --category 数学系列
  python3 learn.py search "骰子"
  python3 learn.py stats
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add' and len(sys.argv) >= 10:
        add_product(
            sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
            sys.argv[6], sys.argv[7], int(sys.argv[8]), sys.argv[9]
        )
    elif cmd == 'list':
        cat = None
        for i, arg in enumerate(sys.argv):
            if arg == '--category' and i+1 < len(sys.argv):
                cat = sys.argv[i+1]
        list_products(cat)
    elif cmd == 'search' and len(sys.argv) >= 3:
        search_products(sys.argv[2])
    elif cmd == 'stats':
        stats()
    elif cmd == 'import' and len(sys.argv) >= 3:
        import_from_excel(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")

if __name__ == "__main__":
    main()
