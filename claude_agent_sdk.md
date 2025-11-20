# Claude Agent SDK - Python Developer Guide

**Comprehensive guide for building AI agents with Claude's Agent SDK in Python**

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [Custom Tools](#custom-tools)
7. [Configuration](#configuration)
8. [Best Practices](#best-practices)
9. [Examples & Resources](#examples--resources)

---

## Overview

### What is the Claude Agent SDK?

The Claude Agent SDK is a production-ready framework for building autonomous AI agents powered by Claude. It's built on the same agent infrastructure that powers Claude Code and provides enterprise-grade tools for creating sophisticated AI systems.

### Key Features

#### 🎯 Automatic Context Management
- Intelligent context compaction prevents token exhaustion
- Automatically manages conversation history
- Maintains relevant information across long interactions

#### 🛠️ Rich Tool Ecosystem
- File operations (read, write, edit, search)
- Code execution (Bash, Python)
- Web capabilities (search, fetch)
- Model Context Protocol (MCP) integration
- Custom tool creation

#### 🔒 Advanced Permissions
- Fine-grained tool access control
- User approval workflows
- Security boundaries for agent operations
- Plan mode for reviewing before execution

#### 🚀 Production Features
- Built-in error handling and recovery
- Session management for persistent conversations
- Performance monitoring and usage tracking
- Streaming and partial message support
- Automatic prompt caching optimization

#### ⚡ Performance Optimization
- Automatic prompt caching
- Efficient token usage
- Streaming responses
- Parallel tool execution

### Use Cases

**Coding Agents**
- Diagnose production issues and debug code
- Audit code for security vulnerabilities
- Triage incidents and generate reports
- Enforce code standards and best practices
- Automated code review and refactoring

**Business Agents**
- Review and analyze legal contracts
- Process and analyze financial data
- Handle customer support inquiries
- Create marketing content and copy
- Data analysis and reporting

**Research Agents**
- Gather information from multiple sources
- Analyze documents and extract insights
- Generate summaries and reports
- Fact-checking and verification

**Data Processing Agents**
- ETL pipeline automation
- Data cleaning and transformation
- Report generation
- API integration and orchestration

### Why Use the Agent SDK?

**vs. Direct API Usage:**
- Automatic context management (no manual token counting)
- Built-in tool system with file operations and execution
- Session persistence out of the box
- Production-ready error handling
- Optimized performance with caching

**vs. Building from Scratch:**
- Proven agent architecture from Claude Code
- Battle-tested tool implementations
- Security best practices built-in
- Comprehensive permission system
- Active maintenance and updates

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Anthropic API key

### Installation

```bash
pip install claude-agent-sdk
```

### Authentication

The SDK requires an Anthropic API key. Set it as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or in Python:

```python
import os
os.environ['ANTHROPIC_API_KEY'] = 'your-api-key-here'
```

### Verify Installation

```python
import claude_agent_sdk

print(f"SDK Version: {claude_agent_sdk.__version__}")
```

### Alternative Providers

The SDK supports alternative API providers:

**Amazon Bedrock**
```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    provider="bedrock",
    region="us-west-2"
)
```

**Google Vertex AI**
```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    provider="vertex",
    project_id="your-project-id",
    region="us-central1"
)
```

---

## Core Concepts

### Two Interaction Patterns

The SDK provides two ways to interact with agents:

#### 1. `query()` - Single Interactions

- Creates a new session for each call
- Ideal for one-off tasks
- No conversation history maintained
- Simpler for stateless operations

```python
from claude_agent_sdk import query

async for message in query(
    prompt="What is 2+2?",
    options=options
):
    print(message)
```

#### 2. `ClaudeSDKClient` - Persistent Sessions

- Maintains session across multiple interactions
- Conversation history preserved
- Claude remembers previous context
- Better for multi-turn conversations

```python
from claude_agent_sdk import ClaudeSDKClient

async with ClaudeSDKClient(options=options) as client:
    await client.query("What's the capital of France?")
    # ... later ...
    await client.query("What's the population?")  # Remembers context
```

### Message Types

The SDK returns different message types during execution:

**UserMessage**
- User input to the agent
- `type: "user"`

**AssistantMessage**
- Claude's responses
- Contains text, tool calls, or thinking
- `type: "assistant"`

**ResultMessage**
- Final result with execution summary
- Includes token usage and costs
- `type: "result"`
- Subtypes: `"success"` or `"error"`

**SystemMessage**
- Metadata about execution
- Tool execution status
- Internal agent events
- `type: "system"`

### Permission Modes

Control how the agent executes tools:

**acceptEdits**
- Agent can read files and make edits
- User approval required for destructive operations
- Balanced security and autonomy

**plan**
- Agent creates execution plan first
- User reviews and approves before execution
- Maximum control and visibility

**bypassPermissions**
- Agent executes without asking
- Use only in controlled environments
- Maximum autonomy, minimal oversight

```python
from claude_agent_sdk import ClaudeAgentOptions

# Safe default
options = ClaudeAgentOptions(permission_mode='acceptEdits')

# Review before execution
options = ClaudeAgentOptions(permission_mode='plan')

# Autonomous execution (use with caution)
options = ClaudeAgentOptions(permission_mode='bypassPermissions')
```

---

## Basic Usage

### Quick Start Example

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        permission_mode='acceptEdits',
        cwd="/home/user/project"
    )

    async for message in query(
        prompt="List files in the current directory",
        options=options
    ):
        if message.type == "assistant":
            print(message.content)
        elif message.type == "result":
            print(f"\nCompleted. Tokens used: {message.usage.total_tokens}")

asyncio.run(main())
```

### Single Query Pattern

For one-off tasks without conversation history:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def simple_query():
    options = ClaudeAgentOptions(
        system_prompt="You are a Python expert",
        cwd="/path/to/project"
    )

    result = None
    async for message in query(
        prompt="Create a function to calculate fibonacci numbers",
        options=options
    ):
        if message.type == "assistant":
            # Print assistant responses
            for content in message.content:
                if content.get("type") == "text":
                    print(content["text"])

        elif message.type == "result":
            result = message
            if message.subtype == "success":
                print("✓ Task completed successfully")
            else:
                print(f"✗ Task failed: {message.error}")

    return result

asyncio.run(simple_query())
```

### Persistent Session Pattern

For multi-turn conversations:

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def conversation():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful coding assistant",
        permission_mode='acceptEdits'
    )

    async with ClaudeSDKClient(options=options) as client:
        # First query
        await client.query("Create a file called hello.py with a hello world function")

        async for message in client.receive_response():
            if message.type == "assistant":
                print(message.content)

        # Follow-up query - remembers previous context
        await client.query("Now add a docstring to that function")

        async for message in client.receive_response():
            if message.type == "assistant":
                print(message.content)
            elif message.type == "result":
                print(f"Total tokens: {message.usage.total_tokens}")

asyncio.run(conversation())
```

### Processing Different Message Types

```python
async def handle_messages():
    async for message in query(prompt="Create a test file", options=options):

        if message.type == "user":
            print(f"User: {message.message.content}")

        elif message.type == "assistant":
            for block in message.content:
                if block.get("type") == "text":
                    print(f"Claude: {block['text']}")
                elif block.get("type") == "tool_use":
                    print(f"Using tool: {block['name']}")

        elif message.type == "system":
            print(f"System: {message.content}")

        elif message.type == "result":
            if message.subtype == "success":
                print("✓ Success")
                print(f"  Input tokens: {message.usage.input_tokens}")
                print(f"  Output tokens: {message.usage.output_tokens}")
                print(f"  Total cost: ${message.cost:.4f}")
            else:
                print(f"✗ Error: {message.error}")
```

---

## Advanced Features

### Streaming with Partial Messages

Get real-time updates as Claude generates responses:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def streaming_example():
    options = ClaudeAgentOptions(
        include_partial_messages=True  # Enable streaming
    )

    async for message in query(
        prompt="Write a long story about space exploration",
        options=options
    ):
        if message.type == "assistant":
            # Print each chunk as it arrives
            for block in message.content:
                if block.get("type") == "text":
                    print(block["text"], end="", flush=True)

asyncio.run(streaming_example())
```

### Custom System Prompts

Define agent behavior with system prompts:

```python
from claude_agent_sdk import ClaudeAgentOptions

# Custom behavior
options = ClaudeAgentOptions(
    system_prompt="""You are an expert Python developer specializing in data science.
    When writing code:
    - Use type hints
    - Include docstrings
    - Follow PEP 8 style guide
    - Add error handling
    - Write unit tests when appropriate
    """
)

# Preset prompts
options = ClaudeAgentOptions(
    system_prompt="code-reviewer"  # Use built-in preset
)
```

### Tool Allowlisting

Control which tools the agent can use:

```python
from claude_agent_sdk import ClaudeAgentOptions

# Only allow specific tools
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read",           # Read files
        "Write",          # Write files
        "Glob",           # Search for files
        "Grep",           # Search file contents
    ]
)

# Allow all tools (default)
options = ClaudeAgentOptions(
    allowed_tools=None
)
```

### Working Directory Control

Set the working directory for file operations:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project"  # All file operations relative to this
)

async for message in query(
    prompt="Read the README.md file",
    options=options
):
    print(message)
```

### Max Turns Limiting

Prevent infinite loops by limiting conversation turns:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    max_turns=10  # Stop after 10 back-and-forth exchanges
)

async for message in query(
    prompt="Solve this complex problem",
    options=options
):
    if message.type == "result" and message.subtype == "error":
        if "max_turns" in str(message.error).lower():
            print("Agent reached maximum turns limit")
```

### Interrupting Agent Execution

Stop the agent mid-execution:

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def interruptible_task():
    async with ClaudeSDKClient() as client:
        await client.query("Perform a very long task")

        # Start receiving responses
        response_task = asyncio.create_task(
            process_responses(client)
        )

        # Wait for user interrupt
        await asyncio.sleep(5)

        # Interrupt the agent
        await client.interrupt("User requested cancellation")

        await response_task

async def process_responses(client):
    try:
        async for message in client.receive_response():
            print(message)
    except asyncio.CancelledError:
        print("Task interrupted")
```

### Error Handling

Comprehensive error handling:

```python
from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    AuthenticationError
)

