#!/usr/bin/env node
const XLSX = require('xlsx');
const fs = require('fs');

/**
 * Excel Reader for Doc Filler
 * Improved version with better table parsing
 */

const filePath = process.argv[2];
const outputPath = process.argv[3];

if (!filePath) {
    console.error('Usage: node read_excel_advanced.js <file.xlsx> [output.json]');
    process.exit(1);
}

if (!fs.existsSync(filePath)) {
    console.error('File not found:', filePath);
    process.exit(1);
}

function parseExcel(workbook) {
    const result = {};
    
    for (const sheetName of workbook.SheetNames) {
        const sheet = workbook.Sheets[sheetName];
        const json = XLSX.utils.sheet_to_json(sheet, { 
            header: 1, 
            defval: '',
            raw: false,
            blankrows: false
        });
        
        // Parse as key-value pairs (first column = key, second column = value)
        const kvData = {};
        
        for (let i = 0; i < json.length; i++) {
            const row = json[i];
            
            // Skip empty rows
            if (!row || row.length === 0) continue;
            
            // Get key from first column
            const key = String(row[0] || '').trim();
            if (!key) continue;
            
            // Get value from second column
            let value = row[1];
            
            // Skip if value is empty
            if (value === undefined || value === '' || value === null) continue;
            
            // Convert to string
            value = String(value).trim();
            
            // Handle special cases (like dates stored as numbers)
            if (typeof row[1] === 'number' && row[1] > 30000 && row[1] < 60000) {
                // Likely Excel date serial number
                const date = new Date((row[1] - 25569) * 86400 * 1000);
                value = date.toISOString().split('T')[0];
            }
            
            // Store in kvData
            kvData[key] = value;
            
            // Also capture additional columns as extra fields
            for (let j = 2; j < row.length; j++) {
                if (row[j] && String(row[j]).trim()) {
                    kvData[`${key}_${j}`] = String(row[j]);
                }
            }
        }
        
        result[sheetName] = {
            kv: kvData,
            raw: json
        };
    }
    
    return result;
}

// Also support CSV
function parseCSV(content) {
    const lines = content.split('\n');
    const result = {};
    let currentSection = 'default';
    
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        
        // Check if section header
        if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
            currentSection = trimmed.slice(1, -1);
            result[currentSection] = {};
            continue;
        }
        
        // Parse key=value
        const eqIdx = trimmed.indexOf('=');
        if (eqIdx > 0) {
            const key = trimmed.slice(0, eqIdx).trim();
            const value = trimmed.slice(eqIdx + 1).trim();
            if (!result[currentSection]) {
                result[currentSection] = {};
            }
            result[currentSection][key] = value;
        }
    }
    
    return result;
}

// Main
try {
    let data;
    
    if (filePath.endsWith('.csv')) {
        data = { 'csv': parseCSV(fs.readFileSync(filePath, 'utf-8')) };
    } else {
        const workbook = XLSX.readFile(filePath);
        data = parseExcel(workbook);
    }
    
    const output = JSON.stringify(data, null, 2);
    
    if (outputPath) {
        fs.writeFileSync(outputPath, output);
        console.log('Data extracted to:', outputPath);
    } else {
        console.log(output);
    }
} catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
}
