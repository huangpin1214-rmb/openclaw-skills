---
name: doc-filler
description: Fill template documents with provided information. Use when user wants to fill a blank document or form template with their data. Supports DOCX, Excel, JSON, CSV. Automatically detects missing fields and highlights items needing human confirmation. Triggers on fill document, fill template, fill form, complete document, 填写Word, 填写表格.
---

# Document Filler

Fill blank documents/templates with data from Excel, JSON, or CSV. Supports DOCX, XLSX, JSON, CSV formats.

## Quick Start

```bash
# Read Excel data
node scripts/read_excel_advanced.js 公司资料.xlsx

# Fill Word template with JSON data
node scripts/fill_docx.js template.docx data.json output.docx

# Interactive mode (text templates)
python3 scripts/fill_document.py --interactive
```

## Features

### 1. Excel Reader (read_excel_advanced.js)

- Reads .xlsx and .csv files
- Automatically detects table structure
- Extracts key-value pairs
- Handles merged cells

```bash
# Extract to JSON
node scripts/read_excel_advanced.js 公司资料.xlsx data.json

# View in terminal
node scripts/read_excel_advanced.js 公司资料.xlsx
```

### 2. Word Filler (fill_docx.js)

- Fills DOCX table templates
- Supports fuzzy label matching
- Preserves original formatting
- Works with complex tables

```bash
# Basic usage
node scripts/fill_docx.js template.docx data.json output.docx

# data.json format:
# {
#   "公司名称": "成都星拓微电子科技股份有限公司",
#   "法人代表": "闫明明",
#   ...
# }
```

### 3. Text Template Filler (fill_document.py)

- For plain text templates
- Supports {{placeholder}} syntax
- Reports missing fields
- Interactive mode

```bash
# With JSON data
python3 scripts/fill_document.py template.txt data.json

# Interactive
python3 scripts/fill_document.py --interactive
```

## Workflow

### Complete Workflow Example

```bash
# 1. Read Excel data to understand structure
node scripts/read_excel_advanced.js 公司资料.xlsx

# 2. Create data.json with fields you want to fill
# {
#   "公司名称【中文】Company Name【CN】": "成都星拓微电子科技股份有限公司",
#   "法人代表": "闫明明",
#   ...
# }

# 3. Fill Word template
node scripts/fill_docx.js 制造商调查表.docx data.json 填写完成.docx
```

## Tips

### For Best Results

1. **Use clear labels**: Match labels in your template exactly
2. **Fuzzy matching**: The filler tries to match partial labels
3. **Check empty cells**: Make sure target cells are empty before filling
4. **Backup original**: Always keep a copy of the original template

### Field Mapping

The filler tries to match:
- Exact match: `公司名称` = `公司名称`
- Partial match: `公司名称【中文】` contains `公司名称`
- Case insensitive: `COMPANY NAME` = `company name`

### Common Issues

| Issue | Solution |
|-------|----------|
| Value not filled | Check label matches exactly |
| Format lost | Use fill_docx.js instead of string replacement |
| Encoding issues | Ensure UTF-8 encoding |
| Large files | Increase timeout |

## File Formats

| Format | Tool | Description |
|--------|------|-------------|
| .docx | fill_docx.js | Word documents with tables |
| .xlsx | read_excel_advanced.js | Excel spreadsheets |
| .csv | read_excel_advanced.js | CSV files |
| .txt | fill_document.py | Plain text templates |
| .json | All | Data interchange |

## Dependencies

- Node.js: xlsx, adm-zip
- Python: (built-in for text templates)

Install Node dependencies:
```bash
cd scripts
npm install xlsx adm-zip
```
