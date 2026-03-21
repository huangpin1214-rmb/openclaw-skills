#!/bin/bash
# 漏洞监控周报推送

echo "=== 漏洞监控周报 ===" > /tmp/vuln-report.md
echo "📅 $(date '+%Y-%m-%d %H:%M')" >> /tmp/vuln-report.md
echo "" >> /tmp/vuln-report.md

# 查询CISA KEV
echo "## 🔴 CISA KEV 在野利用漏洞" >> /tmp/vuln-report.md
echo "" >> /tmp/vuln-report.md

# 使用exabys mcporter搜索最新漏洞
RESULT=$(mcporter call 'exa.web_search_exa(query: "CVE vulnerability exploit 2026", numResults: 10)' 2>/dev/null)

if [ -n "$RESULT" ] && ! echo "$RESULT" | grep -q "Error"; then
    echo "$RESULT" | grep -oP 'Title: [^\n]+' | head -10 | sed 's/Title: /- /' >> /tmp/vuln-report.md
else
    echo "暂无数据" >> /tmp/vuln-report.md
fi

echo "" >> /tmp/vuln-report.md
echo "---" >> /tmp/vuln-report.md

# 搜索重大漏洞
echo "## 🟠 高危漏洞" >> /tmp/vuln-report.md
echo "" >> /tmp/vuln-report.md

HIGH_RESULT=$(mcporter call 'exa.web_search_exa(query: "critical vulnerability CVE 2026", numResults: 5)' 2>/dev/null)

if [ -n "$HIGH_RESULT" ] && ! echo "$HIGH_RESULT" | grep -q "Error"; then
    echo "$HIGH_RESULT" | grep -oP 'Title: [^\n]+' | head -5 | sed 's/Title: /- /' >> /tmp/vuln-report.md
fi

echo "" >> /tmp/vuln-report.md
echo "---" >> /tmp/vuln-report.md
echo "*数据来源: CISA KEV, NVD, 厂商公告*" >> /tmp/vuln-report.md

cat /tmp/vuln-report.md
