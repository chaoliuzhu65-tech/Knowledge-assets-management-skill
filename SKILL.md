---
name: knowledge-assets-skill
description: 个人知识资产全面复用与实时检索能力。本地扫描知识文档 + 外网实时检索最新信息 + AI融合生成升级版报告 + 钉钉/飞书自动归档推送。让个人知识持续增值。
license: MIT
version: 2.0.0
homepage: https://github.com/chaoliuzhu65-tech/Knowledge-assets-management-skill
metadata:
  openclaw:
    requires:
      bins: ["python3", "curl"]
    primaryEnv: KNOWLEDGE_BASE_PATH
    dependsOn:
      - dingtalk-mcp-skill
      - lark-feishu-skill
---

# 知识资产管理助手 (knowledge-assets-skill) v2.0

> 让你的个人知识资产持续增值：本地扫描 + 外网实时检索 + AI融合升级 + 多渠道归档

---

## 🚀 核心价值

> **旧知识 + 新信息 = 升级知识**

普通打工人每天产生大量文档（Markdown、HTML、PDF、代码注释），但这些知识往往躺在硬盘里沉睡。本 SKILL 通过三步走：

1. **扫描**：自动扫描本地所有知识文档（排除 node_modules、.git 等噪音）
2. **检索**：实时上网检索相关领域的最新动态（AI趋势、技术更新、行业新闻）
3. **融合**：AI 对比新旧知识，生成结构化的**知识升级报告**

最后自动推送到钉钉/飞书，让知识沉淀到团队协作空间。

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 本地知识扫描 | 支持自定义路径，自动过滤无效文件（node_modules、.git、dist） |
| 主题知识盘点 | 按关键词（如"AI"、"高德"、"飞书"）汇总本地所有相关文档 |
| 外网实时检索 | 内置 4 种检索策略：技术进展 / 最佳实践 / 行业动态 / 竞品对比 |
| 知识升级报告 | 结构化输出：盘点概况 + 现有积累 + 外网动态 + 升级对比表 + 行动建议 |
| 多渠道推送 | 支持钉钉 Markdown、飞书交互卡片双路同时送达 |
| 自动归档 | 可选将报告写入飞书知识库（需配置权限） |

---

## 📦 快速开始

### 前置依赖

| 依赖 | 用途 | 说明 |
|------|------|------|
| Python 3.8+ | 脚本执行 | 系统自带或 brew install python3 |
| curl | 外网检索 API | 系统自带 |
| WorkBuddy | SKILL 运行环境 | https://workbuddy.ai |
| dingtalk-mcp-skill（可选）| 钉钉推送 | https://github.com/chaoliuzhu65-tech/dingtalk-mcp-skill |
| lark-feishu-skill（可选）| 飞书推送 | https://github.com/larksuite/openclaw-lark |

### 配置步骤

#### 步骤 1：复制本 SKILL 到 WorkBuddy

```bash
# 复制整个 skill 目录到 WorkBuddy
cp -r knowledge-assets-skill ~/WorkBuddy/skills/knowledge-assets-skill
```

#### 步骤 2：创建配置文件（可选）

在 SKILL 目录下创建 `.env`：

```bash
cd ~/WorkBuddy/skills/knowledge-assets-skill
cp .env.example .env
```

编辑 `.env`：

```bash
# 本地知识库根路径（默认扫描整个用户目录）
KNOWLEDGE_BASE_PATH=~

# 外网检索偏好（可选：openai / bing / google，默认bing）
SEARCH_ENGINE=bing

# 推送渠道（逗号分隔，留空则不自动推送）
CHANNELS=dingtalk,feishu
```

#### 步骤 3：配置钉钉 / 钉钉 Webhook（如需推送）

创建 `dingtalk/.env`：

```bash
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
DINGTALK_WEBHOOK_SECRET=
```

#### 步骤 4：配置飞书（如需推送）

