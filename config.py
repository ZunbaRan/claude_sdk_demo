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
    return {
            "ANTHROPIC_API_KEY": "2c1aafa6fec3870a1b58ce4110103563.RDKI6qfuATJ7gb2k",
            "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
            "ANTHROPIC_MODEL": "GLM-4.6",
        }

def get_mcp() -> dict:
    # 加载 .mcp.json 文件
    with open(".mcp.json", "r") as f:
        mcp_config = json.load(f)
        return mcp_config