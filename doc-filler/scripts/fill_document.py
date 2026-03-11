#!/usr/bin/env python3
"""Document Filler - Fill template documents with provided information."""

import re
import json
import sys
import os
from pathlib import Path

def extract_placeholders(content):
    """Extract all placeholders from document."""
    # Match {{field}}, [field], _field_ but NOT greedy matching across fields
    patterns = [
        r'\{\{(\w+(?:_\w+)*)\}\}',  # {{field_name}} or {{field_name_sub}}
        r'\[(\w+(?:_\w+)*)\]',        # [field_name]
        r'_(\w+(?:_\w+)*)_'          # _field_name_
    ]
    
    placeholders = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        placeholders.update(matches)
    
    return placeholders

def load_user_data(data_path):
    """Load user data from JSON file."""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def fill_document(content, user_data):
    """Fill placeholders with user data."""
    filled_content = content
    
    # Track what was filled
    filled_fields = {}
    missing_fields = set()
    needs_confirmation = {}
    
    # Get all placeholders
    placeholders = extract_placeholders(content)
    
    # Sort placeholders by length (longest first) to avoid partial replacements
    sorted_fields = sorted(placeholders, key=len, reverse=True)
    
    for field in sorted_fields:
        field_key = field.strip().lower().replace(' ', '_')
        value = None
        
        # Check exact match only (no partial matching)
        if field in user_data:
            value = user_data[field]
        elif field_key in user_data:
            value = user_data[field_key]
        
        if value:
            # Replace only this specific placeholder format
            filled_content = re.sub(r'\{\{' + re.escape(field) + r'\}\}', str(value), filled_content)
            filled_content = re.sub(r'\[' + re.escape(field) + r'\]', str(value), filled_content)
            filled_content = re.sub(r'_' + re.escape(field) + r'_', str(value), filled_content)
            filled_fields[field] = value
        else:
            missing_fields.add(field)
    
    # Check what needs confirmation (fields with sensitive/important data)
    for field in missing_fields:
        if any(keyword in field.lower() for keyword in ['amount', 'price', 'date', 'signature', 'confirm', 'due']):
            needs_confirmation[field] = "Important field - needs human confirmation before use"
    
    return filled_content, filled_fields, missing_fields, needs_confirmation

def generate_report(filled_fields, missing_fields, needs_confirmation):
    """Generate a report of the filling operation."""
    report = []
    report.append("=" * 50)
    report.append("   Document Filling Report")
    report.append("=" * 50)
    
    # Filled fields
    report.append("\n✅ Filled Fields:")
    if filled_fields:
        for field, value in filled_fields.items():
            report.append(f"   • {field}: {value}")
    else:
        report.append("   (none)")
    
    # Missing fields
    report.append("\n⚠️ Missing Fields (not provided):")
    if missing_fields:
        for field in sorted(missing_fields):
            report.append(f"   • {field}")
    else:
        report.append("   (none)")
    
    # Needs confirmation
    report.append("\n❓ Needs Human Confirmation:")
    if needs_confirmation:
        for field, reason in needs_confirmation.items():
            report.append(f"   • {field}: {reason}")
    else:
        report.append("   (none)")
    
    report.append("=" * 50)
    
    return "\n".join(report)

def interactive_mode():
    """Run in interactive mode - prompt for template and data."""
    print("📄 Document Filler - Interactive Mode")
    print("=" * 50)
    
    # Get template file
    template_path = input("Enter template file path: ").strip()
    if not os.path.exists(template_path):
        print(f"❌ File not found: {template_path}")
        return
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract placeholders
    placeholders = extract_placeholders(template_content)
    print(f"\nFound {len(placeholders)} placeholder(s): {', '.join(sorted(placeholders))}")
    
    # Get user data
    print("\nEnter values for each field (press Enter to skip):")
    user_data = {}
    for field in sorted(placeholders):
        value = input(f"  {field}: ").strip()
        if value:
            user_data[field] = value
    
    # Fill document
    filled_content, filled_fields, missing_fields, needs_confirmation = fill_document(template_content, user_data)
    
    # Generate report
    report = generate_report(filled_fields, missing_fields, needs_confirmation)
    print("\n" + report)
    
    # Show filled document
    print("\n📝 Filled Document:")
    print("-" * 50)
    print(filled_content)
    print("-" * 50)
    
    # Ask to save
    save = input("\nSave filled document? (y/n): ").strip().lower()
    if save == 'y':
        output_path = input("Output file path: ").strip()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(filled_content)
        print(f"✅ Saved to: {output_path}")

def main():
    if len(sys.argv) == 1 or '--interactive' in sys.argv:
        interactive_mode()
        return
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 fill_document.py <template_file> <data.json>")
        print("  python3 fill_document.py --interactive")
        sys.exit(1)
    
    template_path = sys.argv[1]
    data_path = sys.argv[2]
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Load user data
    user_data = load_user_data(data_path)
    
    # Fill document
    filled_content, filled_fields, missing_fields, needs_confirmation = fill_document(template_content, user_data)
    
    # Generate and print report
    report = generate_report(filled_fields, missing_fields, needs_confirmation)
    print(report)
    
    # Print filled document
    print("\n📝 Filled Document:")
    print("-" * 50)
    print(filled_content)
    print("-" * 50)

if __name__ == "__main__":
    main()
