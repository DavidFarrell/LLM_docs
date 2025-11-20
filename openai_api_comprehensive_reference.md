# OpenAI API Comprehensive Reference Guide

> **For Offline LLM Development Use** - Complete documentation for OpenAI Platform API

## Table of Contents
1. [Overview](#overview)
2. [Authentication & Setup](#authentication--setup)
3. [Models](#models)
4. [Chat Completions](#chat-completions)
5. [Text Generation](#text-generation)
6. [Image Generation](#image-generation)
7. [Audio & Speech](#audio--speech)
8. [Embeddings](#embeddings)
9. [Fine-Tuning](#fine-tuning)
10. [Assistants & Agents](#assistants--agents)
11. [Error Handling](#error-handling)
12. [Best Practices](#best-practices)
13. [Rate Limits & Pricing](#rate-limits--pricing)
14. [Code Examples](#code-examples)

---

## Overview

The OpenAI API provides access to powerful AI models including:
- **Chat models** (GPT-4o, o1 series, GPT-4, GPT-3.5)
- **Image generation** (DALL-E)
- **Speech-to-text** (Whisper)
- **Text-to-speech** (TTS)
- **Embeddings** (text-embedding models)
- **Reasoning models** (o1 series)

### Key Capabilities

- 🤖 **Conversational AI**: Build chatbots and assistants
- 🎨 **Image Generation**: Create images from text descriptions
- 🗣️ **Speech**: Transcribe audio and generate speech
- 📊 **Text Analysis**: Extract information, classify, summarize
- 🔍 **Semantic Search**: Find similar content using embeddings
- 🧠 **Complex Reasoning**: Advanced problem-solving with o1 models

### Base URL

```
https://api.openai.com/v1/
```

---

## Authentication & Setup

### API Keys

1. Create account at https://platform.openai.com/
2. Navigate to API keys section
3. Generate new API key

**⚠️ CRITICAL SECURITY:**
- **NEVER** commit API keys to version control
- **ALWAYS** use environment variables
- **NEVER** expose keys in client-side code
- Rotate keys regularly
- OpenAI scans GitHub and auto-disables leaked keys

### Python Setup

**Installation:**
```bash
pip install openai
```

**Basic Initialization:**
```python
import os
from openai import OpenAI

# ALWAYS use environment variables
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
```

**Alternative with .env file:**
```python
# .env file
OPENAI_API_KEY=sk-...

# Python code
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()  # Automatically uses OPENAI_API_KEY env var
```

### Organization ID (Optional)

For team usage tracking:
```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_ID")
)
```

### Node.js Setup

```bash
npm install openai
```

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});
```

### curl Examples

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Models

### Current Models (2025)

#### Reasoning Models (o1 Series)

**o1** - Advanced reasoning
- Best for: Complex problem-solving, math, science, coding
- Context: 200K tokens
- Output: 100K tokens
- Strengths: Multi-step reasoning, careful analysis
- Use cases: Research, complex algorithms, deep analysis

**o1-mini** - Faster reasoning
- Optimized for STEM tasks
- Lower cost than o1
- Faster responses

#### Chat Models (GPT Series)

**gpt-4o** (Flagship Model - March 2025)
- **Multimodal**: Text, images, audio
- **Built-in image generation** (as of March 2025)
- Context: 128K tokens
- Best balance of capability and cost
- Recommended for most applications

**gpt-4o-mini**
- Cost-effective version
- Good for simpler tasks
- Fast responses

**gpt-4-turbo**
- Previous flagship
- Context: 128K tokens
- Strong performance

**gpt-4**
- Original GPT-4
- Context: 8K or 32K tokens
- Very capable but more expensive

**gpt-3.5-turbo**
- Fast and economical
- Good for simple tasks
- Context: 16K tokens

### Model Selection Guide

```python
# Complex reasoning, math, science
model = "o1"

# Most applications (recommended)
model = "gpt-4o"

# Cost-effective general use
model = "gpt-4o-mini"

# Budget-conscious applications
model = "gpt-3.5-turbo"
```

### Model Capabilities Comparison

| Model | Reasoning | Speed | Cost | Context | Multimodal |
|-------|-----------|-------|------|---------|------------|
| o1 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | 200K | ❌ |
| gpt-4o | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 128K | ✅ |
| gpt-4o-mini | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | 128K | ✅ |
| gpt-3.5-turbo | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | 16K | ❌ |

---

## Chat Completions

### Basic Chat Completion

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
# Output: "The capital of France is Paris."
```

### Message Roles

**system** - Sets behavior and context
```python
{"role": "system", "content": "You are an expert Python programmer."}
```

**user** - User's message
```python
{"role": "user", "content": "How do I read a file in Python?"}
```

**assistant** - AI's previous responses (for conversation history)
```python
{"role": "assistant", "content": "You can use open() to read files."}
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its main features?"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)
```

### Parameters

```python
response = client.chat.completions.create(
    model="gpt-4o",

    messages=[...],

    # Temperature: 0-2 (default: 1)
    # Lower = more focused and deterministic
    # Higher = more random and creative
    temperature=0.7,

    # Max tokens in response
    max_tokens=500,

    # Top-p sampling (alternative to temperature)
    # 0-1, lower = more focused
    top_p=1.0,

    # Frequency penalty: -2 to 2
    # Positive values reduce repetition
    frequency_penalty=0.0,

    # Presence penalty: -2 to 2
    # Positive values encourage new topics
    presence_penalty=0.0,

    # Stop sequences
    stop=["\n\n", "END"],

    # Number of responses to generate
    n=1,

    # User identifier (for abuse monitoring)
    user="user-12345"
)
```

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

### Response Format

```python
# Response object structure
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-4o",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "The capital of France is Paris."
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 13,
        "completion_tokens": 7,
        "total_tokens": 20
    }
}
```

### Function Calling (Tools)

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if model wants to call function
tool_call = response.choices[0].message.tool_calls[0]
if tool_call:
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Call your actual function
    result = get_weather(**arguments)

    # Send result back to model
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "content": json.dumps(result),
        "tool_call_id": tool_call.id
    })

    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
```

### JSON Mode

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract user info as JSON"},
        {"role": "user", "content": "John Doe, 30 years old, lives in NYC"}
    ],
    response_format={"type": "json_object"}
)

# Response will be valid JSON
data = json.loads(response.choices[0].message.content)
```

---

## Text Generation

### Completions (Legacy)

**Note**: Chat completions are recommended over legacy completions.

```python
# Legacy API (not recommended for new projects)
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Write a tagline for an ice cream shop",
    max_tokens=50
)
```

### Text Editing (Deprecated)

The edits endpoint is deprecated. Use chat completions with instructions instead:

```python
# Instead of edits, use chat completions
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Fix grammar and spelling"},
        {"role": "user", "content": "I has went to the store yesterday"}
    ]
)
```

---

## Image Generation

### DALL-E 3 (Recommended)

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city with flying cars at sunset",
    size="1024x1024",  # Options: 1024x1024, 1792x1024, 1024x1792
    quality="standard",  # or "hd"
    n=1  # DALL-E 3 only supports n=1
)

image_url = response.data[0].url
```

### DALL-E 2

```python
response = client.images.generate(
    model="dall-e-2",
    prompt="A white siamese cat",
    size="512x512",  # Options: 256x256, 512x512, 1024x1024
    n=2  # Can generate multiple images
)

for image in response.data:
    print(image.url)
```

### Image Parameters

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    size="1024x1024",

    # Quality: "standard" or "hd"
    quality="hd",

    # Style: "vivid" or "natural"
    style="vivid",

    # Number of images (DALL-E 2 only supports > 1)
    n=1,

    # Response format: "url" or "b64_json"
    response_format="url"
)
```

### Saving Images

```python
import requests
from pathlib import Path

response = client.images.generate(
    model="dall-e-3",
    prompt="A serene landscape",
    size="1024x1024"
)

# Download and save
image_url = response.data[0].url
image_data = requests.get(image_url).content

Path("generated_image.png").write_bytes(image_data)
```

### Image Editing (DALL-E 2 only)

```python
response = client.images.edit(
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="Add a sun in the sky",
    n=1,
    size="1024x1024"
)
```

### Image Variations (DALL-E 2 only)

```python
response = client.images.create_variation(
    image=open("image.png", "rb"),
    n=2,
    size="1024x1024"
)
```

### GPT-4o Built-in Image Generation (2025)

As of March 2025, GPT-4o can generate images directly:

```python
# No separate DALL-E call needed
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Generate an image of a sunset over mountains"}
    ]
)

# Check response for image
```

---

## Audio & Speech

### Whisper (Speech-to-Text)

**Transcription:**
```python
audio_file = open("audio.mp3", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

print(transcription.text)
```

**With Options:**
```python
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="en",  # Optional: specify language (ISO-639-1)
    prompt="Optional context to guide transcription",
    response_format="json",  # Options: json, text, srt, vtt
    temperature=0  # 0-1, lower = more focused
)
```

**Translation (to English):**
```python
translation = client.audio.translations.create(
    model="whisper-1",
    file=open("german_audio.mp3", "rb")
)

print(translation.text)  # Translated to English
```

### Supported Audio Formats

- mp3
- mp4
- mpeg
- mpga
- m4a
- wav
- webm

**File size limit**: 25 MB

### Text-to-Speech (TTS)

```python
response = client.audio.speech.create(
    model="tts-1",  # or "tts-1-hd" for higher quality
    voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
    input="Hello! This is a test of text to speech."
)

# Save to file
response.stream_to_file("speech.mp3")
```

**Voices:**
- **alloy** - Neutral, balanced
- **echo** - Male, clear
- **fable** - British accent
- **onyx** - Deep, authoritative
- **nova** - Female, energetic
- **shimmer** - Warm, friendly

**Streaming TTS:**
```python
from openai import OpenAI

client = OpenAI()

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="Streaming speech synthesis"
) as response:
    response.stream_to_file("output.mp3")
```

### GPT-4o Voice Mode (Real-time)

For real-time voice interactions, use the Realtime API (separate from standard API).

---

## Embeddings

Embeddings convert text into numerical vectors for similarity comparisons.

### Creating Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Your text here"
)

embedding = response.data[0].embedding
# Returns: list of floats (1536 dimensions for ada-002)
```

### Batch Embeddings

```python
texts = [
    "First document",
    "Second document",
    "Third document"
]

response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=texts
)

embeddings = [item.embedding for item in response.data]
```

### Embedding Models

**text-embedding-ada-002** (Recommended)
- Dimensions: 1536
- Best performance/cost ratio
- Use for most applications

**text-embedding-3-small**
- More efficient
- Lower cost
- Good performance

**text-embedding-3-large**
- Highest quality
- More dimensions
- Higher cost

### Similarity Search

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Get embeddings
query_embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input="search query"
).data[0].embedding

document_embeddings = [...]  # Your stored embeddings

# Find most similar
similarities = [
    cosine_similarity(query_embedding, doc_emb)
    for doc_emb in document_embeddings
]

most_similar_idx = np.argmax(similarities)
```

### Use Cases

1. **Semantic Search**: Find relevant documents
2. **Clustering**: Group similar content
3. **Classification**: Categorize text
4. **Recommendation**: Suggest similar items
5. **Anomaly Detection**: Find outliers

### Best Practices

```python
# Store embeddings for reuse
import json

# Create and save
embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input="document text"
).data[0].embedding

with open("embedding.json", "w") as f:
    json.dump(embedding, f)

# Load and use
with open("embedding.json") as f:
    stored_embedding = json.load(f)
```

---

## Fine-Tuning

Fine-tuning customizes models for specific tasks.

### Preparing Training Data

**Format**: JSONL (JSON Lines)

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is 2+2?"}, {"role": "assistant", "content": "4"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of France?"}, {"role": "assistant", "content": "Paris"}]}
```

**Requirements**:
- Minimum 10 examples
- Recommended: 50-100 examples for good results
- More data = better performance

### Upload Training File

```python
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

file_id = file.id
```

### Create Fine-Tuning Job

```python
fine_tune = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo"  # Base model
)

job_id = fine_tune.id
```

### Monitor Progress

```python
# Check status
status = client.fine_tuning.jobs.retrieve(job_id)
print(status.status)  # "running", "succeeded", "failed"

# List all jobs
jobs = client.fine_tuning.jobs.list()

# Cancel job
client.fine_tuning.jobs.cancel(job_id)
```

### Use Fine-Tuned Model

```python
# After job succeeds
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo:org-name:custom-name:id",
    messages=[{"role": "user", "content": "..."}]
)
```

### Fine-Tuning Costs

- Training cost: per token
- Usage cost: higher than base model
- Check pricing page for current rates

---

## Assistants & Agents

### Assistants API

Create AI assistants with tools and file access.

**Creating an Assistant:**
```python
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a helpful math tutor. Explain concepts clearly.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}]
)
```

**Creating a Thread:**
```python
thread = client.beta.threads.create()
```

**Adding Messages:**
```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Solve: x^2 + 5x + 6 = 0"
)
```

**Running the Assistant:**
```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for completion
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    time.sleep(1)

# Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

### Assistant Tools

**Code Interpreter:**
```python
tools=[{"type": "code_interpreter"}]
```

**File Search:**
```python
tools=[{"type": "file_search"}]
```

**Function Calling:**
```python
tools=[{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather",
        "parameters": {...}
    }
}]
```

### Agents SDK (Python)

Build autonomous agents:

```python
# Agents SDK example (conceptual)
from openai import Agent

agent = Agent(
    model="gpt-4o",
    tools=[search_tool, calculator_tool],
    instructions="Help users find information and calculate"
)

result = agent.run("What's 15% of $249.99?")
```

---

## Error Handling

### Common Errors

**AuthenticationError:**
```python
from openai import AuthenticationError

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    print("Invalid API key")
```

**RateLimitError:**
```python
from openai import RateLimitError
import time

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    print("Rate limit exceeded, waiting...")
    time.sleep(60)
```

**APIError:**
```python
from openai import APIError

try:
    response = client.chat.completions.create(...)
except APIError as e:
    print(f"API error: {e}")
```

### Retry Logic with Exponential Backoff

```python
import time
from openai import RateLimitError, APIError

def api_call_with_retry(max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[...]
            )
            return response

        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.random()
            print(f"Rate limited. Waiting {wait_time:.2f}s...")
            time.sleep(wait_time)

        except APIError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.random()
            print(f"API error. Retrying in {wait_time:.2f}s...")
            time.sleep(wait_time)
```

