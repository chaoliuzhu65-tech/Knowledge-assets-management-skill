#!/usr/bin/env python3
"""
外网检索脚本
使用 WorkBuddy web_search 工具进行实时检索
"""

import json
import os
from typing import List, Dict

def load_strategies(path: str = "config/search_strategies.json") -> Dict:
    """加载检索策略"""
    default_strategies = {
        "tech_latest": "{技术名} 2026 最新特性",
        "best_practices": "{技术名} best practices 2026",
        "industry_trends": "{行业} AI 应用 2026",
        "competitor_analysis": "{产品} vs 竞品 2026"
    }
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            user_strategies = json.load(f)
            default_strategies.update(user_strategies)
    
    return default_strategies

def generate_search_queries(topic: str, strategies: Dict) -> List[str]:
    """根据主题生成检索查询"""
    queries = []
    
    for strategy_name, template in strategies.items():
        if "{技术名}" in template:
            queries.append(template.replace("{技术名}", topic))
        elif "{行业}" in template:
            queries.append(template.replace("{行业}", topic))
        elif "{产品}" in template:
            queries.append(template.replace("{产品}", topic))
        else:
            queries.append(template)
    
    return queries

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 web_search.py <主题> [策略名称]")
        sys.exit(1)
    
    topic = sys.argv[1]
    strategy = sys.argv[2] if len(sys.argv) > 2 else None
    
    strategies = load_strategies()
    
    if strategy and strategy in strategies:
        queries = [strategies[strategy].format(**{"技术名": topic, "行业": topic, "产品": topic})]
    else:
        queries = generate_search_queries(topic, strategies)
    
    print(f"生成检索查询：{len(queries)} 条")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    
    # 输出 JSON 供后续处理
    output = {
        "topic": topic,
        "queries": queries
    }
    
    print("\nJSON 输出：")
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
