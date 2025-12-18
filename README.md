# Claude Agent SDK + DeepSeek API 测试项目

这个项目演示如何使用 Claude Agent SDK 与 DeepSeek API 进行对话。

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
uv pip install -r requirements.txt
```

### 2. 运行测试

#### 简单测试（推荐开始）

```bash
python simple_test.py
```

这将测试基本的对话功能，包括：
- 中文自我介绍
- Python 装饰器解释
- 斐波那契数列函数编写

#### 完整对话测试

```bash
python test_chat.py
```

这将测试连续对话功能，包括：
- 多轮对话
- 文件写入操作
- 上下文记忆

## 项目文件说明

### 核心文件

- [`simple_test.py`](simple_test.py) - 简单的 API 测试，适合快速验证
- [`test_chat.py`](test_chat.py) - 完整的对话测试，展示 SDK 的高级功能
- [`config.py`](config.py) - DeepSeek API 配置管理

### 配置文件

- [`litellm_config.yaml`](litellm_config.yaml) - LiteLLM 代理服务器配置
- [`requirements.txt`](requirements.txt) - Python 依赖列表

### 文档

- [`refs/agent_sdk.md`](refs/agent_sdk.md) - Claude Agent SDK 完整文档
- [`refs/deepseek.md`](refs/deepseek.md) - DeepSeek API 调用示例
- [`refs/my_mcp.md`](refs/my_mcp.md) - MCP 服务器配置

## API 配置

项目使用 `.env` 文件管理配置，确保 API 密钥安全：

### 1. 配置环境变量

**方法一：使用 `.env` 文件**

项目已包含 `.env` 文件模板。你可以：

1. 复制模板文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，替换 API 密钥：
   ```bash
   DEEPSEEK_API_KEY=your_actual_api_key_here
   ```

**方法二：直接设置环境变量**

```bash
export DEEPSEEK_API_KEY=your_actual_api_key_here
export DEEPSEEK_MODEL=deepseek-chat
```

### 2. `.env` 文件配置

`.env` 文件包含以下配置：

```bash
# DeepSeek API 配置
DEEPSEEK_API_KEY=sk-76595a859876480cb1de7ed3a7ee9239
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# LiteLLM 配置
LITELLM_MASTER_KEY=sk-1234

# Claude Agent SDK 配置
ANTHROPIC_API_KEY=sk-76595a859876480cb1de7ed3a7ee9239
ANTHROPIC_BASE_URL=https://api.deepseek.com/v1
ANTHROPIC_MODEL=deepseek-chat
```

### 2. 更新 API 密钥

**重要：** 请将 `.env` 文件中的 `DEEPSEEK_API_KEY` 替换为你自己的 API 密钥。

```bash
# 将这行
DEEPSEEK_API_KEY=sk-76595a859876480cb1de7ed3a7ee9239

# 替换为
DEEPSEEK_API_KEY=your_actual_api_key_here
```

### 3. 环境变量加载

[`config.py`](config.py) 使用 `python-dotenv` 自动加载 `.env` 文件：

```python
from dotenv import load_dotenv
load_dotenv()  # 自动加载 .env 文件
```

## 直接测试 DeepSeek API

你也可以使用 curl 直接测试 DeepSeek API：

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-76595a859876480cb1de7ed3a7ee9239" \
  -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "stream": false
      }'
```

## 故障排除

### 常见问题

1. **模块导入错误**
   ```
   ModuleNotFoundError: No module named 'claude_agent_sdk'
   ```
   解决方案：确保运行了 `uv pip install -r requirements.txt`

2. **API 连接错误**
   ```
   Connection failed to Claude Code
   ```
   解决方案：检查网络连接和 API 密钥是否正确

3. **权限错误**
   ```
   Permission denied
   ```
   解决方案：检查 API 密钥权限

### 调试模式

在测试文件中，你可以修改以下参数来调试：

```python
options = ClaudeAgentOptions(
    env=env_config,
    allowed_tools=["Read", "Write"],  # 添加更多工具
    permission_mode="acceptEdits",     # 或 "bypassPermissions"
    stderr=print                      # 显示调试信息
)
```

## 扩展功能

### 添加自定义工具

你可以创建自定义 MCP 工具：

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("calculator", "执行数学计算", {"expression": str})
async def calculator(args):
    try:
        result = eval(args["expression"])
        return {"content": [{"type": "text", "text": f"结果: {result}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"错误: {e}"}]}
```

### 使用不同模型

修改 `config.py` 中的模型配置：

```python
"model": "deepseek-coder"  # 代码专用模型
```

## 相关资源

- [Claude Agent SDK 文档](https://docs.claude.com/agent-sdk)
- [DeepSeek API 文档](https://platform.deepseek.com/)
- [LiteLLM 文档](https://docs.litellm.ai/)

## 许可证

MIT License