---
name: web-search
description: Search the web for information and fetch web content. Use when the user asks to look up something online, search for information, find answers, or retrieve content from URLs. Handles general web searches, URL content fetching, information extraction from web pages, looking up definitions facts or current events.
---

# Web Search

## Quick Start

Use `curl` with search engines or directly fetch URLs:

```bash
# Simple search via DuckDuckGo HTML
curl -s "https://html.duckduckgo.com/html/?q=your+search+query"

# Fetch a webpage
curl -s "https://example.com"

# Search via Bing (may require API key)
curl -s "https://api.bing.microsoft.com/v7.0/search?q=query"
```

## Common Tasks

### 1. General Web Search

Use DuckDuckGo HTML for simple searches (no API key required):

```bash
curl -s "https://html.duckduckgo.com/html/?q=search+term" | grep -oP '(?<=<a class="result__a" href=")[^"]+' | head -5
```

Or use textise dot iitty for cleaner output:

```bash
curl -s "https://duckduckgo.com/html/?q=search+term&format=json"
```

### 2. Fetching Webpage Content

```bash
# Basic fetch
curl -sL "https://example.com"

# With headers
curl -sL -H "User-Agent: Mozilla/5.0" "https://example.com"

# Download to file
curl -LO "https://example.com/file.pdf"
```

### 3. JSON API Queries

Many services offer free JSON APIs:

```bash
# Wikipedia API
curl -s "https://en.wikipedia.org/api/rest_v1/page/summary/Topic"

# GitHub API
curl -s "https://api.github.com/repos/owner/repo"
```

### 4. Extracting Information

Use grep/sed/awk or parse with tools:

```bash
# Extract all links
curl -sL "https://example.com" | grep -oP 'href="[^"]*"'

# Extract specific content
curl -sL "https://example.com" | grep -oP '<title>[^<]+</title>'
```

## Tips

- Always use `-s` (silent) and `-L` (follow redirects) for cleaner output
- Add `-H "User-Agent: Mozilla/5.0"` to avoid being blocked
- For heavy scraping, respect robots.txt and add delays
- Use `jq` to parse JSON responses: `curl -s API_URL | jq '.key'`
