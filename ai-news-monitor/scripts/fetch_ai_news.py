#!/usr/bin/env python3
"""AI News Fetcher - Fetches latest AI news and opinions from multiple sources."""

import subprocess
import re
import html
import time
import xml.etree.ElementTree as ET
from datetime import datetime

def run_curl(url, timeout=10):
    """Run curl command and return output."""
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', str(timeout), url],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def parse_rss(xml_content, max_items=10):
    """Parse RSS feed and extract titles and links."""
    articles = []
    try:
        xml_content = re.sub(r'<!\[CDATA\[', '', xml_content)
        xml_content = re.sub(r'\]\]>', '', xml_content)
        xml_content = re.sub(r'&(?![a-zA-Z]+;)', '&amp;', xml_content)
        
        root = ET.fromstring(xml_content)
        for item in root.findall('.//item'):
            title_elem = item.find('title')
            link_elem = item.find('link')
            if title_elem is not None and title_elem.text:
                title = html.unescape(title_elem.text.strip())
                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                articles.append({
                    'title': title,
                    'link': link,
                    'source': 'Hacker News'
                })
                if len(articles) >= max_items:
                    break
    except:
        try:
            titles = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', xml_content)
            links = re.findall(r'<link>([^<]+)</link>', xml_content)
            for i, title in enumerate(titles[:max_items]):
                if i < len(links):
                    articles.append({
                        'title': html.unescape(title.strip()),
                        'link': links[i].strip(),
                        'source': 'Hacker News'
                    })
        except:
            pass
    return articles

def fetch_hackernews_frontpage(max_items=8):
    """Fetch from Hacker News front page."""
    url = "https://hnrss.org/frontpage"
    content = run_curl(url)
    return parse_rss(content, max_items)

def fetch_hackernews_ai(max_items=8):
    """Fetch AI-related stories from Hacker News."""
    queries = ["openai", "anthropic", "chatgpt", "llm", "AI"]
    all_articles = []
    
    for query in queries[:2]:
        url = f"https://hnrss.org/newest?q={query}"
        content = run_curl(url)
        articles = parse_rss(content, max_items=5)
        all_articles.extend(articles)
        time.sleep(0.5)
    
    seen = set()
    unique = []
    for a in all_articles:
        if a['title'] not in seen:
            seen.add(a['title'])
            unique.append(a)
    
    return unique[:max_items]

def fetch_ap_ai_hub(max_results=5):
    """Fetch from AP News AI hub."""
    url = "https://apnews.com/hub/artificial-intelligence"
    html_content = run_curl(url)
    
    slugs = re.findall(r'apnews\.com/article/([a-z0-9-]+)', html_content)
    slugs = list(dict.fromkeys(slugs))[:max_results]
    
    articles = []
    for slug in slugs:
        article_url = f"https://apnews.com/article/{slug}"
        title = fetch_ap_title(article_url)
        if title:
            articles.append({'title': title, 'link': article_url, 'source': 'AP News'})
        time.sleep(0.5)
    
    return articles

def fetch_ap_title(url):
    """Fetch title from an AP News article."""
    html_content = run_curl(url, timeout=5)
    match = re.search(r'<meta property="og:title" content="([^"]+)"', html_content)
    if match:
        return html.unescape(match.group(1))
    return None

def fetch_ai_experts_opinions(max_items=8):
    """Fetch AI expert opinions via Bing search for quotes and opinions."""
    # AI industry leaders and their recent statements
    experts = [
        "Sam Altman",
        "Dario Amodei", 
        "Demis Hassabis",
        "Sam Altman OpenAI opinion 2026",
        "Dario Amodei Anthropic interview 2026",
    ]
    
    articles = []
    
    # Use Bing to search for expert opinions
    for expert in experts[:3]:
        url = f"https://www.bing.com/search?q={expert.replace(' ', '+')}+AI+opinion+2026"
        content = run_curl(url, timeout=8)
        
        # Extract titles from search results
        titles = re.findall(r'class="b_topp[^"]*"[^>]*>([^<]+)<', content)
        for title in titles[:2]:
            title = title.strip()
            if title and len(title) > 10:
                articles.append({
                    'title': title,
                    'link': '',
                    'source': f'Expert: {expert}'
                })
        time.sleep(0.5)
    
    return articles[:max_items]

def main():
    print(f"🤖 AI News Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    all_articles = []
    
    # Section 1: Hacker News Front Page
    print("\n📰 Hacker News Front Page...")
    try:
        articles = fetch_hackernews_frontpage(max_items=6)
        for i, a in enumerate(articles[:4], 1):
            print(f"  {i}. {a['title'][:65]}")
        all_articles.extend(articles)
    except Exception as e:
        print(f"  Error: {e}")
    
    # Section 2: Hacker News AI
    print("\n📰 Hacker News (AI)...")
    try:
        articles = fetch_hackernews_ai(max_items=6)
        for i, a in enumerate(articles[:5], 1):
            print(f"  {i}. {a['title'][:65]}")
        all_articles.extend(articles)
    except Exception as e:
        print(f"  Error: {e}")
    
    # Section 3: AP News AI
    print("\n📰 AP News (AI)...")
    try:
        articles = fetch_ap_ai_hub(max_results=4)
        for i, a in enumerate(articles[:3], 1):
            print(f"  {i}. {a['title'][:65]}")
        all_articles.extend(articles)
    except Exception as e:
        print(f"  Error: {e}")
    
    # Section 4: AI Expert Opinions
    print("\n🎤 AI Expert Opinions & Perspectives...")
    try:
        articles = fetch_ai_experts_opinions(max_items=5)
        for i, a in enumerate(articles[:4], 1):
            print(f"  {i}. {a['title'][:65]}")
            if a['source']:
                print(f"     [{a['source']}]")
        all_articles.extend(articles)
    except Exception as e:
        print(f"  Error: {e}")
    
    # Remove duplicates
    seen = set()
    unique_articles = []
    for a in all_articles:
        title_lower = a['title'].lower()[:50]
        if title_lower not in seen:
            seen.add(title_lower)
            unique_articles.append(a)
    
    print(f"\n📊 Total: {len(unique_articles)} unique articles")
    print("=" * 70)

if __name__ == "__main__":
    main()
