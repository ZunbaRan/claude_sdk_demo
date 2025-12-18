#!/usr/bin/env python3
import json
from config import get_mcp
"""
简单的 DeepSeek API 测试
"""

import asyncio
from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, SystemMessage, TextBlock, ToolResultBlock, ToolUseBlock, UserMessage, query, ClaudeAgentOptions
from config import get_claude_agent_env

async def simple_chat_test():
    """简单聊天测试"""

    print("-" * 40)

    # # 获取配置
    env_config = get_claude_agent_env()

    mcp_config = get_mcp()

    # 测试问题
    test_questions = [
        # "查询一下最近的ai新闻热点。使用 web-search-prime"
        "你查看一下你当前拥有的tools 和 Skills, 分类列出"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 问题 {i}: {question}")
        print("🤖 回答: ", end="", flush=True)

        # if (i == 1):
        #     async with ClaudeSDKClient(options=options) as client:
        #         await client.query(question)
        #         async for message in client.receive_response():
        #             if isinstance(message, AssistantMessage):
        #                 for block in message.content:
        #                     if isinstance(block, TextBlock):
        #                         print(f"Claude: {block.text}")
        # elif (i == 2):
        #         async for message in query(
        #             prompt=question,
        #             options=options
        #         ):
        #             print(message)

        tools_name = list(mcp_config["mcpServers"].keys())

            
        # 把 allowedTools 和 options 合并
        # cwd 根目录全路径, 通过os包获取当前目录
        import os
        query_options = ClaudeAgentOptions(
            cwd=os.getcwd(),
            env=env_config,
            mcp_servers=mcp_config["mcpServers"],
            allowed_tools=["Skill", *tools_name],
            permission_mode="bypassPermissions",
            setting_sources=["user", "project"]
        )

        async with ClaudeSDKClient(options=query_options) as client:
            await client.query(question)
            print(f"query_options.cwd: {query_options.cwd}")
            async for message in client.receive_response():
                # 打印 message

                if isinstance(message, SystemMessage):
                    if message.subtype == "init":
                        # Check MCP server status
                        failed_servers = [
                            s for s in message.data["mcp_servers"]
                            if s["status"] != "connected"
                        ]

                        if failed_servers:
                            print(f"Failed to connect: {failed_servers}") 
                    # print("-" * 40)
                    # print(message.data)
                    # print("-" * 40)
                
                if isinstance(message, ResultMessage) and message.subtype == "error_during_execution":
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
                        if isinstance(block, ToolResultBlock) :
                            print("#" * 40)
                            # 只打印前 100 个字符 content: str | list[dict[str, Any]] | None = None
                            if isinstance(block.content, str):
                                print(f"Tool Result: {block.content[:100]}...")
                            elif isinstance(block.content, list):
                                print(f"Tool Result: {block.content[0]['text'][:100]}...")
                            else:
                                print(f"Tool Result: {block.content}")
                            print("#" * 40)



async def main():
    """主函数"""
    print("=" * 40)

    # 聊天测试
    await simple_chat_test()


if __name__ == "__main__":
    asyncio.run(main())