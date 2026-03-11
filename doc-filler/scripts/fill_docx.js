#!/usr/bin/env node
/**
 * Word DOCX Filler - Advanced Version
 * Better XML manipulation for filling Word templates
 */

const fs = require('fs');
const path = require('path');

/**
 * Parse DOCX file and extract document XML
 */
function readDocx(docxPath) {
    const AdmZip = require('adm-zip');
    const zip = new AdmZip(docxPath);
    const entries = zip.getEntries();
    const files = {};
    
    for (const entry of entries) {
        files[entry.entryName] = entry.getData().toString('utf8');
    }
    
    return {
        files,
        xml: files['word/document.xml'],
        getContentTypes: () => files['[Content_Types].xml'],
        getStyles: () => files['word/styles.xml']
    };
}

/**
 * Parse XML and extract text elements with positions
 */
function parseDocumentXML(xml) {
    const result = {
        tables: [],
        texts: [],
        elements: []
    };
    
    // Find all tables
    const tableRegex = /<w:tbl[^>]*>([\s\S]*?)<\/w:tbl>/g;
    let match;
    while ((match = tableRegex.exec(xml)) !== null) {
        result.tables.push({
            xml: match[0],
            start: match.index,
            end: match.index + match[0].length
        });
    }
    
    // Find all text runs with context
    const runRegex = /<w:r[^>]*>[\s\S]*?<w:t(?:\s+[^>]*)?>([^<]*)<\/w:t>[\s\S]*?<\/w:r>/g;
    while ((match = runRegex.exec(xml)) !== null) {
        const text = match[1];
        result.texts.push({
            text: text,
            xml: match[0],
            start: match.index,
            end: match.index + match[0].length
        });
    }
    
    return result;
}

/**
 * Extract all text from document
 */
function extractAllText(xml) {
    const texts = [];
    const regex = /<w:t[^>]*>([^<]*)<\/w:t>/g;
    let match;
    while ((match = regex.exec(xml)) !== null) {
        texts.push(match[1]);
    }
    return texts;
}

/**
 * Find table rows and their content
 */
function extractTableRows(xml) {
    const rows = [];
    const rowRegex = /<w:tr[^>]*>([\s\S]*?)<\/w:tr>/g;
    let match;
    
    while ((match = rowRegex.exec(xml)) !== null) {
        const cells = [];
        const cellRegex = /<w:tc[^>]*>([\s\S]*?)<\/w:tc>/g;
        let cellMatch;
        
        while ((cellMatch = cellRegex.exec(match[0])) !== null) {
            const cellText = extractAllText(cellMatch[1]).join(' ').trim();
            cells.push({
                text: cellText,
                xml: cellMatch[0]
            });
        }
        
        rows.push(cells);
    }
    
    return rows;
}

/**
 * Find label and fill next cell
 */
function fillTableCell(xml, label, value) {
    // Strategy 1: Find exact label in a cell, fill next cell
    let filled = false;
    
    // Find row with this label
    const rows = extractTableRows(xml);
    
    for (const row of rows) {
        for (let i = 0; i < row.length - 1; i++) {
            if (row[i].text.includes(label) || label.includes(row[i].text)) {
                // Found label, check if next cell is empty
                if (!row[i+1].text || row[i+1].text.trim() === '') {
                    // Fill next cell with value
                    const nextCellXML = row[i+1].xml;
                    // Find the first w:t element and add text
                    const newCellXML = nextCellXML.replace(
                        /(<w:t[^>]*>)(<\/w:t>)/,
                        `$1${value}$2`
                    );
                    xml = xml.replace(row[i+1].xml, newCellXML);
                    filled = true;
                    break;
                }
            }
        }
        if (filled) break;
    }
    
    // Strategy 2: Direct text append (for simple cases)
    if (!filled) {
        // Find label and append value after it in the text
        const labelRegex = new RegExp(`(<w:t[^>]*>${escapeRegex(label)})(</w:t>)`, 'g');
        xml = xml.replace(labelRegex, `$1${value}$2`);
    }
    
    return xml;
}

/**
 * Escape special regex characters
 */
function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Main fill function
 */
function fillDocx(docxPath, data, outputPath) {
    const AdmZip = require('adm-zip');
    const zip = new AdmZip(docxPath);
    const entries = zip.getEntries();
    const files = {};
    
    // Read all files
    for (const entry of entries) {
        files[entry.entryName] = entry.getData().toString('utf8');
    }
    
    let xml = files['word/document.xml'];
    
    // Fill in data
    for (const [label, value] of Object.entries(data)) {
        if (value && String(value).trim()) {
            xml = fillTableCell(xml, label, String(value));
        }
    }
    
    // Write output
    files['word/document.xml'] = xml;
    
    const outputZip = new AdmZip();
    for (const [name, content] of Object.entries(files)) {
        outputZip.addFile(name, Buffer.from(content, 'utf8'));
    }
    
    outputZip.writeZip(outputPath);
    console.log('Created:', outputPath);
}

/**
 * Export functions
 */
module.exports = {
    readDocx,
    parseDocumentXML,
    extractAllText,
    extractTableRows,
    fillTableCell,
    fillDocx
};

// CLI
if (require.main === module) {
    const docxPath = process.argv[2];
    const dataFile = process.argv[3];
    const outputPath = process.argv[4];
    
    if (!docxPath || !dataFile) {
        console.log('Usage: node fill_docx.js <template.docx> <data.json> [output.docx]');
        console.log('  data.json should contain: { "label": "value", ... }');
        process.exit(1);
    }
    
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    const output = outputPath || docxPath.replace('.docx', '_filled.docx');
    
    fillDocx(docxPath, data, output);
}
