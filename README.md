# OpenClaw Skills

我的 OpenClaw 自定义技能集合。

## Skills 列表

### 1. bis-entity-check
BIS EAR 实体清单查询工具

**功能：**
- 查询公司是否在美国 BIS 实体清单上
- 显示具体实体名称、脚注编号、列入时间、列入原因
- 支持浪潮、新华三、华为、中芯国际等公司

**使用：**
```bash
python3 bis-entity-check/scripts/check_bis.py
python3 bis-entity-check/scripts/report.py 华为
```

---

### 2. web-search
基于 Tavily API 的网页搜索工具

**使用：**
```bash
curl -sL -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"YOUR_KEY","query":"关键词","max_results":5}'
```

---

### 3. ai-news-monitor
AI 新闻每日简报自动推送

**功能：**
- 每天早上 8:00 自动推送最新 AI 新闻
- 使用 Tavily 搜索，支持当日缓存

**使用：**
```bash
python3 ai-news-monitor/scripts/fetch_news.py
```

---

### 4. doc-filler
文档模板填写工具

**功能：**
- 从 Excel 读取数据
- 自动填入 Word 文档表格
- 支持批量处理

---

### 5. 8d-report
芯片 Fabless 公司客户问题 8D 报告生成工具

**功能：**
- 生成标准 8D 报告（D0-D8）
- 交互式问答填写
- 包含 5Why 分析、鱼骨图模板
- 适用于芯片 fabless 公司客户投诉处理

**使用：**
```bash
python3 8d-report/scripts/generate_8d.py
# 交互式填写问题信息，自动生成完整 8D 报告
```

---

## 配置

- Tavily API Key：需自行配置
- 搜索额度：免费版每月 1000 credits

---

## 许可证

MIT
