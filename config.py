import json
"""
DeepSeek API 配置文件
从 .env 文件读取配置
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def get_claude_agent_env():
    """返回 Claude Agent SDK 环境变量配置"""
    # 加载 .claude/setting.json/.env属性
    with open(".claude/settings.json", "r") as f:
        setting = json.load(f)
        env = setting["env"]
        return env

def get_mcp() -> dict:
    # 加载 .mcp.json 文件
    with open(".mcp.json", "r") as f:
        mcp_config = json.load(f)
        return mcp_config