### Timeout Handling

```python
from openai import OpenAI

client = OpenAI(
    timeout=30.0  # 30 second timeout
)

# Or per-request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    timeout=60.0
)
```

---

## Best Practices

### 1. Security

```python
# ✅ GOOD: Use environment variables
import os
api_key = os.environ.get("OPENAI_API_KEY")

# ❌ BAD: Hardcoded keys
# api_key = "sk-..."

# ✅ GOOD: .env file (not committed)
from dotenv import load_dotenv
load_dotenv()

# ❌ BAD: Keys in code or frontend
```

### 2. Cost Optimization

```python
# Use appropriate model
# gpt-4o-mini for simple tasks
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Cheaper
    messages=[...],
    max_tokens=100  # Limit response length
)

# Cache responses when possible
import functools

@functools.lru_cache(maxsize=100)
def get_completion(prompt):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
```

### 3. Prompt Engineering

```python
# ✅ GOOD: Clear, specific instructions
messages = [
    {"role": "system", "content": "You are a Python expert. Provide concise code examples with explanations."},
    {"role": "user", "content": "How do I read a CSV file in Python? Show code and explain."}
]

# ❌ BAD: Vague prompts
messages = [
    {"role": "user", "content": "CSV in Python"}
]

# ✅ GOOD: Provide context and examples
messages = [
    {"role": "system", "content": "Extract email addresses from text. Output as JSON array."},
    {"role": "user", "content": "Contact us at support@example.com or sales@example.com"}
]
```

