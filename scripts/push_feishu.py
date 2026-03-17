#!/usr/bin/env python3
"""
飞书推送脚本
将知识升级报告推送到飞书群
"""

import urllib.request
import json
import os

def load_config():
    """加载飞书配置"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "feishu", ".env"
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

def get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 Tenant Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        return result.get("tenant_access_token", "")

def send_interactive_card(token: str, chat_id: str, card: Dict) -> Dict:
    """发送交互卡片到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = {
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False)
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        })
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"code": -1, "msg": str(e)}

def build_card_from_report(report_content: str) -> Dict:
    """从报告内容构建飞书交互卡片"""
    # 提取标题
    title = "🧠 知识升级报告"
    lines = report_content.split('\n')
    
    # 提取关键信息
    elements = []
    
    # 概况部分
    overview_text = ""
    in_overview = False
    for i, line in enumerate(lines):
        if "📊 盘点概况" in line:
            in_overview = True
            continue
        elif in_overview and line.startswith("## "):
            break
        elif in_overview and line.strip():
            overview_text += line.strip() + " "
    
    if overview_text:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": f"**📊 本次扫描概况**\n{overview_text}"}
        })
        elements.append({"tag": "hr"})
    
    # 本地知识摘要
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "完整报告请查看文件详情。"}
    })
    
    # 添加底部说明
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "note",
        "elements": [{
            "tag": "plain_text",
            "content": "本报告由 knowledge-assets-skill v2.0 自动生成"
        }]
    })
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue"
        },
        "elements": elements
    }
    
    return card

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 push_feishu.py <报告文件>")
        sys.exit(1)
    
    report_file = sys.argv[1]
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    config = load_config()
    
    app_id = config.get('FEISHU_APP_ID')
    app_secret = config.get('FEISHU_APP_SECRET')
    chat_id = config.get('FEISHU_CHAT_ID')
    
    if not all([app_id, app_secret, chat_id]):
        print("错误：未找到完整飞书配置")
        print("请在 feishu/.env 中配置 FEISHU_APP_ID、FEISHU_APP_SECRET、FEISHU_CHAT_ID")
        sys.exit(1)
    
    # 获取 Token
    print("正在获取飞书 Token...")
    token = get_tenant_token(app_id, app_secret)
    
    if not token:
        print("错误：Token 获取失败")
        sys.exit(1)
    
    # 构建卡片
    card = build_card_from_report(report_content)
    
    # 发送
    print("正在发送到飞书...")
    result = send_interactive_card(token, chat_id, card)
    
    print("飞书推送结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get('code') == 0:
        print("✅ 推送成功")
        print(f"消息 ID: {result['data'].get('message_id')}")
    else:
        print(f"❌ 推送失败：{result.get('msg')}")

if __name__ == "__main__":
    main()
