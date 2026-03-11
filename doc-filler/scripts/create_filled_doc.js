const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, BorderStyle, ShadingAttributes } = require('docx');
const fs = require('fs');

// Company data from Excel
const companyData = {
  // 1.1 Basic Information
  companyNameCN: "成都星拓微电子科技股份有限公司",
  companyNameEN: "Silicon Innovation Technologies Co.,Ltd",
  companyShortName: "电科星拓",
  website: "https://silicon-innovation-cd.com/",
  companyType: "有限责任公司",
  establishmentDate: "2019.12.26",
  registeredCapital: "3943.2141 万元",
  taxRate: "13%",
  registrationAddress: "中国（四川）自由贸易试验区成都高新区府城大道西段399号7栋3单元14层1409号",
  factoryAddress: "成都市武侯区天府大道北段28号茂业中心C座21层2106号",
  businessScope: "一般项目：技术服务、技术开发、技术咨询、技术交流、技术转让、技术推广；集成电路设计；集成电路销售；智能控制系统集成；信息系统集成服务；计算机系统服务；计算机软硬件及辅助设备零售；计算机软硬件及辅助设备批发；电子元器件批发；电子元器件零售；货物进出口；技术进出口。",
  annualSales: "49000万元（2025年）",
  
  // 1.2 Personnel
  totalEmployees: 254,
  managementStaff: 6,
  technicalStaff: 153,
  qualityStaff: 13,
  
  // 1.3 Financial
  bankName: "中国民生银行股份有限公司成都郫都支行",
  bankCode: "305651000331",
  bankAccount: "161422342",
  currency: "人民币",
  taxCategory: "一般纳税人",
  
  // Contacts
  legalRepresentative: { name: "闫明明", phone: "13518184003", email: "ming@silicon-innovation-cd.com" },
  generalManager: { name: "李丹", phone: "18980958276", email: "lidan@silicon-innovation-cd.com" },
  salesDirector: { name: "马明辉", phone: "18616825418", email: "jacky.ma@silicon-innovation-cd.com" },
  financeDirector: { name: "王晓梅", phone: "18080448151", email: "" },
  contactPerson: { name: "黄频", phone: "18908205072", email: "huangpin@silicon-innovation-cd.com" },
  
  // Certifications
  certifications: [
    { type: "ISO9001:2015 质量管理体系", number: "00125Q35836R1M/5100", authority: "CQC", scope: "模拟和数模混合芯片的研发和销售" },
    { type: "ISO45001:2018 职业健康安全管理体系", number: "00125S32384R1M/5100", authority: "CQC" },
    { type: "ISO14001:2015 环境管理体系", number: "00125E32818R1M/5100", authority: "CQC" }
  ]
};

