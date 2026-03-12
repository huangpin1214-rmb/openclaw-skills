#!/usr/bin/env python3
"""
流程图快速生成工具
"""

import sys
import os

TEMPLATES = {
    "login": """graph LR
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

    "mindmap": """mindmap
  root((主题))
    方面一
      子项A
      子项B
    方面二
      子项C
      子项D""",

    "gantt": """gantt
    title 项目进度
    dateFormat YYYY-MM-DD
    section 阶段一
    任务A: a1, 2024-01-01, 7d
    任务B: a2, after a1, 5d
    section 阶段二
    任务C: b1, after a2, 10d
    任务D: b2, after b1, 5d""",
}

def show_templates():
    print("\n📊 可用的流程图模板：\n")
    for name, _ in TEMPLATES.items():
        print(f"  • {name}")
    print("\n使用: python3 diagram.py <模板名>")
    print("例如: python3 diagram.py login")

def generate(template_name):
    if template_name not in TEMPLATES:
        print(f"❌ 未知模板: {template_name}")
        show_templates()
        return
    
    mmd = TEMPLATES[template_name]
    filename = f"{template_name}.mmd"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(mmd)
    
    print(f"\n✅ 已生成: {filename}")
    print("\n--- Mermaid 代码 ---\n")
    print(mmd)
    print("\n--- 在线预览 ---")
    print("复制以上代码到: https://mermaid.live/")
    print(f"\n或使用 mmdc 生成图片: mmdc -i {filename} -o {filename}.png")

def main():
    if len(sys.argv) < 2:
        show_templates()
        return
    
    template = sys.argv[1]
    generate(template)

if __name__ == "__main__":
    main()