async def robust_query():
    try:
        async for message in query(
            prompt="Create a test file",
            options=options
        ):
            print(message)

    except CLINotFoundError:
        print("Error: Claude Code CLI not found")
        print("Install with: pip install claude-agent-sdk")

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("Check your ANTHROPIC_API_KEY")

    except ProcessError as e:
        print(f"Process failed with exit code: {e.exit_code}")
        print(f"Error output: {e.stderr}")

    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Usage Tracking

Monitor token usage and costs:

```python
async def track_usage():
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0

    async for message in query(prompt="Complex task", options=options):
        if message.type == "result" and message.subtype == "success":
            usage = message.usage

            total_input_tokens += usage.input_tokens
            total_output_tokens += usage.output_tokens
            total_cost += message.cost

            print(f"\nUsage Summary:")
            print(f"  Input tokens:  {usage.input_tokens:,}")
            print(f"  Output tokens: {usage.output_tokens:,}")
            print(f"  Cached reads:  {usage.cache_read_input_tokens:,}")
            print(f"  Total cost:    ${message.cost:.4f}")
```

---

## Custom Tools

### Overview

Custom tools extend the Agent SDK with domain-specific capabilities. Tools are created using the `@tool` decorator and served via Model Context Protocol (MCP) servers.

### Creating a Simple Tool

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(
    name="calculate",
    description="Perform mathematical calculations",
    input_schema={
        "expression": {
            "type": "string",
            "description": "Mathematical expression to evaluate"
        }
    }
)
async def calculate(args):
    """Execute a mathematical calculation."""
    try:
        result = eval(args["expression"])
        return {
            "content": [{
                "type": "text",
                "text": f"Result: {result}"
            }]
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {str(e)}"
            }],
            "isError": True
        }

