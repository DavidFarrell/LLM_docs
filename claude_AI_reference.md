# Claude API Reference - Python Developer Guide

**Comprehensive reference for developing with Claude's API using Python**

## Table of Contents

1. [Getting Started](#getting-started)
2. [Models Overview](#models-overview)
3. [Messages API](#messages-api)
4. [Streaming](#streaming)
5. [Rate Limits](#rate-limits)
6. [Error Handling](#error-handling)
7. [API Features](#api-features)
8. [Client SDK](#client-sdk)

---

## Getting Started

### Installation

Install the official Python SDK:

```bash
pip install anthropic
```

**Requirements:** Python 3.8+

### Repository

- GitHub: https://github.com/anthropics/anthropic-sdk-python
- Open-source and actively maintained by Anthropic

### Authentication

Set your API key as an environment variable or pass it directly:

```python
import anthropic

# Option 1: Environment variable (recommended)
# export ANTHROPIC_API_KEY='your-api-key-here'
client = anthropic.Anthropic()

# Option 2: Direct initialization
client = anthropic.Anthropic(api_key="your-api-key-here")
```

### Basic Example

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

---

## Models Overview

### Current Production Models

#### Claude Sonnet 4.5 (Recommended)

**Best for:** Complex agents, coding tasks, and advanced reasoning

- **API ID:** `claude-sonnet-4-5-20250929`
- **Alias:** `claude-sonnet-4-5` (auto-updates to latest)
- **Context Window:** 200K tokens (1M tokens in beta)
- **Max Output:** 64K tokens
- **Pricing:** $3/MTok input, $15/MTok output
- **Knowledge Cutoff:** January 2025
- **Description:** The smartest model for complex agents and coding

#### Claude Haiku 4.5

**Best for:** Fast responses with near-frontier intelligence

- **API ID:** `claude-haiku-4-5-20251001`
- **Alias:** `claude-haiku-4-5`
- **Context Window:** 200K tokens
- **Max Output:** 64K tokens
- **Pricing:** $1/MTok input, $5/MTok output
- **Description:** Fastest model with excellent performance/cost ratio

#### Claude Opus 4.1

**Best for:** Specialized reasoning tasks requiring maximum capability

- **API ID:** `claude-opus-4-1-20250805`
- **Alias:** `claude-opus-4-1`
- **Context Window:** 200K tokens
- **Max Output:** 32K tokens
- **Pricing:** $15/MTok input, $75/MTok output
- **Knowledge Cutoff:** January 2025
- **Description:** Most capable model for specialized reasoning

### Model Capabilities

All current models support:
- Text and image input (vision)
- Extended thinking capability
- Tool use
- Structured outputs
- Multilingual processing
- Priority tier access

### Choosing a Model

- **Sonnet 4.5**: Default choice for most applications
- **Haiku 4.5**: When speed and cost are priorities
- **Opus 4.1**: When maximum reasoning capability is required

---

## Messages API

### Overview

The Messages API is the core interface for interacting with Claude. It processes conversational exchanges and returns Claude's responses.

**Endpoints:**
- Create Message: `POST /v1/messages`
- Count Tokens: `POST /v1/messages/count_tokens`

### Request Format

#### Required Parameters

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",  # Required: model to use
    max_tokens=1024,                      # Required: max response length
    messages=[                            # Required: conversation history
        {"role": "user", "content": "Hello!"}
    ]
)
```

#### Optional Parameters

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],

    # Optional parameters
    system="You are a helpful assistant",  # System prompt
    temperature=0.7,                       # Randomness (0-1)
    top_p=0.9,                            # Nucleus sampling
    top_k=40,                             # Token sampling limit
    stop_sequences=["END"],               # Custom stop sequences
    metadata={                            # Request metadata
        "user_id": "user_123"
    }
)
```

### Parameter Details

**model** (required)
- Specifies which Claude model processes the request
- Use versioned IDs for consistency or aliases for auto-updates

**messages** (required)
- Array of message objects with `role` and `content`
- Roles: `"user"` or `"assistant"`
- Must start with a user message
- Content can be string or array of content blocks

**max_tokens** (required)
- Maximum tokens Claude generates in response
- Does not include input tokens
- Sets hard limit on output length

**system** (optional)
- System prompt defining Claude's behavior
- Provides context, instructions, and personality
- Applied before the conversation begins

**temperature** (optional, 0-1)
- Controls response randomness
- Lower (0.0-0.3): More focused and deterministic
- Higher (0.7-1.0): More creative and varied
- Default: 1.0

### Content Types

#### Text Content

```python
messages=[
    {"role": "user", "content": "What is the capital of France?"}
]
```

#### Multi-Modal Content (Images)

```python
messages=[
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_encoded_image_data
                }
            }
        ]
    }
]
```

#### Multi-Turn Conversations

```python
messages=[
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's the population?"}
]
```

### Response Format

```python
{
    "id": "msg_01XYZ...",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "Hello! How can I help you today?"
        }
    ],
    "model": "claude-sonnet-4-5-20250929",
    "stop_reason": "end_turn",
    "stop_sequence": null,
    "usage": {
        "input_tokens": 10,
        "output_tokens": 25,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0
    }
}
```

#### Response Fields

**id**: Unique message identifier

**content**: Array of content blocks
- Text blocks: `{"type": "text", "text": "..."}`
- Thinking blocks: `{"type": "thinking", "thinking": "...", "signature": "..."}`
- Tool use blocks: `{"type": "tool_use", "id": "...", "name": "...", "input": {...}}`

**stop_reason**: Why generation stopped
- `"end_turn"`: Natural completion
- `"max_tokens"`: Hit max_tokens limit
- `"tool_use"`: Model wants to use a tool
- `"stop_sequence"`: Hit custom stop sequence

**usage**: Token consumption details
- `input_tokens`: New input tokens processed
- `output_tokens`: Tokens generated
- `cache_creation_input_tokens`: Tokens written to cache
- `cache_read_input_tokens`: Tokens read from cache

### Accessing Response Data

```python
# Get the response text
response_text = message.content[0].text

# Access message metadata
message_id = message.id
model_used = message.model
tokens_used = message.usage.input_tokens + message.usage.output_tokens

# Get request ID for support
request_id = message._request_id
```

---

## Streaming

### Overview

Streaming enables real-time response delivery using Server-Sent Events (SSE). Set `stream=True` to receive incremental updates as Claude generates the response.

### Benefits

- Lower perceived latency for users
- Real-time display of long responses
- Ability to process partial results
- Better user experience for chat applications

### Basic Streaming

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Event Flow

Streaming responses follow this sequence:

1. **message_start** - Initial event with empty Message object
2. **content_block_start** - Beginning of a content block
3. **content_block_delta** - Incremental content updates (multiple events)
4. **content_block_stop** - End of current content block
5. **message_delta** - Top-level message changes
6. **message_stop** - Final event completing the stream

### Delta Types

**Text Deltas**
```python
# Text arrives incrementally
{
    "type": "content_block_delta",
    "delta": {
        "type": "text_delta",
        "text": "Hello, "
    }
}
```

**Tool Use Deltas**
```python
# Tool parameters stream as partial JSON
{
    "type": "content_block_delta",
    "delta": {
        "type": "input_json_delta",
        "partial_json": '{"location": "San'
    }
}
```

**Thinking Deltas**
```python
# Extended thinking content streams
{
    "type": "content_block_delta",
    "delta": {
        "type": "thinking_delta",
        "thinking": "Let me analyze..."
    }
}
```

### Advanced Streaming Usage

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    # Access different event types
    for event in stream:
        if event.type == "content_block_start":
            print(f"\n[Block {event.index} started: {event.content_block.type}]")
        elif event.type == "content_block_delta":
            if hasattr(event.delta, 'text'):
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n[Message complete]")

    # Get final message after stream completes
    final_message = stream.get_final_message()
    print(f"\nTotal tokens: {final_message.usage.input_tokens + final_message.usage.output_tokens}")
```

### Error Handling in Streams

```python
import anthropic

client = anthropic.Anthropic()

try:
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
except anthropic.APIStatusError as e:
    print(f"API error: {e.status_code} - {e.message}")
except anthropic.APIConnectionError as e:
    print(f"Connection error: {e}")
```

### Stream Recovery

If streaming interrupts, you can resume by including the partial response:

```python
# First attempt
partial_response = ""
try:
    with client.messages.stream(...) as stream:
        for text in stream.text_stream:
            partial_response += text
except Exception as e:
    print(f"Stream interrupted: {e}")

    # Resume with partial response
    messages = [
        {"role": "user", "content": "Original prompt"},
        {"role": "assistant", "content": partial_response},
        {"role": "user", "content": "Please continue"}
    ]

    with client.messages.stream(messages=messages, ...) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
```

**Note:** Tool use and thinking blocks cannot be partially recovered. Resume from the most recent complete text block.

---

## Rate Limits

### Overview

The Claude API enforces rate limits to ensure fair usage and system stability. Rate limits are measured across three dimensions and vary by organization tier.

### Rate Limit Types

**Requests Per Minute (RPM)**
- Maximum number of API requests in a 60-second window
- Applies to all API calls regardless of token count

**Input Tokens Per Minute (ITPM)**
- Maximum uncached input tokens processed per minute
- Only new tokens count; cached tokens don't consume ITPM

**Output Tokens Per Minute (OTPM)**
- Maximum tokens Claude can generate per minute
- Limits response generation capacity

### Cache-Aware Rate Limiting

A key advantage: **only uncached input tokens count towards ITPM limits**.

**Token Accounting:**
- `cache_read_input_tokens`: Do NOT count toward ITPM ✓
- `cache_creation_input_tokens`: Count toward ITPM ✗
- `input_tokens`: Count toward ITPM ✗

**Example:**
```python
# Usage with caching
{
    "input_tokens": 100,                    # Counts toward ITPM
    "cache_creation_input_tokens": 1000,    # Counts toward ITPM
    "cache_read_input_tokens": 5000,        # Does NOT count toward ITPM ✓
    "output_tokens": 200
}

# Effective ITPM usage: 1,100 tokens (not 6,100)
```

### Response Headers

The API returns rate limit information in response headers:

```python
response = client.messages.create(...)

# Access via underlying HTTP response
# Headers available (check SDK documentation for access method):
# - anthropic-ratelimit-requests-limit
# - anthropic-ratelimit-requests-remaining
# - anthropic-ratelimit-requests-reset
# - anthropic-ratelimit-tokens-limit
# - anthropic-ratelimit-tokens-remaining  (rounded to nearest 1000)
# - anthropic-ratelimit-tokens-reset
# - retry-after  (seconds to wait before retrying)
```

### Rate Limit Algorithm

**Token Bucket System**
- Continuous replenishment rather than fixed intervals
- Capacity regenerates constantly up to maximum limit
- Unused capacity doesn't carry over beyond the limit

### Organization Tiers

Tiers automatically advance based on cumulative credit purchases (excluding tax):

| Tier | Qualifying Spend | Typical Limits |
|------|-----------------|----------------|
| Tier 1 | $5 | Starter limits |
| Tier 2 | $40 | Increased limits |
| Tier 3 | $200 | Higher limits |
| Tier 4 | $400 | Production limits |

**Note:** Specific limits vary by model and tier. Check the Console for your current limits.

### Handling Rate Limits

```python
import time
import anthropic
from anthropic import RateLimitError

client = anthropic.Anthropic()

def make_request_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}]
            )
            return message
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            wait_time = (2 ** attempt) * 1
            print(f"Rate limited. Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

message = make_request_with_retry()
```

### Best Practices

1. **Ramp Traffic Gradually**: Don't suddenly spike to maximum limits
2. **Maintain Consistent Usage**: Avoid sporadic high-volume bursts
3. **Implement Exponential Backoff**: For 429 (rate limit) responses
4. **Use Prompt Caching**: Reduces ITPM consumption significantly
5. **Monitor Headers**: Track remaining capacity proactively
6. **Batch When Possible**: Use Batch API for non-urgent workloads (50% cost reduction)

---

## Error Handling

### HTTP Status Codes

The Claude API uses standard HTTP status codes with specific error types:

| Status | Error Type | Description |
|--------|-----------|-------------|
| 400 | `invalid_request_error` | Format or content issue with request |
| 401 | `authentication_error` | API key missing or invalid |
| 403 | `permission_error` | Insufficient API key permissions |
| 404 | `not_found_error` | Resource not found |
| 413 | `request_too_large` | Request exceeds size limits |
| 429 | `rate_limit_error` | Rate limit exceeded |
| 500 | `api_error` | Internal Anthropic system error |
| 529 | `overloaded_error` | API temporarily overloaded |

### Request Size Limits

| Endpoint | Maximum Size |
|----------|-------------|
| Messages API | 32 MB |
| Token Counting API | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |

Exceeding these limits returns a 413 error from Cloudflare before reaching API servers.

### Error Response Structure

All errors return JSON in this format:

```python
{
    "type": "error",
    "error": {
        "type": "error_type",
        "message": "Human-readable description"
    },
    "request_id": "req_..."
}
```

### Python Error Handling

```python
import anthropic
from anthropic import (
    APIError,
    APIStatusError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    BadRequestError
)

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Check your API key")
except PermissionDeniedError as e:
    print(f"Permission denied: {e}")
    print(f"Your API key lacks required permissions")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print(f"Wait before retrying")
except BadRequestError as e:
    print(f"Invalid request: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Request ID: {e.request_id}")  # Include in support tickets
except APIConnectionError as e:
    print(f"Connection error: {e}")
    print(f"Check your network connection")
except APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
    print(f"Request ID: {e.request_id}")
except APIError as e:
    print(f"Unexpected API error: {e}")

# Access request ID from successful responses
message = client.messages.create(...)
request_id = message._request_id  # Include in support tickets
```

### Common Error Scenarios

**Invalid Request (400)**
```python
# Missing required parameter
try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{"role": "user", "content": "Hello"}]
        # Missing max_tokens!
    )
except BadRequestError as e:
    print(f"Invalid request: {e.message}")
```

**Authentication Error (401)**
```python
# Invalid or missing API key
try:
    client = anthropic.Anthropic(api_key="invalid-key")
    message = client.messages.create(...)
except AuthenticationError as e:
    print("Check your ANTHROPIC_API_KEY environment variable")
```

**Rate Limit Error (429)**
```python
import time

def make_request_with_backoff(max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(...)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)
```

**Request Too Large (413)**
```python
# Request exceeds 32 MB limit
try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": extremely_large_content  # > 32 MB
        }]
    )
