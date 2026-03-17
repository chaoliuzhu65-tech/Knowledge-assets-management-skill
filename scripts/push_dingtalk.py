#!/usr/bin/env python3
"""
钉钉推送脚本
将知识升级报告推送到钉钉群
"""

import urllib.request
import json
import os

def load_config():
    """加载钉钉配置"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "dingtalk", ".env"
    )
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value
    
    return config

def send_markdown(webhook_url: str, title: str, content: str) -> Dict:
    """发送 Markdown 消息到钉钉"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": content
        }
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(webhook_url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"})
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}

def format_report_as_markdown(report_md: str) -> str:
    """格式化报告为钉钉 Markdown"""
    # 钉钉 Markdown 支持有限，移除不支持的语法
    lines = report_md.split('\n')
    formatted = []
    
    for line in lines:
        # 移除代码块、表格（钉钉不支持）
        if line.strip().startswith('```') or line.strip().startswith('|'):
            continue
        formatted.append(line)
    
    return '\n'.join(formatted)

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 push_dingtalk.py <报告文件>")
        sys.exit(1)
    
    report_file = sys.argv[1]
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    config = load_config()
    webhook_url = config.get('DINGTALK_WEBHOOK_URL')
    
    if not webhook_url:
        print("错误：未找到 DINGTALK_WEBHOOK_URL 配置")
        print("请在 dingtalk/.env 中配置钉钉机器人 Webhook URL")
        sys.exit(1)
    
    # 提取标题
    title = "🧠 知识升级报告"
    for line in report_content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # 格式化内容
    markdown_content = format_report_as_markdown(report_content)
    
    # 发送
    result = send_markdown(webhook_url, title, markdown_content)
    
    print("钉钉推送结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get('errcode') == 0:
        print("✅ 推送成功")
    else:
        print(f"❌ 推送失败：{result.get('errmsg')}")

if __name__ == "__main__":
    main()
