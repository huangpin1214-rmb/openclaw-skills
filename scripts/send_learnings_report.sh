#!/bin/bash
# 每日学习记录总结推送脚本
# 每天 22:50 运行，检查 .learnings 变更并推送飞书消息

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_OUTPUT=$("$SCRIPT_DIR/daily_learnings_report.py" 2>&1)

# 检查是否有变更
HAS_CHANGES=$(echo "$REPORT_OUTPUT" | grep "__HAS_CHANGES__:True" || echo "")

if [ -n "$HAS_CHANGES" ]; then
    # 提取报告内容（去掉内部标记）
    MESSAGE=$(echo "$REPORT_OUTPUT" | sed '/__HAS_CHANGES__:/d')
    
    # 发送飞书消息
    openclaw message send \
        --channel feishu \
        --account default \
        --target "ou_97a37bb8a7fc9beb141b801d9ef83f92" \
        --message "$MESSAGE" \
        2>&1
    
    echo "已发送学习记录总结"
else
    echo "今日无新增变更，无需推送"
fi