创建 `feishu/.env`：

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHAT_ID=oc_xxx
```

---

## 🎯 使用示例

### 示例 1：单文档知识升级

> 场景：你有一篇旧的技术文档，想知道现在是否需要更新

```
帮我升级这篇文档：~/Documents/2024年AI应用总结.md
```

**执行流程**：
1. 读取文档内容
2. AI 提炼核心知识点
3. 外网检索 "AI应用 2026 最新进展"
4. 生成对比报告
5. （可选）推送到钉钉/飞书

---

### 示例 2：主题知识全量盘点

> 场景：你想了解自己在某个领域的知识积累情况

```
盘点我电脑上所有关于"高德地图API"的知识，并结合最新文档升级
```

**执行流程**：
1. 在 `~/` 下搜索所有含"高德地图API"的 Markdown 文件
2. 汇总提炼核心知识脉络
3. 外网检索 "高德地图 JSAPI v2.0 2026 最新特性"
4. 生成升级报告（含：现有积累 + 新增知识 + 行动建议）

---

### 示例 3：自动化知识晨报

> 场景：每天早上自动推送知识日报

```
生成今日知识晨报，扫描昨天的新文档，加上AI行业最新动态
```

**执行流程**：
1. 扫描昨日新增/修改的文档（`find -newer`）
2. 提炼新增知识点
3. 外网检索 "AI Agent 2026 趋势"
4. 生成晨报
5. 推送到钉钉群

---

## 📋 知识升级报告模板

```markdown
# [知识升级报告] {主题} — {YYYY-MM-DD}

## 📊 盘点概况
- 扫描文档数：N 篇
- 知识覆盖时间：{最早日期} ~ {最新日期}
- 核心知识域：{列举}

## 🏛️ 现有知识积累
{从本地文档提炼的核心知识点，3-8条，每条100字内}

## 🌐 外网最新动态（实时检索）
{web_search 检索结果的关键信息，标注来源URL}

## 🔄 知识升级点
| 旧知识 | 新信息 | 升级结论 |
|--------|--------|----------|
| ... | ... | ... |

## 💡 行动建议
1. {建议1}
2. {建议2}

## 🏷️ 标签
`{领域}` `{技术}` `{时间}`
```

---

## 🔧 高级配置

### 本地知识扫描策略

编辑 `config/scan_rules.json`：

```json
{
  "include_extensions": [".md", ".txt", ".html", ".py", ".js"],
  "exclude_dirs": ["node_modules", ".git", "dist", "build"],
  "max_depth": 6,
  "max_files": 500
}
```

### 外网检索策略

编辑 `config/search_strategies.json`：

```json
{
  "tech_latest": "{技术名} 2026 最新特性",
  "best_practices": "{技术名} best practices 2026",
  "industry_trends": "{行业} AI 应用 2026",
  "competitor_analysis": "{产品} vs 竞品 2026"
}
```

### 推送格式自定义

编辑 `config/push_templates.json`：

```json
{
  "dingtalk": {
    "msgtype": "markdown",
    "title": "🧠 知识升级报告",
    "include_sections": ["盘点概况", "现有知识积累", "外网动态", "行动建议"]
  },
  "feishu": {
    "template": "blue",
    "wide_screen_mode": true
  }
}
```

---

## 📂 项目结构

```
knowledge-assets-skill/
├── SKILL.md                 # 本文件
├── _meta.json              # WorkBuddy SKILL 元数据
├── README.md               # 使用文档（GitHub 展示用）
├── .env.example           # 配置文件模板
├── clawhub.json           # ClawHub 元数据
├── LICENSE                # MIT 协议
├── scripts/              # 工作流脚本
│   ├── scan_local.py    # 本地知识扫描
│   ├── web_search.py    # 外网检索
│   ├── merge_knowledge.py # 知识融合
│   ├── push_dingtalk.py # 钉钉推送
│   └── push_feishu.py   # 飞书推送
├── config/               # 配置文件
│   ├── scan_rules.json
│   ├── search_strategies.json
│   └── push_templates.json
├── dingtalk/            # 钉钉配置（用户自行创建）
│   └── .env
└── feishu/             # 飞书配置（用户自行创建）
    └── .env
```

---

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request！

**贡献方向**：
- 新增更多外网检索源（支持更多搜索引擎）
- 优化本地扫描性能（并行、增量扫描）
- 新增更多推送渠道（Slack、企业微信等）
- 改进知识融合算法（RAG、图谱化）

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 相关项目

- [dingtalk-mcp-skill](https://github.com/chaoliuzhu65-tech/dingtalk-mcp-skill) - 钉钉 MCP 插件
- [lark-feishu-skill](https://github.com/larksuite/openclaw-lark) - 飞书 MCP 插件
- [WorkBuddy](https://workbuddy.ai) - AI 编程助手平台

---

> **让知识不再沉睡，让学习持续增值** 🚀
