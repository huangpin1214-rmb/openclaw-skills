---
name: ai-news-monitor
description: Monitor and fetch the latest AI news daily from multiple sources including expert opinions. Use when the user wants AI news artificial intelligence updates. Triggers on AI news, AI updates, AI research, LLM news, OpenAI, Anthropic, Google DeepMind, machine learning news.
---

# AI News Monitor

Daily AI news monitoring skill with expert opinions. Fetches latest AI news from multiple reliable sources.

## Quick Start

```bash
python3 scripts/fetch_ai_news.py
```

## News Sources (Working)

### 1. Hacker News
- **Front Page**: `https://hnrss.org/frontpage`
- **AI Search**: `https://hnrss.org/newest?q=openai`
- Tech and startup news, covers AI extensively

### 2. AP News
- **AI Hub**: `https://apnews.com/hub/artificial-intelligence`
- Major news agency AI coverage

### 3. AI Expert Opinions
Search for recent opinions from industry leaders:
- Sam Altman (OpenAI)
- Dario Amodei (Anthropic)
- Demis Hassabis (Google DeepMind)
- Other AI researchers and thought leaders

## Output Sections

1. **Hacker News Front Page** - Top tech stories
2. **Hacker News AI** - AI-specific stories
3. **AP News AI** - Major news agency coverage
4. **Expert Opinions** - Perspectives from AI leaders

## Adding More Expert Sources

For more expert opinions, consider:
- **Substack AI newsletters** - Many AI researchers write on Substack
- **Twitter/X lists** - AI expert lists
- **Personal blogs** - Researchers often ( bloge.g., Andrej Karpathy)
- **YouTube** - AI conference talks

### 4. 卡兹克（数字生命卡兹克）
- **公众号**：数字生命卡兹克（Rockhazix）
- **简介**：AI领域顶流博主，连续12个月AI公众号TOP1，曾参与《流浪地球3》AI辅助创作
- **内容**：AI工具测评、实用技巧分享
- **链接**：公众号搜索"数字生命卡兹克"

## Cron Setup (Optional)

```bash
openclaw cron add --name "daily-ai-news" --schedule "0 9 * * *" --payload "Check latest AI news" --sessionTarget isolated
```

## Tips

- Hacker News RSS is most reliable
- Expert opinion search uses Bing
- AP News may have rate limiting
- Consider adding custom expert names to the script
