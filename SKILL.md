---
name: feishu-knowledge-assets
description: |
  飞书知识资产沉淀与经验总结工具集，基于飞书 MCP 插件能力，支持经验快速沉淀、结构化梳理、自动归档和知识复用。

  **当以下情况时使用此 Skill**：
  (1) 需要生成项目经验总结、复盘报告、流程文档
  (2) 需要将群聊讨论、会议记录、项目经验沉淀为可复用的知识资产
  (3) 需要批量处理飞书消息、文档、表格中的内容，提炼结构化知识
  (4) 用户提到"经验小结"、"知识沉淀"、"复盘"、"文档归档"、"知识复用"
  (5) 需要建立组织级的知识库、经验库、最佳实践库
---

# 飞书知识资产沉淀 Skill

基于飞书 MCP 插件能力，实现"讨论 → 提炼 → 结构化 → 归档 → 复用"的全流程知识资产管理，将零散的沟通内容转化为可复用的组织资产。

## 🎯 核心能力矩阵

| 能力模块 | 功能描述 | 适用场景 |
|---------|---------|---------|
| **经验自动提炼** | 从群聊消息、会议记录、项目讨论中自动提取核心经验、决策点、待办事项 | 项目复盘、会议总结、经验沉淀 |
| **结构化梳理** | 将非结构化内容转化为标准化的知识结构，支持多模板适配 | 流程文档、最佳实践、故障手册 |
| **自动归档** | 自动将生成的知识资产归档到指定知识库、文件夹或多维表格 | 知识库建设、资产入库、版本管理 |
| **知识复用** | 支持关键词检索、相似经验匹配、模板复用 | 新项目启动、问题排查、方案参考 |
| **跨源整合** | 整合飞书 IM、文档、表格、日历等多源数据生成统一知识视图 | 跨项目经验汇总、全局知识盘点 |

## 🔧 前置依赖

### 必选权限
- 飞书 IM 消息读取权限（读取群聊/单聊历史消息）
- 飞书文档读写权限（创建/更新/读取云文档）
- 飞书多维表格权限（管理知识资产目录）
- 飞书知识库权限（归档到指定知识空间）

### 推荐配置
1. 预先创建知识资产归档目录（文件夹/知识库）
2. 配置知识资产元数据多维表格（用于索引和检索）
3. 定义组织级知识模板（经验总结、故障复盘、流程规范等）

---

## 🚀 核心工作流

### 工作流 1: 群聊经验快速沉淀
**适用场景**：项目群讨论后快速生成经验总结、决策记录

#### 执行步骤
```mermaid
graph TD
    A[用户触发："总结这个群最近3天的经验"] --> B[调用 feishu_im_user_get_messages 获取历史消息]
    B --> C{是否有话题讨论?}
    C -->|是| D[调用 feishu_im_user_get_thread_messages 展开话题回复]
    C -->|否| E[内容提炼：核心观点、决策、待办、经验教训]
    D --> E
    E --> F[结构化梳理：匹配对应知识模板]
    F --> G[调用 feishu_create_doc 创建经验文档]
    G --> H[调用 feishu_bitable_app_table_record 写入资产索引表]
    H --> I[返回文档链接 + 归档确认]
```

#### 关键参数
| 参数 | 默认值 | 说明 |
|---------|---------|---------|
| 时间范围 | `last_7_days` | 用户未指定时默认获取最近7天消息 |
| 话题展开深度 | 最新10条回复 | 完整讨论需求时获取全部 |
| 模板类型 | 通用经验总结 | 支持指定：项目复盘/故障报告/会议纪要 |

### 工作流 2: 多源知识整合生成
**适用场景**：整合 IM 消息、已有文档、表格数据生成综合知识资产

#### 执行步骤
```mermaid
graph TD
    A[用户需求："整合XX项目的所有资料生成复盘报告"] --> B[调用 feishu_im_user_search_messages 搜索项目相关消息]
    A --> C[调用 feishu_search_doc_wiki 搜索项目相关文档]
    A --> D[调用 feishu_sheet 读取项目数据表格]
    B --> E[内容整合：去重、关联、补全上下文]
    C --> E
    D --> E
    E --> F[结构化梳理：按复盘模板组织内容]
    F --> G[调用 feishu_create_doc 创建综合报告]
    G --> H[关联相关资源：插入文档链接、表格引用]
    H --> I[归档到知识库 + 更新索引]
```

### 工作流 3: 知识资产复用
**适用场景**：新项目启动、问题排查时匹配已有经验

#### 执行步骤
```mermaid
graph TD
    A[用户需求："有没有类似XX问题的处理经验?"] --> B[调用 feishu_bitable_app_table_record 搜索资产索引表]
    B --> C[调用 feishu_search_doc_wiki 全文搜索相关文档]
    C --> D[相似度匹配：返回Top3最相关知识资产]
    D --> E{用户需要参考还是整合?}
    E -->|参考| F[返回文档链接 + 核心摘要]
    E -->|整合| G[调用 feishu_fetch_doc 获取相关文档内容]
    G --> H[整合生成新的方案文档]
    H --> I[返回新文档链接]
```

---

## 📝 知识模板规范

