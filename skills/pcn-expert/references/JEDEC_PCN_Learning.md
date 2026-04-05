# JEDEC PCN 规范学习摘要

> 学习时间: 2026-04-05
> 资料来源: 
> - JEDEC可靠性标准学习报告.md（第24-27节）
> - 主流芯片厂商PCN调研报告.pdf（飞书文件夹）
> - 厂商实际PCN案例（TI/Intel/NXP/NVIDIA）
> ⚠️ 本文档为学习摘要+实际案例，非JEDEC官方原文。

---

## 一、JESD46 - 产品变更通知（PCN）要求

### 1.1 适用范围
- 适用于固态半导体产品（固态存储器、微处理器等）
- 定义何时需要向客户发出变更通知

### 1.2 变更分类

| 类别 | 说明 |
|------|------|
| 封装变更 | 封装尺寸、材料、供应商变更 |
| 制造变更 | 代工厂、晶圆厂变更 |
| 规格变更 | 电气参数、热参数调整 |
| 标识变更 | Marking/标识变更 |
| 停产通知 | EOL (End of Life) |

### 1.3 通知要求

| 变更类型 | 是否需要通知 | 是否需要客户承认 |
|---------|------------|----------------|
| 封装尺寸变更 | ✅ | ✅ |
| 封装材料变更 | ✅ | ✅ |
| 代工厂变更 | ✅ | ✅ |
| 规格收紧 | ✅ | ⚠️ 评估后决定 |
| 规格放宽 | ⚠️ 评估影响 | ⚠️ 评估后决定 |
| 标识变更 | ❌ | ❌ |
| 环保标识变更 | ❌ | ❌ |

### 1.4 客户批准流程

1. 供应商发出PCN
2. 客户评估影响
3. 客户回复Acknowledgment
4. 供应商确认并执行变更

---

## 二、J-STD-046 - PCN要求（取代JESD46）

### 2.1 主要变更（相对于JESD46）
- 明确了form-fit-function评估标准
- 细化了客户承认流程
- 增加了样品要求

### 2.2 通知内容要求

PCN必须包含：
- 变更产品型号
- 变更类型和描述
- 变更原因
- 变更生效日期
- 影响评估（电气/热/机械）
- 样品提供计划（如需要）
- 客户确认截止日期
- 联系人信息

---

## 三、J-STD-048 - 产品生命周期结束管理（EOL）

### 3.1 停产通知要求
- 必须提前通知客户
- 明确Last-Time-Buy (LTB) 窗口
- 明确最后发货日期

### 3.2 LTB窗口
- 通常6-12个月
- 客户需在LTB窗口内完成采购
- 超过LTB后不再接受订单

---

## 四、J-STD-609 - 环保标识要求

### 4.1 Pb-free标识
- 无铅产品必须标注Pb-free标识
- 符合RoHS指令

### 4.2 卤素要求
- 无卤素产品需符合J-STD-609C.01
- 氯(Cl) ≤ 900ppm
- 溴(Br) ≤ 900ppm

---

## 五、主流厂商PCN实际格式（学习自TI/Intel/NXP/NVIDIA）

### 5.1 PCN标准结构

```
1. 头部信息
   - 公司名称+地址
   - PCN编号（如：PCN# 20250213002.1）
   - 标题（变更描述）
   - 日期
   - 收件人

2. 变更通知类型
   - Change Notification / Sample Request（需确认）
   - Information Only（仅通知，无需回复）

3. 客户须知
   - 确认期限（如：60天内）
   - 默认接受条款（如：30/60天无回复视为接受）
   - 样品申请说明

4. 关键里程碑
   - Proposed 1st Ship Date（首次发货日期）
   - Sample Request Date（样品申请截止）

5. 变更类型（打勾选择）
   □ Assembly Site    □ Design       □ Wafer Bump Material
   □ Assembly Process □ Data Sheet    □ Wafer Bump Process
   □ Assembly Materials □ Part number change □ Wafer Fab Site
   □ Mechanical Specification □ Test Site □ Wafer Fab Materials
   □ Packing/Shipping/Labeling □ Test Process □ Wafer Fab Process

6. 变更详细描述
   - Current XX → New XX（表格对比）
   - Qual details provided in Qual Data Section

7. 变更原因
   - 如：Continuity of Supply / Cost Reduction / Quality Improvement

8. 影响评估
   - Anticipated impact on Form, Fit, Function, Quality, Reliability
   - Positive / Negative / None

9. 产品标识变更说明
   - 如：Changes to product identification resulting from this PCN

10. 受影响产品完整清单
    - DEVICE | CUSTOMER PART NUMBER 表格
```

### 5.2 厂商差异总结

| 差异点 | TI | Intel | Infineon/Broadcom |
|--------|-----|-------|-------------------|
| 通知性质 | Information Only + 需确认两类 | Minor/Major分类 | 通常需确认 |
| 默认期限 | 60天 | 30天 | 30天 |
| 供应商披露 | 不披露具体供应商名 | 不披露具体供应商名 | 不披露 |
| 影响说明 | 简洁"None" | 简洁"无影响" | 逐条详细说明 |
| Minor vs Major | 不显式标注 | 标题冠以"MINOR CHANGE" | 标注"Major" |

### 5.3 Intel PCN Minor变更示例

> "Intel considers this a MINOR CHANGE. There is no change to the form, fit, functionality, quality or reliability for any of the downstream products."

### 5.4 厂商PCN案例文件

| 文件 | 说明 |
|------|------|
| `TI_PCN20250213002.pdf` | TI Die Coat材料变更PCN（2025年2月） |
| `Intel_PCN119527.pdf` | Intel电阻供应商变更PCN（Minor） |
| `NXP_Final_PCN.pdf` | NXP产品变更PCN |
| `NVIDIA_Jetson_TX1_TX2_PCN.pdf` | NVIDIA Jetson模块PCN |
| `PCN常见问题FAQ.docx` | PCN常见问题FAQ |

---

## 六、常见PCN触发条件速查

| 场景 | 是否需要发PCN | 依据 |
|------|-------------|------|
| 封装供应商从A换成B | ✅ 需要 | J-STD-046 |
| 封装尺寸变更 | ✅ 需要 | J-STD-046 |
| 代工厂换厂 | ✅ 需要 | J-STD-046 |
| 晶圆工艺调整 | ✅ 需要 | J-STD-046 |
| 电气参数收紧 | ⚠️ 评估 | J-STD-046 |
| 标识字体变更 | ❌ 不需要 | JESD46 |
| 环保标识变更 | ❌ 不需要 | J-STD-609 |

---

*本文档为学习摘要+实际案例，完整规范请参考JEDEC官方原文*