except BadRequestError as e:
    print("Request exceeds 32 MB limit")
    print("Consider using the Batch API or Files API")
```

### Best Practices

1. **Always Catch Exceptions**: API calls can fail in production
2. **Include Request IDs**: Essential for support tickets
3. **Implement Retry Logic**: For transient errors (429, 500, 529)
4. **Use Exponential Backoff**: Prevents overwhelming the API
5. **Log Errors Appropriately**: Include context for debugging
6. **Handle Long Requests**: Use streaming or Batch API for >10min requests
7. **Validate Input**: Check input size and format before sending

### Streaming Error Handling

Streaming responses may error after returning 200 OK:

```python
try:
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
except APIStatusError as e:
    print(f"\nStream error: {e.status_code} - {e.message}")
    # Handle partial response
    try:
        partial_message = stream.get_final_message()
        print(f"Partial response received: {partial_message.content}")
    except:
        print("Could not retrieve partial response")
```

---

## API Features

### Core Capabilities

The Claude API provides advanced features for building sophisticated applications:

#### Extended Context

- **200K tokens** standard across all models
- **1M tokens** available in beta for Sonnet 4.5
- Process large documents, codebases, and conversations
- Maintains coherence across entire context window

#### Batch Processing

- Process large volumes asynchronously
- **50% cost reduction** compared to standard API
- Ideal for non-urgent workloads
- Results available within 24 hours

#### Citations

- Detailed references to source material
- Exact sentences and passages cited
- Grounded responses with verifiable sources
- Available on supported models

#### Structured Outputs

- JSON output with schema validation (Sonnet 4.5+)
- Strict tool use for guaranteed formats
- Type-safe responses for applications
- Reduces parsing errors

#### Token Counting

- Determine token count before sending
- Endpoint: `POST /v1/messages/count_tokens`
- Helps manage costs and context limits
- Accurate billing estimation

### Tools & Integration

#### Bash & Code Execution

- Execute shell commands in sandboxed environment
- Run Python code securely
- Process data and perform computations
- Available in Agent SDK

#### Computer Use (Beta)

- Screenshot capture
- Mouse and keyboard control
- Interact with applications
- Experimental feature

#### Web Tools

- Web search for real-time information
- Web fetch to retrieve page content
- Access current data beyond training cutoff
- Useful for research and fact-checking

#### Files API

- Upload PDFs, images, and text files
- Manage document references
- Persistent file storage
- Up to 500 MB per file

#### Memory Tool (Beta)

- Store information across conversations
- Retrieve context from previous interactions
- Build personalized experiences
- Session-based or persistent memory

### Deployment Options

The Claude API is available through multiple platforms:

1. **Direct Claude API**
   - Primary API at api.anthropic.com
   - Full feature support
   - Python SDK maintained by Anthropic

2. **Amazon Bedrock**
   - AWS-hosted Claude models
   - Integration with AWS services
   - Enterprise features and compliance

3. **Google Cloud Vertex AI**
   - GCP-hosted Claude models
   - Integration with Google Cloud services
   - Enterprise support

4. **OpenAI SDK Compatibility**
   - Limited compatibility mode
   - Easier migration from OpenAI
   - Not all features supported

### Beta Features

Access beta features using the `beta` namespace:

```python
# Beta features require special headers
# Check SDK documentation for current beta features