# Create MCP server with custom tools
math_server = create_sdk_mcp_server(
    name="math-tools",
    tools=[calculate]
)
```

### Using Custom Tools

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def use_custom_tools():
    options = ClaudeAgentOptions(
        mcp_servers={
            "math-tools": math_server
        },
        allowed_tools=[
            "mcp__math-tools__calculate"  # Format: mcp__{server}__{tool}
        ],
        max_turns=5
    )

    async for message in query(
        prompt="What is 25 * 4 + 10?",
        options=options
    ):
        if message.type == "assistant":
            print(message.content)
        elif message.type == "result":
            print(f"Completed in {message.usage.total_tokens} tokens")

asyncio.run(use_custom_tools())
```

### Tool with API Integration

```python
import aiohttp
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(
    name="get_weather",
    description="Get current weather for a location",
    input_schema={
        "latitude": {
            "type": "number",
            "description": "Latitude coordinate"
        },
        "longitude": {
            "type": "number",
            "description": "Longitude coordinate"
        }
    }
)
async def get_weather(args):
    """Fetch weather data from API."""
    lat = args["latitude"]
    lon = args["longitude"]

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m&temperature_unit=fahrenheit"

            async with session.get(url) as response:
                if response.status != 200:
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"API error: {response.status}"
                        }],
                        "isError": True
                    }

                data = await response.json()
                temp = data["current"]["temperature_2m"]

                return {
                    "content": [{
                        "type": "text",
                        "text": f"Current temperature: {temp}°F"
                    }]
                }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Failed to fetch weather: {str(e)}"
            }],
            "isError": True
        }

weather_server = create_sdk_mcp_server(
    name="weather-api",
    tools=[get_weather]
)
```

