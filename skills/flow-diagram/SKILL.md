---
name: flow-diagram
description: 流程图和图表绘制专家。使用 Mermaid 语法生成流程图、序列图、类图、思维导图、甘特图等。帮助用户快速创建专业的技术文档图表。
---

# Flow Diagram - 流程图绘制专家

使用 Mermaid 语法快速生成各类图表。

## 支持的图表类型

1. **流程图 (Flowchart)** - 业务流程、决策流程
2. **序列图 (Sequence Diagram)** - 交互时序
3. **类图 (Class Diagram)** - UML 类结构
4. **状态图 (State Diagram)** - 状态机
5. **ER 图 (Entity-Relationship)** - 数据库设计
6. **甘特图 (Gantt Chart)** - 项目进度
7. **思维导图 (Mindmap)** - 脑图
8. **Pie 饼图** - 比例分布

## 触发场景

- "画个流程图"
- "帮我画一个 XXX 流程图"
- "生成序列图"
- "做个思维导图"
- "画个时序图"

## 使用方式

### 方式 1：命令行自动生成（推荐 ✅）

```bash
# 生成登录流程图
python3 ~/.openclaw/workspace/skills/flow-diagram/scripts/auto_diagram.py login

# 生成订单流程图
python3 ~/.openclaw/workspace/skills/flow-diagram/scripts/auto_diagram.py order

# 生成微服务架构图
python3 ~/.openclaw/workspace/skills/flow-diagram/scripts/auto_diagram.py microservice

# 生成序列图
python3 ~/.openclaw/workspace/skills/flow-diagram/scripts/auto_diagram.py sequence

# 生成 SVG 格式
python3 ~/.openclaw/workspace/skills/flow-diagram/scripts/auto_diagram.py login svg
```

### 方式 2：描述需求，自动生成

直接描述你想要什么图：
- "帮我画一个用户登录的流程图"
- "生成订单处理的全流程"
- "画一个微服务架构图"

### 方式 2：Mermaid 语法预览

```mermaid
graph TD
    A[开始] --> B{判断}
    B -->|是| C[处理1]
    B -->|否| D[处理2]
    C --> E[结束]
    D --> E
```

### 方式 3：命令行生成图片

```bash
# 安装 Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 生成 PNG 图片
mmdc -i input.mmd -o output.png

# 生成 SVG
mmdc -i input.mmd -o output.svg
```

## 常用 Mermaid 语法

### 流程图

```mermaid
graph TD
    A[矩形] --> B(圆角)
    B --> C{菱形}
    C -->|Yes| D[方形]
    C -->|No| E[圆形]
    
    subgraph 子图
    D
    E
    end
```

### 序列图

```mermaid
sequenceDiagram
    participant A as 客户端
    participant B as 服务器
    participant C as 数据库
    
    A->>B: 请求
    B->>C: 查询
    C-->>B: 返回结果
    B-->>A: 响应
```

### 思维导图

```mermaid
mindmap
  root((项目))
    设计
      UI
      架构
    开发
      前端
      后端
    测试
      单元
      集成
```

### 甘特图

```mermaid
gantt
    title 项目进度
    dateFormat YYYY-MM-DD
    section 设计
    需求分析: a1, 2024-01-01, 7d
    UI设计: a2, after a1, 5d
    section 开发
    前端: b1, after a2, 10d
    后端: b2, after a2, 12d
```

### 类图

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog
```

### ER 图

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : appears_in
```

## 快速生成示例

### 用户登录流程

```mermaid
graph LR
    A[用户输入账号密码] --> B{验证成功?}
    B -->|是| C[生成Token]
    B -->|否| D[返回错误]
    C --> E[存储Token]
    E --> F[跳转首页]
    D --> A
```

### 订单处理流程

```mermaid
graph TD
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
    G --> K
```

### 微服务架构

```mermaid
graph TB
    subgraph 客户端
    A[Web App]
    B[Mobile App]
    end
    
    subgraph 网关层
    C[API Gateway]
    end
    
    subgraph 服务层
    D[用户服务]
    E[订单服务]
    F[商品服务]
    end
    
    subgraph 数据层
    G[(MySQL)]
    H[(Redis)]
    I[(MongoDB)]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    C --> F
    D --> G
    D --> H
    E --> G
    F --> I
```

## 在线预览工具

- Mermaid Live: https://mermaid.live/ (可导出 PNG/SVG/PDF)
- Draw.io: https://draw.io (可导出 PDF/PPT)
- PlantUML: https://plantuml.com

## 导出 PDF/PPT 方法

### 方法 1：Mermaid Live（推荐）

1. 打开 https://mermaid.live/
2. 粘贴 Mermaid 代码
3. 点击导出 → 选择格式（PNG/SVG/PDF）

### 方法 2：Draw.io

1. 打开 https://draw.io/
2. 选择 "Presentation" 模式
3. 手动创建或导入图表
4. 文件 → 导出 → PDF/PPT

### 方法 3：本地命令行（需要安装）

```bash
# 安装 Node.js 后
npm install -g @mermaid-js/mermaid-cli

# 生成 PNG
mmdc -i diagram.mmd -o diagram.png

# 生成 SVG
mmdc -i diagram.mmd -o diagram.svg
```

### 方法 4：Python 脚本生成 PPT

需要安装 python-pptx：
```bash
pip install python-pptx
```

## 技巧

1. 使用 `subgraph` 组织复杂流程
2. 用不同形状表达不同含义：`[]` 矩形、`()` 圆角、`{}` 菱形
3. 序列图用 `-->` 表示虚线，`->>` 表示实线
4. 用 `|标签|` 给分支加说明
5. 注释用 `%%`

## 输出格式

当用户需要图表时：
1. 先用 Mermaid 语法生成代码
2. 提供在线预览链接
3. 如需要图片，提供命令行转换方法