# Example structure (check docs for current API):
client = anthropic.Anthropic()

# Beta features accessed via specific API calls
# with appropriate beta headers
```

---

## Client SDK

### Python SDK Features

The official Python SDK provides:

- **Type Hints**: Full type annotations for IDE support
- **Async Support**: Asyncio-compatible methods
- **Error Handling**: Specific exception types
- **Beta Access**: `beta` namespace for new features
- **Streaming**: Built-in streaming support
- **Retry Logic**: Automatic retries for transient errors

### Installation & Setup

```bash
pip install anthropic
```

```python
import anthropic

# Initialize client
client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

# Or with explicit key
client = anthropic.Anthropic(api_key="your-api-key")
```

### Async Usage

```python
import asyncio
import anthropic

async def main():
    client = anthropic.AsyncAnthropic()

    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )

    print(message.content[0].text)

asyncio.run(main())
```

### Async Streaming

```python
import asyncio
import anthropic

async def main():
    client = anthropic.AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(main())
```

### Configuration Options

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key",
    base_url="https://api.anthropic.com",  # Custom base URL
    timeout=60.0,  # Request timeout in seconds
    max_retries=2,  # Maximum retry attempts
    default_headers={  # Custom headers for all requests
        "X-Custom-Header": "value"
    }
)
```

