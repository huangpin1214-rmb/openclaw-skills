#!/usr/bin/env python3
"""
根据关键词搜索 Get 笔记，返回相关笔记片段
用法: python3 fetch_notes.py <关键词> [返回数量]
"""
import urllib.request
import json
import sys

API_KEY = "gk_live_d6b346daab8c1120.695c91212fb3dc706bb893e4f77daa54e9207d83ddd29047"
CLIENT_ID = "cli_3802f9db08b811f197679c63c078bacc"
BASE_URL = "https://openapi.biji.com/open/api/v1/resource/recall"

def search_notes(query, top_k=3):
    payload = json.dumps({"query": query, "top_k": top_k})
    req = urllib.request.Request(
        BASE_URL,
        data=payload.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "X-Client-ID": CLIENT_ID,
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    
    results = data.get("data", {}).get("results", [])
    if not results:
        return None
    
    output = []
    for r in results:
        output.append({
            "note_id": r.get("note_id", ""),
            "title": r.get("title", "无标题"),
            "content": r.get("content", ""),
            "created_at": r.get("created_at", ""),
            "note_type": r.get("note_type", ""),
        })
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 fetch_notes.py <关键词> [返回数量]")
        sys.exit(1)
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    results = search_notes(query, top_k)
    if results is None:
        print("未找到相关笔记")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
