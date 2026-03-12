#!/usr/bin/env python3
"""
流程图自动生成器 - 使用 Kroki API
全自动生成 PNG/SVG，无需安装任何依赖
"""

import subprocess
import sys
import os
import tempfile

def mermaid_to_png(mermaid_code):
    """使用 Kroki API 将 Mermaid 转换为 PNG"""
    # 使用 curl 调用 API
    cmd = [
        'curl', '-s', '-X', 'POST',
        'https://kroki.io/mermaid/png',
        '-H', 'Content-Type: text/plain',
        '-d', mermaid_code,
        '-o', '/tmp/mermaid_output.png',
        '-w', '%{http_code}'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout.strip() == '200':
        with open('/tmp/mermaid_output.png', 'rb') as f:
            return f.read(), None
    else:
        return None, f"HTTP {result.stdout}"

def mermaid_to_svg(mermaid_code):
    """使用 Kroki API 将 Mermaid 转换为 SVG"""
    cmd = [
        'curl', '-s', '-X', 'POST',
        'https://kroki.io/mermaid/svg',
        '-H', 'Content-Type: text/plain',
        '-d', mermaid_code,
        '-o', '/tmp/mermaid_output.svg',
        '-w', '%{http_code}'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout.strip() == '200':
        with open('/tmp/mermaid_output.svg', 'r', encoding='utf-8') as f:
            return f.read(), None
    else:
        return None, f"HTTP {result.stdout}"

def save_file(content, filename, is_binary=False):
    """保存文件"""
    mode = 'wb' if is_binary else 'w'
    encoding = None if is_binary else 'utf-8'
    with open(filename, mode, encoding=encoding) as f:
        f.write(content)
    return filename

# 模板
TEMPLATES = {
    "login": """graph TD
    A[用户访问] --> B{已登录?}
    B -->|是| C[显示首页]
    B -->|否| D[跳转登录]
    D --> E[输入账号密码]
    E --> F{验证成功?}
    F -->|是| G[生成Token]
    F -->|否| H[显示错误]
    H --> E
    G --> C""",

    "order": """graph TD
    A[客户下单] --> B{库存充足?}
    B -->|是| C[锁定库存]
    B -->|否| D[提示缺货]
    C --> E{支付成功?}
    E -->|是| F[扣减库存]
    E -->|否| G[释放库存]
    F --> H[发货]
    H --> I[客户收货]
    I --> J[完成]
    D --> K[取消订单]
    G --> K""",

    "microservice": """graph TB
    subgraph 客户端
    A[Web]
    B[App]
    end
    subgraph 网关
    C[API Gateway]
    end
    subgraph 服务
    D[用户服务]
    E[订单服务]
    F[商品服务]
    end
    subgraph 数据
    G[(MySQL)]
    H[(Redis)]
    end
    A --> C
    B --> C
    C --> D
    C --> E
    C --> F
    D --> G
    D --> H
    E --> G
    F --> G""",

    "sequence": """sequenceDiagram
    participant U as 用户
    participant S as 服务器
    participant D as 数据库
    U->>S: 发起请求
    S->>D: 查询数据
    D-->>S: 返回结果
    S-->>U: 响应""",
}

def generate(template_name, output_format='png'):
    """生成流程图"""
    if template_name not in TEMPLATES:
        print(f"❌ 未知模板: {template_name}")
        print(f"可用模板: {', '.join(TEMPLATES.keys())}")
        return
    
    mermaid_code = TEMPLATES[template_name]
    print(f"📊 正在生成 {template_name} 流程图...")
    
    if output_format == 'svg':
        svg, error = mermaid_to_svg(mermaid_code)
        if error:
            print(f"❌ 生成失败: {error}")
            return
        filename = save_file(svg, f"{template_name}.svg")
        print(f"✅ 已生成: {filename}")
    else:
        png, error = mermaid_to_png(mermaid_code)
        if error:
            print(f"❌ 生成失败: {error}")
            return
        filename = save_file(png, f"{template_name}.png", is_binary=True)
        print(f"✅ 已生成: {filename}")
    
    print(f"\n📂 文件位置: {os.path.abspath(filename)}")

def main():
    if len(sys.argv) < 2:
        print("""
📊 流程图自动生成器

用法:
  python3 auto_diagram.py <模板名> [格式]

模板:
  login         - 用户登录流程
  order        - 订单处理流程
  microservice - 微服务架构
  sequence     - 序列图

格式: png (默认), svg

示例:
  python3 auto_diagram.py login
  python3 auto_diagram.py order png
  python3 auto_diagram.py microservice svg
        """)
        return
    
    template = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'png'
    
    generate(template, output_format)

if __name__ == "__main__":
    main()