### Repository & Documentation

- **GitHub**: https://github.com/anthropics/anthropic-sdk-python
- **PyPI**: https://pypi.org/project/anthropic/
- **Documentation**: Comprehensive docs in repository
- **Examples**: Sample code and patterns

### SDK Methods

**Messages**
- `client.messages.create()`: Create a message
- `client.messages.stream()`: Stream a message
- `client.messages.count_tokens()`: Count tokens (when available)

**Beta Namespace**
- Access experimental features
- Requires beta headers
- Check documentation for current beta features

### Best Practices

1. **Use Environment Variables**: Store API keys securely
2. **Enable Type Checking**: Use mypy or similar tools
3. **Handle Errors Properly**: Catch specific exceptions
4. **Use Async for Concurrency**: Better performance for multiple requests
5. **Keep SDK Updated**: `pip install --upgrade anthropic`
6. **Check Release Notes**: Stay informed about changes

---

## Advanced Topics

### Prompt Caching

Reuse large contexts across requests to reduce costs and latency:

- Cache persists for 5 minutes (ephemeral) or 1 hour (with extended TTL)
- 90% cost reduction for cached content
- Cached tokens don't count toward ITPM rate limits
- Minimum 1024 tokens to cache
- Use `cache_control` breakpoints in messages

```python
# Example structure (check current API documentation)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Large system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question about cached context"}]
)
```

