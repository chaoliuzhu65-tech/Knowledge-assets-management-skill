#!/usr/bin/env python3
"""
经验总结生成脚本
输入：群聊消息列表、模板类型
输出：结构化的 Markdown 内容
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any

class KnowledgeGenerator:
    def __init__(self):
        self.template_dir = "../references/templates/"
    
    def load_template(self, template_type: str) -> str:
        """加载对应类型的模板"""
        template_map = {
            "project": "project_summary.md",
            "incident": "incident_review.md",
            "best_practice": "best_practice.md"
        }
        
        template_file = template_map.get(template_type, "project_summary.md")
        with open(f"{self.template_dir}/{template_file}", "r", encoding="utf-8") as f:
            return f.read()
    
    def extract_key_points(self, messages: List[Dict]) -> Dict:
        """从消息中提取关键信息"""
        key_points = {
            "decisions": [],
            "experiences": [],
            "problems": [],
            "todos": [],
            "participants": set(),
            "keywords": set()
        }
        
        # 决策关键词
        decision_patterns = ["决定", "确定", "共识", "同意", "结论", "最终方案", "决议"]
        # 经验关键词
        experience_patterns = ["经验", "教训", "收获", "学到", "总结", "发现", "建议"]
        # 问题关键词
        problem_patterns = ["问题", "故障", "bug", "报错", "困难", "阻碍", "风险", "挑战"]
        # 待办关键词
        todo_patterns = ["需要", "待办", "后续", "接下来", "计划", "安排", "负责人"]
        
        for msg in messages:
            if msg.get("sender"):
                key_points["participants"].add(msg["sender"])
            
            content = msg.get("content", "")
            if not content:
                continue
            
            # 提取决策
            for pattern in decision_patterns:
                if pattern in content:
                    key_points["decisions"].append({
                        "content": content,
                        "sender": msg.get("sender"),
                        "time": msg.get("create_time")
                    })
                    break
            
            # 提取经验
            for pattern in experience_patterns:
                if pattern in content:
                    key_points["experiences"].append({
                        "content": content,
                        "sender": msg.get("sender")
                    })
                    break
            
            # 提取问题
            for pattern in problem_patterns:
                if pattern in content:
                    key_points["problems"].append({
                        "content": content,
                        "sender": msg.get("sender")
                    })
                    break
            
            # 提取待办
            for pattern in todo_patterns:
                if pattern in content:
                    key_points["todos"].append({
                        "content": content,
                        "sender": msg.get("sender")
                    })
                    break
        
        # 转换为列表
        key_points["participants"] = list(key_points["participants"])
        
        return key_points
    
    def generate_content(self, messages: List[Dict], template_type: str, extra_info: Dict = None) -> str:
        """生成结构化内容"""
        template = self.load_template(template_type)
        key_points = self.extract_key_points(messages)
        
        # 基础信息填充
        data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "members": ", ".join(key_points["participants"])
        }
        
        # 合并额外信息
        if extra_info:
            data.update(extra_info)
        
        # 生成成功经验部分
        success_content = ""
        for exp in key_points["experiences"]:
            success_content += f"- {exp['content']} (by {exp.get('sender', '未知')})\n"
        data["success_experience"] = success_content if success_content else "暂无"
        
        # 生成问题与教训部分
        problem_content = ""
        for prob in key_points["problems"]:
            problem_content += f"- {prob['content']} (by {prob.get('sender', '未知')})\n"
        data["lessons_learned"] = problem_content if problem_content else "暂无"
        
        # 生成待改进事项部分
        todo_content = ""
        for idx, todo in enumerate(key_points["todos"], 1):
            todo_content += f"| 待办{idx} | {todo.get('sender', '待分配')} | 待确认 | P1 | 待确认 |\n"
        data["待改进事项"] = todo_content if todo_content else "| 暂无待改进项 | - | - | - | - |\n"
        
        # 生成决策部分
        decision_content = ""
        for dec in key_points["decisions"]:
            decision_content += f"- {dec['content']} (by {dec.get('sender', '未知')} at {dec.get('time', '未知')})\n"
        data["key_decisions"] = decision_content if decision_content else "暂无"
        
        # 替换模板变量
        for key, value in data.items():
            placeholder = "{" + key + "}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        # 清理未替换的变量
        template = re.sub(r"\{.*?\}", "待补充", template)
        
        return template

if __name__ == "__main__":
    # 测试用例
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generate_summary.py <messages_json_path> <template_type> [extra_info_json]")
        sys.exit(1)
    
    messages_path = sys.argv[1]
    template_type = sys.argv[2]
    extra_info = {}
    
    if len(sys.argv) > 3:
        extra_info = json.loads(sys.argv[3])
    
    with open(messages_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
    
    generator = KnowledgeGenerator()
    content = generator.generate_content(messages, template_type, extra_info)
    print(content)
