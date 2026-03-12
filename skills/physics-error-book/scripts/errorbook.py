#!/usr/bin/env python3
"""
初中物理错题本管理工具
"""

import json
import os
import sys
from datetime import datetime, timedelta

DB_PATH = os.path.expanduser('~/.openclaw/workspace/knowledge/physics-errors.json')

# 知识点映射
CHAPTERS = {
    '八上': ['机械运动', '声现象', '物态变化', '光现象', '透镜'],
    '八下': ['力', '运动和力', '压强', '浮力', '功和机械能'],
    '九全': ['电压', '电流', '电阻', '欧姆定律', '电功率', '焦耳定律', '磁现象', '电磁感应', '能源']
}

ERROR_TYPES = {
    '1': '知识漏洞',
    '2': '思路错误', 
    '3': '粗心大意',
    '4': '审题不清',
    '5': '记忆模糊'
}

def load_errors():
    """加载错题数据"""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'errors': [], 'stats': {}}

def save_errors(data):
    """保存错题数据"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_error(title, correct_answer, wrong_answer, chapter, error_type='1', note=''):
    """添加错题"""
    data = load_errors()
    
    error = {
        'id': len(data['errors']) + 1,
        'title': title,
        'correct_answer': correct_answer,
        'wrong_answer': wrong_answer,
        'chapter': chapter,
        'error_type': error_type,
        'note': note,
        'created_at': datetime.now().isoformat(),
        'review_times': 0,
        'next_review': datetime.now().isoformat()
    }
    
    data['errors'].append(error)
    save_errors(data)
    
    print(f"\n✅ 错题已添加 (ID: {error['id']})")
    print(f"   章节: {chapter}")
    print(f"   错误类型: {ERROR_TYPES.get(error_type, '未知')}")

def list_errors(chapter=None, limit=10):
    """列出错题"""
    data = load_errors()
    errors = data['errors']
    
    if chapter:
        errors = [e for e in errors if chapter in e['chapter']]
    
    errors = errors[-limit:][::-1]
    
    print(f"\n📝 错题列表 (共 {len(data['errors'])} 题)")
    print("=" * 60)
    
    for e in errors:
        print(f"\n【{e['id']}】{e['title'][:50]}...")
        print(f"   章节: {e['chapter']} | 类型: {ERROR_TYPES.get(e['error_type'], '未知')}")
        print(f"   ❌ {e['wrong_answer'][:30]}...")
        print(f"   ✅ {e['correct_answer'][:30]}...")

def analyze_error(error_id):
    """分析错题"""
    data = load_errors()
    error = next((e for e in data['errors'] if e['id'] == error_id), None)
    
    if not error:
        print(f"❌ 未找到 ID 为 {error_id} 的错题")
        return
    
    print(f"\n📊 错题分析")
    print("=" * 60)
    print(f"\n【题目】{error['title']}")
    print(f"\n❌ 你的答案: {error['wrong_answer']}")
    print(f"✅ 正确答案: {error['correct_answer']}")
    print(f"\n📚 所属章节: {error['chapter']}")
    print(f"🔍 错误类型: {ERROR_TYPES.get(error['error_type'], '未知')}")
    
    if error.get('note'):
        print(f"\n📝 笔记: {error['note']}")
    
    # 根据错误类型给出建议
    suggestions = {
        '1': '建议回归教材，夯实基础，理解概念后再做题',
        '2': '建议归纳解题模型，掌握同类题型的解题思路',
        '3': '建议养成检查习惯，题目多读几遍再下笔',
        '4': '建议圈画关键词，理清已知条件和求解目标',
        '5': '建议加强公式定理的背诵和默写'
    }
    print(f"\n💡 改进建议: {suggestions.get(error['error_type'], '')}")

def stats():
    """统计报告"""
    data = load_errors()
    errors = data['errors']
    
    if not errors:
        print("\n暂无错题数据")
        return
    
    # 按章节统计
    chapter_count = {}
    error_type_count = {}
    
    for e in errors:
        chapter_count[e['chapter']] = chapter_count.get(e['chapter'], 0) + 1
        error_type_count[e['error_type']] = error_type_count.get(e['error_type'], 0) + 1
    
    print(f"\n📊 物理错题统计报告")
    print("=" * 60)
    print(f"\n总错题数: {len(errors)} 题")
    
    print(f"\n📚 按章节统计:")
    for chapter, count in sorted(chapter_count.items(), key=lambda x: -x[1]):
        pct = count / len(errors) * 100
        print(f"   {chapter}: {count} 题 ({pct:.0f}%)")
    
    print(f"\n🔍 按错误类型统计:")
    for etype, count in sorted(error_type_count.items(), key=lambda x: -x[1]):
        pct = count / len(errors) * 100
        print(f"   {ERROR_TYPES.get(etype, '未知')}: {count} 题 ({pct:.0f}%)")

def review_plan():
    """复习计划"""
    data = load_errors()
    errors = data['errors']
    
    if not errors:
        print("\n暂无错题")
        return
    
    # 根据记忆曲线推荐复习
    today = datetime.now()
    review_list = []
    
    for e in errors:
        next_review = datetime.fromisoformat(e['next_review'])
        if next_review <= today:
            review_list.append(e)
    
    print(f"\n📅 今日复习计划")
    print("=" * 60)
    
    if not review_list:
        print("🎉 今天没有需要复习的错题！")
        return
    
    print(f"今日应复习: {len(review_list)} 题\n")
    
    for e in review_list[:10]:
        print(f"【{e['id']}】{e['title'][:40]}...")
        print(f"    章节: {e['chapter']} | 类型: {ERROR_TYPES.get(e['error_type'], '未知')}")

def main():
    if len(sys.argv) < 2:
        print("""
📚 初中物理错题本

用法:
  python3 errorbook.py add <题目> <正确答案> <错误答案> <章节> [错误类型] [笔记]
  python3 errorbook.py list [章节] [数量]
  python3 errorbook.py analyze <ID>
  python3 errorbook.py stats
  python3 errorbook.py review

错误类型:
  1 - 知识漏洞
  2 - 思路错误
  3 - 粗心大意
  4 - 审题不清
  5 - 记忆模糊

示例:
  python3 errorbook.py add "汽车刹车问题..." "40m" "80m" "八下-运动和力" 3 "计算错误"
  python3 errorbook.py list
  python3 errorbook.py analyze 1
  python3 errorbook.py stats
  python3 errorbook.py review
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add' and len(sys.argv) >= 6:
        add_error(
            sys.argv[2], sys.argv[3], sys.argv[4],
            sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else '1',
            sys.argv[7] if len(sys.argv) > 7 else ''
        )
    elif cmd == 'list':
        chapter = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        list_errors(chapter, limit)
    elif cmd == 'analyze' and len(sys.argv) >= 3:
        analyze_error(int(sys.argv[2]))
    elif cmd == 'stats':
        stats()
    elif cmd == 'review':
        review_plan()
    else:
        print(f"未知命令: {cmd}")

if __name__ == "__main__":
    main()
