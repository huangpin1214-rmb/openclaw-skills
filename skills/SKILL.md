---
name: vulnerability-monitor
description: 全球漏洞监控。监控CVE漏洞披露、KEV在野利用、供应商安全公告。按紧急程度分类并推送报告。当用户询问漏洞监控、CVE、零日漏洞、安全公告时触发。
metadata:
  openclaw:
    trigger:
      - "漏洞"
      - "CVE"
      - "零日"
      - "安全公告"
      - "vulnerability"
      - "KEV"
      - "在野利用"
---

# 全球漏洞监控技能

## 功能

- ✅ CVE漏洞披露监控
- ✅ KEV（在野利用）跟踪
- ✅ 供应商安全公告
- ✅ 按紧急程度分类（Urgent/High/Medium/Low）
- ✅ 定期推送（每周）

## 快速使用

直接说"查一下最近有什么高危漏洞"或"给我一个漏洞周报"

## 数据源

- CISA KEV (Known Exploited Vulnerabilities)
- NVD (National Vulnerability Database)
- 厂商安全公告（Microsoft, Cisco, Adobe, Google等）
- CERT/PSIRT公告

## 紧急程度定义

| 级别 | 定义 | 响应时间 |
|------|------|----------|
| Urgent | 在野利用、主动攻击 | 24小时内 |
| High | 严重漏洞、可利用 | 3天内 |
| Medium | 中危漏洞 | 1周内 |
| Low | 低危漏洞 | 常规跟踪 |

## 运行方式

### 快速查询
```bash
# 查询最近72小时高危漏洞
python3 ~/.openclaw/workspace/skills/vulnerability-monitor/scripts/check_cve.py --hours 72 --urgency high
```

### 完整报告
```bash
python3 ~/.openclaw/workspace/skills/vulnerability-monitor/scripts/check_cve.py --hours 168 --output report.md
```

## 输出示例

```
## 🔴 Urgent - 在野利用
- [CVE-2026-XXX] Apache Log4j 漏洞
  来源: CISA KEV | 发布: 2026-03-21
  影响: 远程代码执行，已在野利用

## 🟠 High - 严重漏洞
- [CVE-2026-XXX] Microsoft Windows 漏洞
  来源: MSRC | 发布: 2026-03-20
  影响: 权限提升

## 建议
1. 优先修补Urgent级别漏洞
2. 检查是否受影响
3. 关注厂商最新公告
```

## 定时任务

- 每周一9:30自动推送漏洞周报
- 任务名: 漏洞监控周报

## 参考

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NVD: https://nvd.nist.gov/
- 中国CNNVD: https://www.cnnvd.org.cn/
