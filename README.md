# 知识资产管理助手 v2.0

> **让个人知识持续增值**：本地扫描 + 外网实时检索 + AI 融合升级 + 多渠道归档

---

## 📌 为什么需要这个工具？

普通打工人每天都在产生知识：
- 写过技术文档，后来技术更新了，文档没更新 ❌
- 看过行业文章，后来行业变了，文章躺在硬盘里 ❌
- 学过新工具，后来工具升级了，教程过时了 ❌

**结果**：知识资产不仅没增值，反而贬值了。

---

## ✨ 本工具能做什么？

| 你做的事 | 工具做的事 | 价值 |
|----------|------------|------|
| 写了篇 AI 应用文档 | 扫描 + 外网检索 "AI 2026 趋势" + 对比 | 告诉你文档哪里需要更新 |
| 学了高德地图 API | 扫描 + 检索 "高德 JSAPI v2.0 新特性" | 告诉你用了哪些过时 API |
| 积累 100 篇飞书开发笔记 | 自动归档 + 钉钉/飞书双路推送 | 团队共享，知识可复用 |

---

## 🚀 3 分钟快速上手

### 1. 安装依赖

```bash
# 系统自带 Python 3.8+ 即可
python3 --version  # 确保版本 >= 3.8
```

### 2. 复制到 WorkBuddy

```bash
# 克隆仓库
git clone https://github.com/chaoliuzhu65-tech/Knowledge-assets-management-skill.git

# 复制到 WorkBuddy skills 目录
cp -r Knowledge-assets-management-skill/skills/knowledge-assets-skill ~/WorkBuddy/skills/
```

### 3. 配置推送（可选）

#### 钉钉推送

创建 `~/WorkBuddy/skills/knowledge-assets-skill/dingtalk/.env`：

```bash
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
DINGTALK_WEBHOOK_SECRET=
```

#### 飞书推送

创建 `~/WorkBuddy/skills/knowledge-assets-skill/feishu/.env`：

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHAT_ID=oc_xxx
```

### 4. 开始使用

打开 WorkBuddy，直接对话：

```
帮我升级这篇文档：~/Documents/AI应用总结.md
```

---

## 💡 使用示例

### 示例 1：单文档升级

**输入**：
```
帮我升级：~/Desktop/飞书开发笔记.md
```

**输出**：
- 📊 扫描到 1 篇文档，提炼 5 个知识点
- 🌐 检索到 "飞书开放平台 2026 新特性"
- 🔄 生成对比表：旧 API → 新 API
- 💡 建议更新 2 处 API 调用
- 📤 （可选）推送到钉钉群

---

### 示例 2：主题知识盘点

**输入**：
```
盘点我所有关于"高德地图"的知识
```

**输出**：
- 📊 扫描到 15 篇相关文档
- 🏛️ 现有知识：JSAPI v1.4 集成经验、逆地理编码、路线规划
- 🌐 外网动态：JSAPI 已升级到 v2.0，新增 WebGL 地图
- 🔄 升级建议：3 个示例代码需要迁移到 v2.0
- 📤 （可选）推送到飞书群

---

### 示例 3：知识晨报

**输入**：
```
生成今日知识晨报，扫描昨天的新文档
```

**输出**：
- 📊 昨日新增 3 篇文档
- 🏛️ 新增知识点：Agent 协作、RAG 优化
- 🌐 行业快讯：AI Agent 2026 趋势
- 💡 建议关注：MCP 协议更新
- 📤 （可选）推送到钉钉群

---

## 📦 核心功能

### 1. 本地知识扫描

- **自动扫描**：按路径或关键词搜索 Markdown / HTML / 代码文件
- **智能过滤**：自动排除 `node_modules`、`.git`、`dist` 等噪音
- **灵活配置**：支持自定义文件类型、扫描深度、最大文件数

### 2. 外网实时检索

内置 4 种检索策略：

| 策略 | 查询模板 | 用途 |
|------|---------|------|
| 技术最新进展 | `{技术名} 2026 最新特性` | 判断技术是否过时 |
| 最佳实践 | `{技术名} best practices 2026` | 补充最佳实践 |
| 行业动态 | `{行业} AI 应用 2026` | 行业趋势洞察 |
| 竞品对比 | `{产品} vs 竞品 2026` | 竞争格局更新 |

### 3. 知识融合升级

- **AI 提炼**：从本地文档提取核心知识点
- **对比分析**：旧知识 vs 新信息
- **升级结论**：给出具体更新建议（API 迁移、工具升级、架构调整）

### 4. 多渠道推送

| 渠道 | 格式 | 状态 |
|------|------|------|
| 钉钉 | Markdown 消息 | ✅ 支持 |
| 飞书 | 交互卡片 | ✅ 支持 |
| 本地 Markdown | 文件 | ✅ 默认 |

---

## ⚙️ 配置说明

### 环境变量（.env）

```bash
# 本地知识库根路径（默认扫描整个用户目录）
KNOWLEDGE_BASE_PATH=~

# 外网检索引擎（可选：openai / bing / google）
SEARCH_ENGINE=bing

# 推送渠道（逗号分隔）
CHANNELS=dingtalk,feishu

# 最大扫描文件数
MAX_SCAN_FILES=500
```

### 扫描规则（config/scan_rules.json）

```json
{
  "include_extensions": [".md", ".txt", ".html", ".py", ".js"],
  "exclude_dirs": ["node_modules", ".git", "dist", "build"],
  "max_depth": 6,
  "max_files": 500
}
```

### 检索策略（config/search_strategies.json）

```json
{
  "tech_latest": "{技术名} 2026 最新特性",
  "best_practices": "{技术名} best practices 2026",
  "industry_trends": "{行业} AI 应用 2026",
  "competitor_analysis": "{产品} vs 竞品 2026"
}
```

---

## 📂 项目结构

```
knowledge-assets-skill/
├── SKILL.md                 # WorkBuddy SKILL 定义
├── README.md               # 本文件
├── _meta.json              # SKILL 元数据
├── clawhub.json            # ClawHub 元数据
├── LICENSE                 # MIT 协议
├── .env.example            # 配置模板
├── scripts/               # 工作流脚本
│   ├── scan_local.py      # 本地扫描
│   ├── web_search.py      # 外网检索
│   ├── merge_knowledge.py # 知识融合
│   ├── push_dingtalk.py   # 钉钉推送
│   └── push_feishu.py     # 飞书推送
├── config/                # 配置文件
│   ├── scan_rules.json
│   ├── search_strategies.json
│   └── push_templates.json
├── dingtalk/               # 钉钉配置（用户自行创建）
│   └── .env.example
└── feishu/                 # 飞书配置（用户自行创建）
    └── .env.example
```

---

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request！

**建议贡献方向**：
- 新增更多外网检索源（Bing、Google、SerpAPI）
- 优化本地扫描性能（并行扫描、增量扫描）
- 新增更多推送渠道（Slack、企业微信、Telegram）
- 改进知识融合算法（引入 RAG、知识图谱）

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 相关项目

- [dingtalk-mcp-skill](https://github.com/chaoliuzhu65-tech/dingtalk-mcp-skill) - 钉钉 MCP 插件
- [lark-feishu-skill](https://github.com/larksuite/openclaw-lark) - 飞书 MCP 插件
- [WorkBuddy](https://workbuddy.ai) - AI 编程助手平台

---

## ⭐ Star History

如果这个工具对你有帮助，请给个 Star ⭐

---

> **让知识不再沉睡，让学习持续增值** 🚀
