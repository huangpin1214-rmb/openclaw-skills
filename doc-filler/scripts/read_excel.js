#!/usr/bin/env node
const XLSX = require('xlsx');
const fs = require('fs');

const filePath = process.argv[2];

if (!filePath) {
    console.error('Usage: node read_excel.js <file.xlsx>');
    process.exit(1);
}

if (!fs.existsSync(filePath)) {
    console.error('File not found:', filePath);
    process.exit(1);
}

const workbook = XLSX.readFile(filePath);
const result = {};

// Process each sheet
for (const sheetName of workbook.SheetNames) {
    const sheet = workbook.Sheets[sheetName];
    const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });
    result[sheetName] = json;
}

console.log(JSON.stringify(result, null, 2));
