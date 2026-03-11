---
name: bis-entity-check
description: Check if an entity is on the BIS EAR Entity List. Use when user asks to verify if a company or person is on the US Bureau of Industry and Security export restriction list. Triggers on BIS entity check, EAR list, export control, entity list search, 美国实体清单, BIS清单, 出口管制.
---

# BIS EAR Entity List Checker

Check if entities are on the Bureau of Industry and Security (BIS) Export Administration Regulations (EAR) Entity List.

## What is the BIS Entity List?

The BIS Entity List contains foreign entities that are subject to specific license requirements for the export, reexport, or transfer (in-country) of specified items. These restrictions are imposed for reasons of national security, missile technology, nuclear non-proliferation, chemical and biological weapons, regional stability, and foreign policy.

## Quick Start

```bash
# Check a single entity
python3 scripts/check_entity.py "Huawei"

# Check multiple entities
python3 scripts/check_entity.py "Huawei" "ZTE" "SMIC"

# Update the entity list first
python3 scripts/check_entity.py --update
```

## Usage

### 1. Update Entity List

Before checking, update the latest entity list from BIS:

```bash
python3 scripts/check_entity.py --update
```

This will download the latest Entity List from:
- Primary: https://www.bis.doc.gov/index.php/policy-and-guidance/lists-of-parties-of-concern/entity-list
- Alternative: https://www.commerce.gov/bureau-industry-and-security/bis-parties-concern

### 2. Search for Entities

```bash
# Single entity
python3 scripts/check_entity.py "company name"

# Multiple entities
python3 scripts/check_entity.py "Huawei" "ZTE" "SMIC"

# Case insensitive search
python3 scripts/check_entity.py --case-insensitive "huawei"
```

### 3. Interactive Mode

```bash
python3 scripts/check_entity.py --interactive
```

## Output Format

The checker will output:

```
=== BIS EAR Entity List Check ===

📅 Entity List Version: 2026-03-10
📊 Total Entities: X,XXX

🔍 Searching for: "huawei"

=== Results ===

❌ FOUND: Huawei Technologies Co., Ltd.
   - Listing Date: 2019-05-16
   - License Requirement: Presumption of denial
   - Federal Register Citation: 84 FR 29355
   - Address: Shenzhen, China
   - Keywords: telecommunications, 5G, smartphones

❌ FOUND: Huawei Cloud Computing Technologies Co., Ltd.
   - Listing Date: 2019-05-16
   - License Requirement: Presumption of denial
   - Federal Register Citation: 84 FR 29355
   - Address: Shenzhen, China
   - Keywords: cloud services

⚠️ PARTIAL MATCH: "Huawei" found in 5 entities
   1. Huawei Technologies Co., Ltd.
   2. Huawei Cloud Computing Technologies Co., Ltd.
   3. Futurewei Technologies, Inc. (d.b.a. Huawei Technologies)
   ...

✅ NOT FOUND: "ZTE" - No exact match found
   (But check related: ZTE Corporation may be listed under different name)
```

## Known Chinese Entities (Common Searches)

Some commonly searched Chinese entities and their status:

| Entity | Status | Notes |
|--------|--------|-------|
| Huawei | ❌ Listed | Since 2019, expanded multiple times |
| ZTE | ❌ Listed | Since 2016 |
| SMIC | ❌ Listed | Since 2020 |
| DJI | ❌ Listed | Since 2021 |
| SenseTime | ❌ Listed | Since 2022 |
| Megvii | ❌ Listed | Since 2022 |
| Hikvision | ❌ Listed | Since 2019 |
| Dahua | ❌ Listed | Since 2019 |
| BYD | ⚠️ Check | Some subsidiaries listed |
| Tencent | ⚠️ Check | Various subsidiaries |

## Data Source

The Entity List is maintained by the Bureau of Industry and Security (BIS), a bureau of the US Department of Commerce.

- **Website**: https://www.bis.doc.gov
- **Entity List Page**: https://www.bis.doc.gov/index.php/policy-and-guidance/lists-of-parties-of-concern/entity-list
- **Federal Register**: Changes are published in the Federal Register

## Important Notes

1. **This is for reference only** - Always verify with official BIS sources for official determinations
2. **List updates frequently** - Check for recent additions
3. **Subsidiaries matter** - Parent companies may have different status than subsidiaries
4. **License requirements vary** - Some may have specific license exceptions

## Legal Disclaimer

This tool provides information for reference purposes only. It does not constitute legal advice. For official determinations regarding export control compliance, consult with legal counsel and the official BIS Entity List.
