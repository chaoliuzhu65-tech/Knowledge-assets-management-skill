#!/usr/bin/env python3
"""
知识融合脚本
对比本地知识积累与外网检索结果，生成升级报告
"""

import json
from typing import List, Dict

def generate_upgrade_report(
    local_knowledge: List[str],
    external_info: List[Dict],
    topic: str
) -> Dict:
    """生成知识升级报告"""
    
    # 构建对比表
    upgrade_points = []
    
    for local_point in local_knowledge:
        matched = False
        for external in external_info:
            # 简单的关键词匹配（实际应由AI完成）
            if any(keyword in external.get("title", "").lower() or 
                   keyword in external.get("summary", "").lower()
                   for keyword in local_point.lower().split()):
                upgrade_points.append({
                    "old_knowledge": local_point,
                    "new_info": external.get("title", ""),
                    "source": external.get("url", ""),
                    "upgrade_conclusion": "需要更新"
                })
                matched = True
                break
        
        if not matched:
            upgrade_points.append({
                "old_knowledge": local_point,
                "new_info": "未找到最新信息",
                "source": "",
                "upgrade_conclusion": "保持现状"
            })
    
    report = {
        "topic": topic,
        "local_points_count": len(local_knowledge),
        "external_sources_count": len(external_info),
        "upgrade_points": upgrade_points,
        "action_suggestions": generate_suggestions(upgrade_points)
    }
    
    return report

def generate_suggestions(upgrade_points: List[Dict]) -> List[str]:
    """根据升级点生成行动建议"""
    suggestions = []
    
    # 需要更新的升级点
    need_update = [p for p in upgrade_points if "需要更新" in p.get("upgrade_conclusion", "")]
    
    if need_update:
        suggestions.append(f"发现 {len(need_update)} 处需要更新的知识，建议优先处理")
    
    if len(need_update) > 3:
        suggestions.append("需要更新的内容较多，建议分批更新")
    
    # 添加通用建议
    suggestions.extend([
        "定期运行知识升级扫描，保持知识时效性",
        "建立知识库索引，提升检索效率",
        "考虑引入 RAG 技术，增强知识检索能力"
    ])
    
    return suggestions[:5]

def markdown_report(report: Dict) -> str:
    """生成 Markdown 格式报告"""
    md = f"""# [知识升级报告] {report['topic']}

## 📊 盘点概况
- 本地知识点数：{report['local_points_count']}
- 外网检索源数：{report['external_sources_count']}

## 🏛️ 现有知识积累
"""
    
    for i, point in enumerate(report.get("local_knowledge", [])[:8], 1):
        md += f"{i}. {point}\n"
    
    md += "\n## 🌐 外网最新动态\n"
    
    for i, info in enumerate(report.get("external_info", [])[:5], 1):
        md += f"### {i}. {info.get('title', '未知')}\n"
        md += f"- 来源：{info.get('url', '未知')}\n"
        md += f"- 摘要：{info.get('summary', '无')[:100]}...\n\n"
    
    md += "## 🔄 知识升级点\n\n"
    md += "| 旧知识 | 新信息 | 升级结论 |\n"
    md += "|--------|--------|----------|\n"
    
    for point in report["upgrade_points"][:10]:
        md += f"| {point['old_knowledge'][:50]} | {point['new_info'][:50]} | {point['upgrade_conclusion']} |\n"
    
    md += "\n## 💡 行动建议\n\n"
    
    for i, suggestion in enumerate(report.get("action_suggestions", []), 1):
        md += f"{i}. {suggestion}\n"
    
    md += "\n---\n"
    md += "*本报告由 knowledge-assets-skill v2.0 自动生成*\n"
    
    return md

def main():
    import sys
    
    # 示例用法：python3 merge_knowledge.py <local_file> <external_file>
    
    local_file = sys.argv[1] if len(sys.argv) > 1 else "-"
    external_file = sys.argv[2] if len(sys.argv) > 2 else "-"
    
    # 从文件加载或使用示例数据
    if local_file != "-":
        with open(local_file, 'r', encoding='utf-8') as f:
            local_knowledge = json.load(f)
    else:
        local_knowledge = ["使用高德地图 JSAPI v1.4 进行地图渲染", "旧版逆地理编码 API"]
    
    if external_file != "-":
        with open(external_file, 'r', encoding='utf-8') as f:
            external_info = json.load(f)
    else:
        external_info = [
            {
                "title": "高德地图 JSAPI v2.0 正式发布",
                "url": "https://lbs.amap.com",
                "summary": "v2.0 提供了 WebGL 地图和性能优化"
            }
        ]
    
    report = generate_upgrade_report(local_knowledge, external_info, "示例主题")
    md = markdown_report(report)
    
    print(md)
    
    # 同时输出 JSON
    print("\nJSON 输出：")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