### 4. Error Handling

```python
# ✅ GOOD: Comprehensive error handling
try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    # Handle auth errors
    log_error("Invalid API key")
except RateLimitError:
    # Handle rate limits
    wait_and_retry()
except APIError as e:
    # Handle API errors
    log_error(f"API error: {e}")
except Exception as e:
    # Catch-all
    log_error(f"Unexpected error: {e}")
```

### 5. Monitoring Usage

```python
# Track token usage
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...]
)

usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Estimate cost
# (Check current pricing on OpenAI website)
```

### 6. Streaming for Better UX

```python
# ✅ GOOD: Stream for real-time responses
def stream_response(prompt):
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Use in web app for progressive display
for text in stream_response("Write a story"):
    print(text, end="", flush=True)
```

### 7. Context Management

```python
# Manage conversation history length
def trim_conversation(messages, max_tokens=4000):
    """Keep conversation within token limit"""
    # Estimate tokens (rough: 1 token ≈ 4 chars)
    while sum(len(m['content']) for m in messages) > max_tokens * 4:
        # Remove oldest user/assistant pair (keep system)
        messages.pop(1)
        if len(messages) > 2:
            messages.pop(1)
    return messages

# Usage
conversation = [
    {"role": "system", "content": "You are helpful"},
    # ... many messages ...
]
conversation = trim_conversation(conversation)
```

