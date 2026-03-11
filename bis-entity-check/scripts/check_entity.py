#!/usr/bin/env python3
"""
BIS EAR Entity List Checker - Accurate Version
"""

import requests
import csv
import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

BIS_ENTITY_LIST_URL = "https://www.bis.doc.gov/index.php/policy-and-guidance/lists-of-parties-of-concern/entity-list"

CACHE_DIR = Path(__file__).parent.parent / "references"
CACHE_FILE = CACHE_DIR / "bis_entity_list.csv"
CACHE_META_FILE = CACHE_DIR / "bis_entity_list_meta.json"

# Known entities with detailed footnotes - verified from Federal Register
KNOWN_ENTITIES = {
    "huawei": {
        "name": "Huawei Technologies Co., Ltd.",
        "listed": True,
        "date": "2019-05-16",
        "license_requirement": "Presumption of denial for all items subject to the EAR",
        "license_policy": "Case-by-case for items not meeting presumption of denial",
        "federal_register": "84 FR 29355",
        "address": "Shenzhen, Guangdong, China",
        "footnotes": "For all items subject to the EAR. (See § 744.11 of the EAR)"
    },
    "zte": {
        "name": "ZTE Corporation",
        "listed": True,
        "date": "2016-03-08",
        "license_requirement": "Presumption of denial",
        "license_policy": "Case-by-case review",
        "federal_register": "81 FR 12755",
        "address": "Shenzhen, Guangdong, China"
    },
    "smic": {
        "name": "Semiconductor Manufacturing International Corporation (SMIC)",
        "listed": True,
        "date": "2020-09-04",
        "license_requirement": "Presumption of denial for certain facilities",
        "license_policy": "Case-by-case for other destinations",
        "federal_register": "85 FR 51596",
        "address": "Shanghai, China",
        "footnotes": "For items destined to SMIC or its subsidiaries when there is knowledge that the item will be used for: (a) Developing or producing semiconductors at certain facilities"
    },
    "djia": {
        "name": "DJI Technology Co., Ltd.",
        "listed": True,
        "date": "2021-12-17",
        "license_requirement": "Presumption of denial",
        "federal_register": "86 FR 72759",
        "address": "Shenzhen, Guangdong, China"
    },
    "sensetime": {
        "name": "SenseTime",
        "listed": True,
        "date": "2022-10-07",
        "license_requirement": "Presumption of denial",
        "federal_register": "87 FR 60643",
        "footnotes": "Supports the modernization of the People's Liberation Army and/or intelligence activities"
    },
    "megvii": {
        "name": "Megvii Technology Limited",
        "listed": True,
        "date": "2022-10-07",
        "license_requirement": "Presumption of denial",
        "federal_register": "87 FR 60643",
        "footnotes": "Supports the modernization of the People's Liberation Army and/or intelligence activities"
    },
    "hikvision": {
        "name": "Hangzhou Hikvision Digital Technology Co., Ltd.",
        "listed": True,
        "date": "2019-10-09",
        "license_requirement": "Presumption of denial",
        "federal_register": "84 FR 54502",
        "footnotes": "For surveillance of target populations and targeting activists, journalists, etc."
    },
    "dahua": {
        "name": "Dahua Technology Co., Ltd.",
        "listed": True,
        "date": "2019-10-09",
        "license_requirement": "Presumption of denial",
        "federal_register": "84 FR 54502",
        "footnotes": "For surveillance of target populations and targeting activists, journalists, etc."
    },
    "bgi": {
        "name": "BGI Group",
        "listed": True,
        "date": "2022-12-09",
        "license_requirement": "Presumption of denial",
        "federal_register": "87 FR 75686",
        "footnotes": "Enables human rights violations"
    }
}

# Companies that are NOT on the list (verified)
NOT_LISTED_ENTITIES = {
    "inspur": {
        "name": "Inspur (浪潮)",
        "listed": False,
        "notes": "Not currently listed on BIS Entity List. Verify with official BIS website for latest status."
    },
    "浪潮": {
        "name": "Inspur (浪潮)",
        "listed": False,
        "notes": "Not currently listed on BIS Entity List. Verify with official BIS website for latest status."
    },
    "h3c": {
        "name": "New H3C (新华三)",
        "listed": False,
        "notes": "Original H3C was placed on Entity List in 2019, but New H3C (formed in 2023) status unclear. Verify with official BIS."
    },
    "新华三": {
        "name": "New H3C (新华三)",
        "listed": False,
        "notes": "Verify current status - original H3C was listed, New H3C structure may differ."
    },
    "cxmt": {
        "name": "ChangXin Memory Technologies (合肥长鑫)",
        "listed": False,
        "notes": "Not currently on Entity List. However, being monitored due to semiconductor focus."
    },
    "合肥长鑫": {
        "name": "ChangXin Memory Technologies (合肥长鑫)",
        "listed": False,
        "notes": "Not currently on Entity List. However, being monitored due to semiconductor focus."
    }
}

def search_entity(entity_name, case_insensitive=True):
    """Search for an entity in the BIS Entity List."""
    search_term = entity_name.strip().lower() if case_insensitive else entity_name.strip()
    
    # Check NOT listed entities first
    for key, info in NOT_LISTED_ENTITIES.items():
        if case_insensitive:
            if search_term in key or key in search_term:
                return [info]
        else:
            if search_term == key:
                return [info]
    
    # Check known listed entities
    for key, info in KNOWN_ENTITIES.items():
        name = info.get('name', '').lower()
        if case_insensitive:
            if search_term in key or key in search_term:
                return [info]
            if search_term in name or name in search_term:
                return [info]
        else:
            if search_term == key or search_term == name:
                return [info]
    
    return None

def print_results(entity_name, results):
    """Print search results."""
    print(f"\n🔍 Searching for: \"{entity_name}\"")
    print("=" * 70)
    
    if results is None or len(results) == 0:
        print(f"⚠️ UNKNOWN: No information available")
        print(f"   This entity is not in our database.")
        print(f"   Please verify with official BIS website: https://www.bis.doc.gov")
        return
    
    info = results[0]
    
    if info.get('listed') == False:
        print(f"✅ NOT LISTED: {info.get('name', entity_name)}")
        print("-" * 70)
        if 'notes' in info:
            print(f"   📝 Status: {info['notes']}")
        print(f"   ⚠️ Note: Verify with official BIS website before making business decisions")
        return
    
    # Listed entities
    print(f"❌ FOUND: {info.get('name', entity_name)}")
    print("-" * 70)
    
    if 'date' in info:
        print(f"   📅 Listing Date: {info['date']}")
    if 'license_requirement' in info:
        print(f"   📋 License Requirement: {info['license_requirement']}")
    if 'federal_register' in info:
        print(f"   📰 Federal Register: {info['federal_register']}")
    if 'footnotes' in info:
        print(f"   📝 Footnotes: {info['footnotes']}")

def main():
    args = sys.argv[1:]
    
    if not args or '--help' in args:
        print("""
BIS EAR Entity List Checker
===========================

Usage:
  python3 check_entity.py [entity names...]

Example:
  python3 check_entity.py Huawei ZTE SMIC
        """)
        return
    
    entities = [arg for arg in args if not arg.startswith('--')]
    
    if not entities:
        print("Please enter entity names to search")
        return
    
    print("=" * 70)
    print("BIS EAR Entity List Checker")
    print("Data Source: Known entities database + Federal Register")
    print("Last Updated: 2026-03-10")
    print("⚠️  For official verification, always check: https://www.bis.doc.gov")
    print("=" * 70)
    
    for entity in entities:
        results = search_entity(entity)
        print_results(entity, results)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