### Tool with Database Access

```python
import aiosqlite
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(
    name="query_database",
    description="Execute SQL query on the database",
    input_schema={
        "query": {
            "type": "string",
            "description": "SQL query to execute (SELECT only)"
        }
    }
)
async def query_database(args):
    """Execute read-only SQL query."""
    query = args["query"]

    # Security: Only allow SELECT queries
    if not query.strip().upper().startswith("SELECT"):
        return {
            "content": [{
                "type": "text",
                "text": "Error: Only SELECT queries are allowed"
            }],
            "isError": True
        }

    try:
        async with aiosqlite.connect("database.db") as db:
            async with db.execute(query) as cursor:
                rows = await cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Format results
                result_text = f"Columns: {', '.join(columns)}\n\n"
                for row in rows:
                    result_text += f"{row}\n"

                return {
                    "content": [{
                        "type": "text",
                        "text": result_text
                    }]
                }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Database error: {str(e)}"
            }],
            "isError": True
        }

db_server = create_sdk_mcp_server(
    name="database-tools",
    tools=[query_database]
)
```

### Multiple Tools in One Server

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(name="add", description="Add two numbers", input_schema={
    "a": {"type": "number"}, "b": {"type": "number"}
})
async def add(args):
    result = args["a"] + args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}

@tool(name="multiply", description="Multiply two numbers", input_schema={
    "a": {"type": "number"}, "b": {"type": "number"}
})
async def multiply(args):
    result = args["a"] * args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}

@tool(name="power", description="Raise a to the power of b", input_schema={
    "a": {"type": "number"}, "b": {"type": "number"}
})
async def power(args):
    result = args["a"] ** args["b"]
    return {"content": [{"type": "text", "text": str(result)}]}

# Create server with multiple tools
math_server = create_sdk_mcp_server(
    name="math",
    version="1.0.0",
    tools=[add, multiply, power]
)