### Tool Use

Define tools Claude can invoke:

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
    tool_use = next(block for block in message.content if block.type == "tool_use")
    print(f"Tool: {tool_use.name}")
    print(f"Input: {tool_use.input}")
```

### Vision (Images)

Send images to Claude:

```python
import base64

# Read and encode image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                }
            ]
        }
    ]
)
```

### PDF Support

Process PDF documents:

```python
import base64

# Read PDF file
with open("document.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Summarize this PDF"},
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                }
            ]
        }
    ]
)
```

---

## Additional Resources

### Official Documentation

- **Developer Portal**: https://platform.claude.com/docs
- **API Reference**: https://platform.claude.com/docs/en/api/overview
- **Console**: https://console.anthropic.com

### Python SDK

- **GitHub**: https://github.com/anthropics/anthropic-sdk-python
- **PyPI**: https://pypi.org/project/anthropic/
- **Issues**: https://github.com/anthropics/anthropic-sdk-python/issues

### Support

- **Documentation**: https://platform.claude.com/docs
- **Support Portal**: https://support.anthropic.com
- **Community**: Anthropic Discord and forums

### Other Resources

- **Prompt Library**: Pre-built prompts and examples
- **Use Cases**: Real-world application examples
- **Best Practices**: Prompt engineering guides
- **System Prompts**: Example system prompt templates

---

**Last Updated:** Based on documentation accessed November 2025
**SDK Version:** Check PyPI for latest version
**API Version:** v1
