#!/usr/bin/env python3
"""
本地知识扫描脚本
扫描指定目录下的知识文档，提取关键信息
"""

import os
import json
from pathlib import Path
from typing import List, Dict

def load_config(config_path: str = "config/scan_rules.json") -> Dict:
    """加载扫描配置"""
    default_config = {
        "include_extensions": [".md", ".txt", ".html", ".py", ".js"],
        "exclude_dirs": ["node_modules", ".git", "dist", "build", "__pycache__"],
        "max_depth": 6,
        "max_files": 500
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            default_config.update(user_config)
    
    return default_config

def scan_directory(base_path: str, config: Dict) -> List[Dict]:
    """扫描目录，返回文件列表"""
    results = []
    base_path = Path(base_path).expanduser()
    
    def walk_dir(current_path: Path, depth: int):
        if depth > config["max_depth"]:
            return
        
        if len(results) >= config["max_files"]:
            return
        
        try:
            for item in current_path.iterdir():
                if item.name in config["exclude_dirs"]:
                    continue
                
                if item.is_dir():
                    walk_dir(item, depth + 1)
                elif item.is_file() and item.suffix in config["include_extensions"]:
                    results.append({
                        "path": str(item),
                        "name": item.name,
                        "extension": item.suffix,
                        "size": item.stat().st_size,
                        "modified": item.stat().st_mtime
                    })
        except PermissionError:
            pass
    
    walk_dir(base_path, 0)
    return results

def filter_by_keyword(files: List[Dict], keyword: str) -> List[Dict]:
    """按关键词过滤文件"""
    keyword_lower = keyword.lower()
    results = []
    
    for file_info in files:
        try:
            with open(file_info["path"], 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if keyword_lower in content.lower():
                    results.append(file_info)
        except Exception:
            pass
    
    return results

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 scan_local.py <路径> [关键词]")
        sys.exit(1)
    
    base_path = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else None
    
    config = load_config()
    files = scan_directory(base_path, config)
    
    if keyword:
        files = filter_by_keyword(files, keyword)
    
    print(f"扫描结果：共找到 {len(files)} 个文件")
    
    for f in files:
        print(f"  - {f['path']}")
    
    # 输出 JSON 供后续处理
    output = {
        "total": len(files),
        "files": files[:50]  # 限制输出数量
    }
    
    print("\nJSON 输出：")
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