# Use in agent
options = ClaudeAgentOptions(
    mcp_servers={"math": math_server},
    allowed_tools=[
        "mcp__math__add",
        "mcp__math__multiply",
        "mcp__math__power"
    ]
)
```

### Tool Naming Convention

MCP tools follow this naming pattern:

```
mcp__{server_name}__{tool_name}
```

**Examples:**
- Tool `get_weather` in server `weather-api` → `mcp__weather-api__get_weather`
- Tool `calculate` in server `math-tools` → `mcp__math-tools__calculate`
- Tool `query_db` in server `database` → `mcp__database__query_db`

### Best Practices for Custom Tools

1. **Clear Descriptions**: Help Claude understand when to use the tool
2. **Type Safety**: Use proper input schemas with types and descriptions
3. **Error Handling**: Always catch and return errors gracefully
4. **Security**: Validate inputs, especially for file/database operations
5. **Async Operations**: Use async/await for I/O operations
6. **Timeouts**: Implement timeouts for external API calls
7. **Logging**: Log tool usage for debugging and monitoring

---

## Configuration

### ClaudeAgentOptions

Complete reference for configuration options:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Model selection
    model="claude-sonnet-4-5-20250929",  # or "claude-haiku-4-5", etc.

    # System behavior
    system_prompt="You are a helpful assistant",  # or preset name
    permission_mode='acceptEdits',  # or 'plan', 'bypassPermissions'

    # File operations
    cwd="/path/to/working/directory",  # Working directory for file ops

    # Tool control
    allowed_tools=["Read", "Write", "Bash"],  # None = all tools
    mcp_servers={  # Custom MCP servers
        "server-name": server_instance
    },

    # Execution limits
    max_turns=20,  # Maximum conversation turns

    # Streaming
    include_partial_messages=True,  # Enable streaming

    # API configuration
    api_key="your-api-key",  # Or use environment variable
    base_url="https://api.anthropic.com",  # Custom API endpoint

    # Provider options (for Bedrock/Vertex)
    provider="anthropic",  # or "bedrock", "vertex"
    region="us-west-2",  # AWS region for Bedrock
    project_id="gcp-project",  # GCP project for Vertex

    # Advanced options
    timeout=60.0,  # Request timeout in seconds
    max_retries=3,  # Maximum retry attempts
)
```

### Built-in Tools Reference

The SDK includes these built-in tools:

**File Operations:**
- `Read` - Read file contents
- `Write` - Write/create files
- `Edit` - Edit existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents

**Code Execution:**
- `Bash` - Execute shell commands
- `PythonREPL` - Execute Python code

**Web:**
- `WebSearch` - Search the web
- `WebFetch` - Fetch web page content

**Utilities:**
- `TodoWrite` - Manage task lists
- `Task` - Launch sub-agents

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY='your-api-key'

# Optional
export ANTHROPIC_BASE_URL='https://api.anthropic.com'
export ANTHROPIC_TIMEOUT='60'
export ANTHROPIC_MAX_RETRIES='3'

# For AWS Bedrock
export AWS_REGION='us-west-2'
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'

# For Google Vertex AI
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'
```

---

## Best Practices

### Security

**1. Use Appropriate Permission Modes**
```python
# For production with user data
options = ClaudeAgentOptions(permission_mode='acceptEdits')

# For reviewing before execution
options = ClaudeAgentOptions(permission_mode='plan')

# Only for controlled environments
options = ClaudeAgentOptions(permission_mode='bypassPermissions')
```

**2. Limit Tool Access**
```python
# Only provide necessary tools
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep"]  # Read-only operations
)
```

**3. Validate Custom Tool Inputs**
```python
@tool(name="run_query", ...)
async def run_query(args):
    query = args["query"]

    # Validate before executing
    if not query.strip().upper().startswith("SELECT"):
        return {"content": [{"type": "text", "text": "Only SELECT allowed"}], "isError": True}

    # ... execute query
```

**4. Set Working Directory Boundaries**
```python
options = ClaudeAgentOptions(
    cwd="/safe/sandbox/directory"  # Limit file access scope
)
```

### Performance

**1. Use Streaming for Long Responses**
```python
options = ClaudeAgentOptions(
    include_partial_messages=True  # Enable streaming
)
```

**2. Set Appropriate Max Turns**
```python
# Simple tasks
options = ClaudeAgentOptions(max_turns=5)

# Complex multi-step tasks
options = ClaudeAgentOptions(max_turns=20)
```

**3. Reuse Sessions for Related Tasks**
```python
# Efficient: One session for multiple queries
async with ClaudeSDKClient(options) as client:
    await client.query("Task 1")
    await process_response(client)

    await client.query("Related task 2")
    await process_response(client)
```

**4. Monitor Token Usage**
```python
async for message in query(prompt="...", options=options):
    if message.type == "result":
        if message.usage.total_tokens > 50000:
            print("Warning: High token usage")
```

### Error Handling

**1. Always Handle Errors**
```python
try:
    async for message in query(prompt="...", options=options):
        process_message(message)
except ProcessError as e:
    log_error(f"Process failed: {e.exit_code}")
    handle_failure()
except Exception as e:
    log_error(f"Unexpected error: {e}")
    handle_unexpected_failure()