// Create document
const doc = new Document({
  sections: [{
    properties: {},
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "制造商调查表", bold: true, size: 44, color: "000000" }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "Manufacturer Questionnaire", bold: true, size: 32, color: "000000" }),
        ],
      }),
      new Paragraph({ text: "" }),
      
      // Section 1.1 Basic Information
      new Paragraph({ text: "1.1 基本信息 / Basic Information", heading: "Heading1", bold: true, spacing: { before: 400, after: 200 } }),
      
      // Table for basic info
      new Table({
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "公司名称【中文】", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.companyNameCN })] }),
              new TableCell({ children: [new Paragraph({ text: "Company Name[CN]", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "法人代表", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.legalRepresentative.name })] }),
              new TableCell({ children: [new Paragraph({ text: "Legal Representative", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "公司名称【英文】", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.companyNameEN })] }),
              new TableCell({ children: [new Paragraph({ text: "Company Name[EN]", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "公司网址", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.website })] }),
              new TableCell({ children: [new Paragraph({ text: "Web Site", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "企业性质", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.companyType })] }),
              new TableCell({ children: [new Paragraph({ text: "Type of Company", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "成立时间", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.establishmentDate })] }),
              new TableCell({ children: [new Paragraph({ text: "Date of Foundation", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "注册资本", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.registeredCapital })] }),
              new TableCell({ children: [new Paragraph({ text: "Registered Capital", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "发票税率", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "☑13%  ☐6%  ☐4%  ☐其他" })] }),
              new TableCell({ children: [new Paragraph({ text: "Tax Rate", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "纳税属性", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "☑一般纳税人  ☐小规模纳税人" })] }),
              new TableCell({ children: [new Paragraph({ text: "Tax Category", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "注册地址", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.registrationAddress })] }),
              new TableCell({ children: [new Paragraph({ text: "Register Address", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "工厂地址", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.factoryAddress })] }),
              new TableCell({ children: [new Paragraph({ text: "Factory Address", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "经营范围", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.businessScope, font: { size: 16 } })] }),
              new TableCell({ children: [new Paragraph({ text: "Business Scope", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "上一年度年销售额", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.annualSales })] }),
              new TableCell({ children: [new Paragraph({ text: "Annual Sales", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE }
      }),
      
      // Section 1.2 Personnel
      new Paragraph({ text: "1.2 人员信息 / Personnel Information", heading: "Heading1", bold: true, spacing: { before: 400, after: 200 } }),
      
      new Table({
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "员工总数", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: String(companyData.totalEmployees) + "人" })] }),
              new TableCell({ children: [new Paragraph({ text: "Number of Employees", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "技术人员数量", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: String(companyData.technicalStaff) + "人" })] }),
              new TableCell({ children: [new Paragraph({ text: "Technical Staff", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "质量人员数量", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: String(companyData.qualityStaff) + "人" })] }),
              new TableCell({ children: [new Paragraph({ text: "Quality Staff", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "管理人员数量", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: String(companyData.managementStaff) + "人" })] }),
              new TableCell({ children: [new Paragraph({ text: "Management Staff", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE }
      }),
      
      // Section 1.3 Financial
      new Paragraph({ text: "1.3 财务信息 / Financial Information", heading: "Heading1", bold: true, spacing: { before: 400, after: 200 } }),
      
      new Table({
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "开户银行名称", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.bankName })] }),
              new TableCell({ children: [new Paragraph({ text: "Bank Name", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "开户银行行号", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.bankCode })] }),
              new TableCell({ children: [new Paragraph({ text: "Bank Code", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "开户银行账号", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: String(companyData.bankAccount) })] }),
              new TableCell({ children: [new Paragraph({ text: "Account No.", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "币别", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.currency })] }),
              new TableCell({ children: [new Paragraph({ text: "Currency", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "" })] }),
            ],
          }),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE }
      }),
      
      // Section 1.4 Contacts
      new Paragraph({ text: "1.4 联系人信息 / Contact Information", heading: "Heading1", bold: true, spacing: { before: 400, after: 200 } }),
      
      new Table({
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "职位", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "姓名", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "电话", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "邮箱", bold: true })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "法人代表" })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.legalRepresentative.name })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.legalRepresentative.phone })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.legalRepresentative.email })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "总经理" })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.generalManager.name })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.generalManager.phone })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.generalManager.email })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "销售负责人" })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.salesDirector.name })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.salesDirector.phone })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.salesDirector.email })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "财务负责人" })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.financeDirector.name })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.financeDirector.phone })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.financeDirector.email })] }),
            ],
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "业务联系人" })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.contactPerson.name })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.contactPerson.phone })] }),
              new TableCell({ children: [new Paragraph({ text: companyData.contactPerson.email })] }),
            ],
          }),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE }
      }),
      
      // Certifications
      new Paragraph({ text: "资质证书 / Certifications", heading: "Heading1", bold: true, spacing: { before: 400, after: 200 } }),
      
      new Table({
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ text: "证书类型", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "证书编号", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "认证机构", bold: true })] }),
              new TableCell({ children: [new Paragraph({ text: "认证范围", bold: true })] }),
            ],
          }),
          ...companyData.certifications.map(cert => 
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph({ text: cert.type })] }),
                new TableCell({ children: [new Paragraph({ text: cert.number })] }),
                new TableCell({ children: [new Paragraph({ text: cert.authority })] }),
                new TableCell({ children: [new Paragraph({ text: cert.scope || "" })] }),
              ],
            })
          ),
        ],
        width: { size: 100, type: WidthType.PERCENTAGE }
      }),
      
      // Notes
      new Paragraph({ text: "", spacing: { before: 400 } }),
      new Paragraph({ 
        text: "备注：以上信息根据公司提供的基础资料填写，以下内容需要人工补充：", 
        bold: true,
        color: "FF0000"
      }),
      new Paragraph({ text: "- 工厂面积、库房面积、场地性质" }),
      new Paragraph({ text: "- 近三年资产负债率、现金流、净利润率" }),
      new Paragraph({ text: "- 员工平均月度流失率" }),
      new Paragraph({ text: "- 通讯行业供货经验（客户名单）" }),
      new Paragraph({ text: "- 关键设备信息、关健工序及工序能力Cpk" }),
      new Paragraph({ text: "- 高管和自然人股东信息" }),
      new Paragraph({ text: "- 前10客户及产品线信息" }),
      new Paragraph({ text: "- 关键原材料品牌清单" }),
      new Paragraph({ text: "- 第2、3、4节其他内容" }),
    ],
  }],
});

// Save document
const outputPath = "/home/huangpin/.openclaw/workspace/制造商调查表_填写完成.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("Document created: " + outputPath);
});