### 内置模板（可扩展）
#### 1. 项目经验总结模板
```markdown
<callout emoji="📋" background-color="light-blue">
# 项目基本信息
- 项目名称：{project_name}
- 项目周期：{start_date} ~ {end_date}
- 项目负责人：{owner}
- 参与人员：{members}
</callout>

## 🎯 项目目标与完成情况
### 原定目标
{original_goals}

### 实际完成情况
{actual_results}

### 差距分析
{gap_analysis}

## ✅ 成功经验
{success_experience}

## ❌ 问题与教训
{lessons_learned}

## 📋 待改进事项
| 改进项 | 负责人 | 截止时间 | 优先级 |
|--------|--------|----------|--------|
| {item1} | {owner1} | {date1} | P0 |
| {item2} | {owner2} | {date2} | P1 |

## 📎 相关资源
- 项目群聊：<chat-card id="{chat_id}"/>
- 项目文档：<mention-doc token="{doc_token}" type="docx"/>
- 相关链接：{links}
```

#### 2. 故障复盘模板
```markdown
<callout emoji="🚨" background-color="light-red">
# 故障基本信息
- 故障编号：{incident_id}
- 发生时间：{start_time}
- 恢复时间：{end_time}
- 故障时长：{duration}
- 影响范围：{impact}
- 故障等级：{level}
</callout>

## 🕒 时间线回顾
{timeline}

## 🔍 根因分析
{root_cause}

## ✅ 处理过程
{resolution_process}

## 📋 改进措施
| 措施 | 负责人 | 截止时间 | 验证标准 |
|------|--------|----------|----------|
| {measure1} | {owner1} | {date1} | {criteria1} |
| {measure2} | {owner2} | {date2} | {criteria2}

## 🎯 经验总结
{summary}
```

#### 3. 最佳实践模板
```markdown
<callout emoji="💡" background-color="light-green">
# 最佳实践：{title}
- 适用场景：{scenario}
- 编写人员：{author}
- 更新时间：{update_time}
- 版本：{version}
</callout>

## 📝 实践说明
{description}

## 🚀 操作步骤
{steps}

## ✅ 预期效果
{expected_result}

## ❌ 常见误区
{pitfalls}

## 📎 参考资料
{references}
```

### 自定义模板扩展
1. 在 `references/templates/` 目录下新增 Markdown 模板文件
2. 在 SKILL.md 中添加模板说明和使用场景
3. 模板中使用 `{变量名}` 作为占位符，自动替换为实际内容

---

## 🏗️ 知识资产索引规范

### 多维表结构（必填）
创建名为「知识资产索引」的多维表格，包含以下字段：

| 字段名 | 字段类型 | 说明 |
|---------|---------|---------|
| 资产ID | 自动编号 | 唯一标识 |
| 资产名称 | 文本 | 文档标题 |
| 资产类型 | 单选 | 经验总结/故障复盘/最佳实践/流程规范/会议纪要 |
| 所属领域 | 单选 | 技术/产品/运营/项目/管理 |
| 关键词 | 多选 | 便于检索的标签 |
| 文档链接 | 超链接 | 飞书文档地址 |
| 创建时间 | 日期 | 自动生成 |
| 创建人 | 人员 | 自动关联 |
| 最后更新时间 | 日期 | 自动更新 |
| 阅读次数 | 数字 | 统计复用次数 |
| 状态 | 单选 | 草稿/已发布/已归档 |

### 索引更新规则
- 新创建知识资产时自动写入索引表
- 文档更新时同步更新索引元数据
- 每月自动清理过期/无效资产索引

---

## ⚙️ 工具调用规范

### 消息读取规范
```json
// 获取群聊历史消息
{
  "name": "feishu_im_user_get_messages",
  "parameters": {
    "chat_id": "{chat_id}",
    "relative_time": "last_7_days",
    "page_size": 50,
    "sort_rule": "create_time_desc"
  }
}

// 展开话题回复
{
  "name": "feishu_im_user_get_thread_messages",
  "parameters": {
    "thread_id": "{thread_id}",
    "page_size": 10,
    "sort_rule": "create_time_desc"
  }
}
```

### 文档创建规范
```json
{
  "name": "feishu_create_doc",
  "parameters": {
    "title": "{document_title}",
    "markdown": "{structured_content}",
    "wiki_space": "{knowledge_space_id}" // 归档到指定知识库
  }
}
```

### 索引写入规范
```json
{
  "name": "feishu_bitable_app_table_record",
  "parameters": {
    "action": "create",
    "app_token": "{bitable_app_token}",
    "table_id": "{index_table_id}",
    "fields": {
      "资产名称": "{title}",
      "资产类型": "{type}",
      "所属领域": "{domain}",
      "关键词": "{keywords}",
      "文档链接": "{doc_url}",
      "创建人": [{ "id": "{user_open_id}" }]
    }
  }
}
```

---

## 🎯 最佳实践

### 1. 内容提炼原则
- **去噪**：过滤闲聊、表情包、重复内容
- **提取**：保留决策、结论、经验、待办、问题
- **关联**：补全上下文，关联相关资源
- **结构化**：按逻辑组织，便于阅读和检索

### 2. 质量把控
- 核心信息不遗漏：时间、人物、决策、原因、结果
- 格式规范：统一使用飞书扩展 Markdown 语法
- 标签准确：关键词选择符合组织检索习惯
- 审核机制：重要知识资产需负责人确认后发布

### 3. 复用优化
- 知识资产命名规范：`[领域] [类型]：标题`（例：`[技术] [故障复盘]：支付系统超时问题处理`）
- 定期盘点：每季度回顾知识资产，更新或归档过时内容
- 复用反馈：建立知识复用反馈机制，持续优化内容质量

---

## 📚 扩展资源
- 模板文件：`references/templates/` 目录下所有模板
- 领域分类：`references/domain_classification.md` 领域标签规范
- 归档路径配置：`references/archive_config.md` 各类型资产归档位置
