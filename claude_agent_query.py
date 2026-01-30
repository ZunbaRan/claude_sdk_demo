#!/usr/bin/env python3
from config import get_claude_agent_env
import json
from anthropic import Anthropic

"""
简单的 DeepSeek API 测试
"""

import asyncio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ResultMessage,
    SandboxSettings,
    SystemMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    create_sdk_mcp_server,
    query,
    ClaudeAgentOptions,
    tool,
)
from config import get_mcp


@tool("knowledge_retrieval", "知识库检索", {"query": str})
async def knowledge_retrieval(query: str) -> list[dict[str, any]]:
    """
    知识库检索
    """
    import aiohttp

    url = "http://43.138.244.5:9501/dify/work/retrieval"
    headers = {"Content-Type": "application/json"}
    query = str(query)

    data = {
        "knowledge_id": "7ef791e6b88911f0b3d60242ac130006",
        "query": query,
        "score_threshold": 0.2,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            print(f"知识库检索请求: {query}")
            print(f"知识库检索响应: {result}")
            return result["result"]


@tool("web_search", "联网检索", {"query": str})
async def knowledge_retrieval(query: str) -> list[dict[str, any]]:
    """
    知识库检索
    """
    import aiohttp

    url = "https://cloud.fadada.com/api/core-crm/outApi/kimiAi"
    headers = {"Content-Type": "application/json"}
    query = str(query)

    data = {
        # "systemContent": system_content,
        "userContent": query,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            print(f"联网检索: {query}")
            print(f"联网检索: {result}")
            return result["result"]


async def claude_agent_query():
    """简单聊天测试"""

    print("-" * 40)

    # # 获取配置
    env_config = get_claude_agent_env()
    mcp_config = get_mcp()

    sandbox_settings: SandboxSettings = {
        "enabled": True,
        "autoAllowBashIfSandboxed": True,
        "excludedCommands": [],
    }

    knowledge_retrieval_server = create_sdk_mcp_server(
        name="knowledge_retrieval",
        version="1.0.0",
        tools=[knowledge_retrieval],  # Pass decorated functions
    )

    # 测试问题
    test_questions = [
        # """
        # 当你需要完成任务的时候，优先查看你拥有的skill能否完成任务。
        # 查询一下最近的ai新闻热点。并且总结并输出为pdf
        # 并且要输出你使用的tool和skill
        # """
        # "查看一下你拥有的mcp servers和对应的tools和 skills"
        '联网查询一下最近一周的ai新闻热点'
        # '使用知识库检索一下FDD的优势信息'
        # "你可以使用bash工具吗"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 问题 {i}: {question}")
        print("🤖 回答: ", end="", flush=True)

        tools_name = list(mcp_config["mcpServers"].keys())

        # 把 allowedTools 和 options 合并
        # cwd 根目录全路径, 通过os包获取当前目录
        import os

        query_options = ClaudeAgentOptions(
            # cwd应该是当前文件所在目录
            system_prompt="你是一个专业的ai助手，你可以使用mcp servers和tools来完成任务。",
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env_config,
            # mcp_servers=[mcp_config["mcpServers"]],
            mcp_servers={"knowledge_retrieval": knowledge_retrieval_server},
            allowed_tools=["Skill"],
            permission_mode="bypassPermissions",
            setting_sources=["project"],
            sandbox=sandbox_settings,
        )

        print(json.dumps(query_options.__dict__, indent=2, default=str))

        async with ClaudeSDKClient(options=query_options) as client:
            await client.query(question)
            print(f"query_options.cwd: {query_options.cwd}")
            async for message in client.receive_response():
                # print(f"-----------------------{message}-----------------------")
                # 打印 message
                if isinstance(message, SystemMessage):
                    if message.subtype == "init":
                        # Check MCP server status
                        failed_servers = [
                            s
                            for s in message.data["mcp_servers"]
                            if s["status"] != "connected"
                        ]

                        if failed_servers:
                            print(f"Failed to connect: {failed_servers}")
                    # print("-" * 40)
                    # print(message.data)
                    # print("-" * 40)

                if (
                    isinstance(message, ResultMessage)
                    and message.subtype == "error_during_execution"
                ):
                    print("Execution failed")
                    print("@" * 40)
                    print(message.result)
                    print("@" * 40)

                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print("*" * 40)
                            print(f"Claude: {block.text}")
                            print("*" * 40)
                        if isinstance(block, ToolUseBlock):
                            print("*" * 40)
                            print(f"Tool Use: {block.name}")
                            print(f"Tool Input: {block.input}")
                            print("*" * 40)

                if isinstance(message, UserMessage):
                    for block in message.content:
                        if isinstance(block, ToolResultBlock):
                            print("#" * 40)
                            # 只打印前 100 个字符 content: str | list[dict[str, Any]] | None = None
                            if isinstance(block.content, str):
                                print(f"Tool Result: {block.content}")
                                # print(f"Tool Result: {block.content[:100]}...")
                            elif isinstance(block.content, list):
                                print(f"Tool Result: {block.content}")
                                # print(f"Tool Result: {block.content[0]['text'][:100]}...")
                            else:
                                print(f"Tool Result: {block.content}")
                            print("#" * 40)


async def main():
    """主函数"""
    print("=" * 40)

    # 聊天测试
    await claude_agent_query()


if __name__ == "__main__":
    asyncio.run(main())
