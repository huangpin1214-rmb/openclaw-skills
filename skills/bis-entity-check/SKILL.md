---
name: bis-entity-check
description: 查询美国 BIS EAR 实体清单。详细版：包含具体实体名称、脚注编号、列入时间、列入原因。
---

# BIS Entity Check

查询公司是否在美国 BIS（ Bureau of Industry and Security）实体清单上。

## 📚 BIS官网（定期学习）
- **官网**: https://www.bis.gov/
- **Federal Register**: https://www.bis.gov/regulations/federal-register-notices
- **Entity List**: https://www.bis.gov/regulations/ear/part-764/section-764.1/introduction

**定期检查**: 每周一BIS EAR周报任务会自动检查更新

## 功能

- ✅ 显示所有具体实体名称（区分母公司/子公司）
- ✅ 显示脚注编号（如 Footnote 4）
- ✅ 显示列入时间
- ✅ 显示列入原因
- ✅ 当日缓存，避免重复调用

## 使用方式

### 运行脚本

```bash
# 查询默认公司（浪潮、新华三、合肥长鑫等）
python3 ~/.openclaw/workspace/skills/bis-entity-check/scripts/check_bis.py

# 查询特定公司
python3 ~/.openclaw/workspace/skills/bis-entity-check/scripts/check_bis.py 浪潮

# 强制刷新缓存
python3 ~/.openclaw/workspace/skills/bis-entity-check/scripts/check_bis.py --refresh
```

### 输出示例

```
🔍 BIS 实体清单查询: 浪潮 (Inspur)

⚠️ 状态: **已在实体清单上**

📋 具体实体:
   1. Inspur (Beijing) Electronic Information Industry Co., Ltd.
   2. Inspur Electronic Information Industry Co., Ltd.
   3. Inspur Electronic Information (Hong Kong) Co., Ltd.
   4. Inspur (HK) Electronics Co., Ltd.
   5. Inspur Software Co., Ltd.
   6. Inspur Taiwan (浪潮台湾子公司)

📋 清单信息:
   • 清单类型: EL (Entity List)
   • 脚注: 4
   • 列入时间: 2025年3月25/26日
   • 列入原因: 支持中国军事现代化/超级计算机开发
```

## 当前支持查询的公司

| 公司 | 状态 | 实体数量 | 列入时间 |
|------|------|----------|----------|
| 浪潮 (Inspur) | 已列入 | 6个实体 | 2025.3 |
| 新华三 (H3C) | 部分列入 | 1个子公司 | 2024.12 |
| 合肥长鑫 (CXMT) | 未列入 | - | - |
| 中芯国际 (SMIC) | 已列入 | 1个 | 2020.12 |
| 长江存储 (YMTC) | 已列入 | 1个 | 2022.12 |
| 华为 | 已列入 | 多个 | 2019.5 |

## 状态说明

| 状态 | 含义 |
|------|------|
| ⚠️ 已列入 | 公司主体已在 BIS 实体清单上 |
| 🔶 部分列入 | 母公司未列入，但子公司已列入 |
| ✅ 未列入 | 不在实体清单上 |

## 脚注说明

| 脚注 | 含义 |
|------|------|
| Footnote 1 | 出口管理条例第 744.22 条规定的军事最终用户 |
| Footnote 3 | 与被列入实体的关系导致 presumption of denial（推定拒绝） |
| Footnote 4 | 涉及国家安全的实体，需要更严格审查 |

## 许可证审查政策

| 政策 | 含义 | 典型时期 |
|------|------|----------|
| 推定拒绝 (Presumption of Denial) | 原则上拒绝 | 2022-2024 |
| 逐案审查 (Case-by-Case) | 根据具体情况 | 2026起松动 |
| 批准 (Approval) | 原则上批准 | 较少使用 |

**注意**: 2026年起H200/MI325X等芯片从"推定拒绝"转为"逐案审查"

## ERC委员会

- **全称**: End-User Review Committee
- **成员**: 商务部(主席)、国防部、国务院、能源部、财政部
- **决策**: 列入需多数票，移除需全票

## 政策演变 (2018-2026)

```
2018: ECRA生效
2019: 华为被列入
2022.10: 史上最严 - "推定拒绝"
2024.12: 最大规模 - 140个新增
2025.01: AI扩散框架
2026.02: 局部松动 - "逐案审查"
```

## 知识库

详细法规知识库请参考: `docs/BIS_Knowledge_Base.md`
中国时间线: `docs/BIS_China_Timeline.md`

## 注意事项

- 信息基于 BIS 官方 Federal Register 公开文件
- 建议访问 BIS 官网确认最新状态：https://www.bis.gov/
- 支持查询更多公司，可后续扩展数据库