```

**2. Check Result Status**
```python
async for message in query(prompt="...", options=options):
    if message.type == "result":
        if message.subtype == "success":
            handle_success(message)
        else:
            handle_error(message.error)
```

**3. Implement Retries for Transient Errors**
```python
async def query_with_retry(prompt, options, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = None
            async for message in query(prompt, options):
                if message.type == "result":
                    result = message
            return result
        except (ProcessError, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

### Code Organization

**1. Encapsulate Agent Logic**
```python
class CodeReviewAgent:
    def __init__(self, repo_path: str):
        self.options = ClaudeAgentOptions(
            system_prompt="You are an expert code reviewer",
            permission_mode='acceptEdits',
            cwd=repo_path,
            allowed_tools=["Read", "Grep", "Glob"]
        )

    async def review_file(self, file_path: str) -> str:
        async for message in query(
            prompt=f"Review {file_path} for issues",
            options=self.options
        ):
            if message.type == "result":
                return self.extract_review(message)

agent = CodeReviewAgent("/path/to/repo")
review = await agent.review_file("src/main.py")
```

**2. Create Reusable Tool Libraries**
```python
# tools/math_tools.py
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(...)
async def add(args): ...

@tool(...)
async def multiply(args): ...

def create_math_server():
    return create_sdk_mcp_server("math", tools=[add, multiply])

# main.py
from tools.math_tools import create_math_server

options = ClaudeAgentOptions(
    mcp_servers={"math": create_math_server()}
)
```

**3. Configuration Management**
```python
# config.py
from dataclasses import dataclass
from claude_agent_sdk import ClaudeAgentOptions

@dataclass
class AgentConfig:
    model: str = "claude-sonnet-4-5-20250929"
    max_turns: int = 20
    permission_mode: str = 'acceptEdits'

    def to_options(self, **overrides) -> ClaudeAgentOptions:
        config = {
            "model": self.model,
            "max_turns": self.max_turns,
            "permission_mode": self.permission_mode
        }
        config.update(overrides)
        return ClaudeAgentOptions(**config)

# Usage
config = AgentConfig()
options = config.to_options(cwd="/specific/path")
```

---

## Examples & Resources

### Example: File Processing Agent

```python
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

async def process_markdown_files(directory: str):
    """Process all markdown files in a directory."""

    options = ClaudeAgentOptions(
        system_prompt="""You are a documentation expert.
        Review markdown files for:
        - Grammar and spelling
        - Consistent formatting
        - Broken links
        - Missing sections
        """,
        permission_mode='plan',
        cwd=directory,
        allowed_tools=["Read", "Glob", "Write"]
    )

    # Find all markdown files
    async for message in query(
        prompt="Find all .md files and review each one. Create a summary report.",
        options=options
    ):
        if message.type == "assistant":
            print(message.content)
        elif message.type == "result":
            if message.subtype == "success":
                print(f"✓ Processed successfully")
                print(f"  Tokens: {message.usage.total_tokens}")
                print(f"  Cost: ${message.cost:.4f}")
            else:
                print(f"✗ Error: {message.error}")

asyncio.run(process_markdown_files("/path/to/docs"))
```

### Example: Code Analysis Agent

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def analyze_codebase(repo_path: str):
    """Analyze a codebase for issues."""

    options = ClaudeAgentOptions(
        system_prompt="You are an expert code auditor",
        permission_mode='acceptEdits',
        cwd=repo_path,
        allowed_tools=["Read", "Grep", "Glob", "Bash"],
        max_turns=15
    )

    async with ClaudeSDKClient(options=options) as client:
        # Step 1: Get overview
        await client.query("Analyze the project structure and list all Python files")
        async for message in client.receive_response():
            if message.type == "assistant":
                print(message.content)

        # Step 2: Check for security issues
        await client.query("Search for potential security vulnerabilities")
        async for message in client.receive_response():
            if message.type == "assistant":
                print(message.content)

        # Step 3: Generate report
        await client.query("Create a markdown report with your findings")
        async for message in client.receive_response():
            if message.type == "result":
                print(f"\nAnalysis complete. Cost: ${message.cost:.4f}")

asyncio.run(analyze_codebase("/path/to/repo"))
```

### Example: Data Processing Agent

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server
import pandas as pd

# Custom tool for data access
@tool(
    name="load_csv",
    description="Load CSV file into memory",
    input_schema={"file_path": {"type": "string"}}
)
async def load_csv(args):
    try:
        df = pd.read_csv(args["file_path"])
        summary = f"Loaded {len(df)} rows, {len(df.columns)} columns\n"
        summary += f"Columns: {', '.join(df.columns)}\n"
        summary += f"\n{df.describe()}"

        return {"content": [{"type": "text", "text": summary}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }

async def process_data():
    data_server = create_sdk_mcp_server("data-tools", tools=[load_csv])

    options = ClaudeAgentOptions(
        system_prompt="You are a data analyst",
        mcp_servers={"data-tools": data_server},
        allowed_tools=["mcp__data-tools__load_csv", "Bash"],
        cwd="/path/to/data"
    )

    async for message in query(
        prompt="Load data.csv, analyze it, and create visualizations",
        options=options
    ):
        if message.type == "assistant":
            print(message.content)

asyncio.run(process_data())
```

### Official Resources

**Documentation:**
- Agent SDK Overview: https://platform.claude.com/docs/en/agent-sdk/overview
- Python SDK Reference: https://platform.claude.com/docs/en/agent-sdk/python
- API Documentation: https://platform.claude.com/docs/en/api/overview

**GitHub Repositories:**
- Python SDK: https://github.com/anthropics/anthropic-agent-sdk-python
- Example Projects: Check repository for examples/
- Claude Code: https://github.com/anthropics/claude-code

**Community:**
- Anthropic Discord
- GitHub Discussions
- Support Portal: https://support.anthropic.com

**Related Documentation:**
- Model Context Protocol: https://modelcontextprotocol.io
- Prompt Engineering: https://platform.claude.com/docs/en/prompt-engineering
- Best Practices: https://platform.claude.com/docs/en/about-claude/best-practices

### Example Projects

Look for these in the official repository:

- **File Manager Agent**: Organize and manage files
- **Code Review Bot**: Automated code review
- **Research Assistant**: Web research and summarization
- **Data Analyst**: CSV/Excel analysis and visualization
- **Customer Support**: Ticket triage and response
- **Documentation Generator**: Generate docs from code

### Getting Help

**Issues or Bugs:**
1. Check GitHub Issues for similar problems
2. Create new issue with reproduction steps
3. Include SDK version and error messages

**Feature Requests:**
1. Check existing feature requests
2. Open GitHub Discussion
3. Describe use case and expected behavior

**Questions:**
1. Review documentation thoroughly
2. Check example projects
3. Ask in community forums
4. Contact support for enterprise issues

---

## Appendix

### Changelog & Updates

Check the GitHub repository for:
- Release notes
- Breaking changes
- Migration guides
- Deprecation notices

### Version Compatibility

- Python 3.8+: Full support
- Python 3.7: Not supported
- Async required: All agent operations use async/await

### Performance Benchmarks

Typical performance metrics (vary by task):
- Simple query: ~2-5 seconds
- File operations: ~3-10 seconds
- Code generation: ~5-15 seconds
- Complex multi-step: ~15-60 seconds

Token usage:
- Simple tasks: 500-2,000 tokens
- Medium tasks: 2,000-10,000 tokens
- Complex tasks: 10,000-50,000+ tokens

### Troubleshooting

**Common Issues:**

1. **"CLI Not Found" Error**
   - Ensure claude-agent-sdk is installed
   - Check Python version (3.8+)
   - Verify installation: `pip show claude-agent-sdk`

2. **Authentication Errors**
   - Verify ANTHROPIC_API_KEY is set
   - Check API key is valid
   - Ensure no extra whitespace

3. **Permission Denied**
   - Check file permissions in cwd
   - Verify working directory exists
   - Review permission_mode setting

4. **High Token Usage**
   - Enable streaming for long responses
   - Set appropriate max_turns
   - Use specific prompts to reduce iterations
   - Monitor usage with ResultMessage

5. **Slow Performance**
   - Use Haiku model for faster responses
   - Enable streaming for better UX
   - Reduce allowed_tools list
   - Set lower max_turns

---

**Last Updated:** Based on documentation accessed November 2025
**SDK Version:** Check PyPI for latest version
**Python Support:** 3.8+