### 8. Input Validation

```python
# Validate inputs before API calls
def safe_completion(user_input):
    # Limit input length
    if len(user_input) > 10000:
        raise ValueError("Input too long")

    # Sanitize if needed
    user_input = user_input.strip()

    # Check for empty input
    if not user_input:
        raise ValueError("Empty input")

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}]
    )
```

---

## Rate Limits & Pricing

### Rate Limits

Rate limits vary by:
- **Model tier**: Different models have different limits
- **Usage tier**: Based on your spending history
- **Metric**: RPM (requests per minute), TPM (tokens per minute), RPD (requests per day)

**Checking rate limits:**
- View in dashboard: https://platform.openai.com/account/rate-limits
- Response headers contain limit information

### Handling Rate Limits

```python
import time
from openai import RateLimitError

def call_with_rate_limit_handling(func, *args, **kwargs):
    max_retries = 5
    base_wait = 1

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = base_wait * (2 ** attempt)
            time.sleep(wait)
```

### Pricing Tiers (Conceptual - check current pricing)

**Input vs Output Tokens:**
- Input tokens: Cheaper
- Output tokens: More expensive

**Model Pricing (relative):**
- gpt-3.5-turbo: $ (cheapest)
- gpt-4o-mini: $$
- gpt-4o: $$$
- gpt-4-turbo: $$$$
- o1: $$$$$ (most expensive)

**Cost Optimization:**
1. Use cheaper models when possible
2. Limit max_tokens
3. Cache responses
4. Batch requests when appropriate
5. Use embeddings for search instead of generating answers

### Monitoring Costs

```python
# Track usage in code
class UsageTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_requests = 0

    def track(self, response):
        self.total_tokens += response.usage.total_tokens
        self.total_requests += 1

    def report(self):
        print(f"Requests: {self.total_requests}")
        print(f"Tokens: {self.total_tokens}")
        # Estimate cost based on current pricing

tracker = UsageTracker()

response = client.chat.completions.create(...)
tracker.track(response)
```

---

## Code Examples

### Example 1: Chatbot

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Chatbot:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, user_message):
        # Add user message
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Get response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.7
        )

        # Extract assistant message
        assistant_message = response.choices[0].message.content

        # Add to history
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset(self):
        self.messages = self.messages[:1]  # Keep only system message

# Usage
bot = Chatbot("You are a Python programming assistant.")

print(bot.chat("How do I read a file?"))
print(bot.chat("Can you show an example?"))
print(bot.chat("What about writing to a file?"))
```

### Example 2: Document Q&A with Embeddings

```python
import numpy as np
from openai import OpenAI

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Example documents
documents = [
    "Python is a high-level programming language.",
    "JavaScript is used for web development.",
    "Machine learning uses algorithms to learn from data.",
    "OpenAI provides powerful AI models via API."
]

# Create embeddings for all documents
doc_embeddings = [get_embedding(doc) for doc in documents]

def answer_question(question):
    # Get question embedding
    q_embedding = get_embedding(question)

    # Find most similar document
    similarities = [
        cosine_similarity(q_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]

    best_idx = np.argmax(similarities)
    context = documents[best_idx]

    # Use GPT to generate answer
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer based on the context provided."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )

    return response.choices[0].message.content

# Usage
print(answer_question("What is Python?"))
print(answer_question("Tell me about AI models"))
```

### Example 3: Content Generator

```python
from openai import OpenAI
import json

client = OpenAI()

def generate_blog_post(topic, tone="professional", length="medium"):
    length_guide = {
        "short": "2-3 paragraphs",
        "medium": "4-6 paragraphs",
        "long": "8-10 paragraphs"
    }

    prompt = f"""Write a {tone} blog post about {topic}.
Length: {length_guide[length]}
Include:
- Engaging introduction
- Main points with examples
- Conclusion with call-to-action
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# Usage
post = generate_blog_post(
    "The Future of AI",
    tone="engaging",
    length="medium"
)
print(post)
```

### Example 4: Code Reviewer

```python
from openai import OpenAI

client = OpenAI()

def review_code(code, language="python"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You are an expert {language} code reviewer.
Review the code for:
- Bugs and errors
- Best practices
- Performance issues
- Security concerns
Provide specific, actionable feedback."""},
            {"role": "user", "content": f"Review this code:\n\n{code}"}
        ],
        temperature=0.3  # Lower for more focused analysis
    )

    return response.choices[0].message.content

# Usage
code = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total / len(numbers)
"""

review = review_code(code)
print(review)
```

### Example 5: Structured Data Extraction

```python
from openai import OpenAI
import json

client = OpenAI()

def extract_contact_info(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """Extract contact information and return as JSON.
Include: name, email, phone, company (if mentioned).
Return only valid JSON."""},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Usage
text = """
Hi, I'm John Smith from Acme Corp.
You can reach me at john.smith@acme.com or call (555) 123-4567.
"""

info = extract_contact_info(text)
print(json.dumps(info, indent=2))
```

---

## Additional Resources

### Official Documentation
- **API Reference**: https://platform.openai.com/docs/api-reference
- **Guides**: https://platform.openai.com/docs/guides
- **Examples**: https://platform.openai.com/examples
- **Cookbook**: https://github.com/openai/openai-cookbook

### Best Practice Guides
- Prompt engineering
- Rate limit handling
- Cost optimization
- Safety best practices

### Tools & SDKs
- **Python SDK**: `pip install openai`
- **Node.js SDK**: `npm install openai`
- **REST API**: Direct HTTP requests

### Community
- **Discord**: OpenAI developer community
- **Forum**: https://community.openai.com/
- **GitHub**: Example code and issues

### Stay Updated
- **Changelog**: https://platform.openai.com/docs/changelog
- **Blog**: https://openai.com/blog/
- **Status**: https://status.openai.com/

---

**End of OpenAI API Comprehensive Reference**

*This documentation covers the OpenAI Platform API including authentication, all major endpoints, best practices, and complete examples. Designed for offline LLM use during hackathon development.*
