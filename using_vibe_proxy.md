# VibeProxy Usage Guide

This guide shows exactly how to modify your code to use VibeProxy for each supported AI provider.

## Prerequisites

1. **VibeProxy is running** - Check menu bar icon shows "Running"
2. **You've authenticated** - Click "Connect" in Settings for the service you want to use
3. **Proxy is listening on** `http://localhost:8317`

---

## 1. Claude Code (Anthropic)

### BEFORE - Using Anthropic API directly
```python
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")  # Costs money per token
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(message.content[0].text)
```

### AFTER - Using VibeProxy with Claude Code subscription
```python
import anthropic

client = anthropic.Anthropic(
    base_url="http://localhost:8317",    # VibeProxy (no /v1 for Anthropic!)
    api_key="dummy-not-used"             # Any value works
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(message.content[0].text)
```

### Available Claude Models
- `claude-opus-4-1-20250805` - Most capable
- `claude-sonnet-4-5-20250929` - Fast and intelligent
- `claude-sonnet-4-5-20250929-thinking-4000` - With 4K token thinking
- `claude-sonnet-4-5-20250929-thinking-10000` - With 10K token thinking
- `claude-sonnet-4-5-20250929-thinking-32000` - With 32K token thinking
- `claude-3-7-sonnet-20250219` - Previous generation
- `claude-3-5-haiku-20241022` - Fast and cheap

### cURL Example
```bash
# BEFORE - Direct to Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# AFTER - Through VibeProxy
curl http://localhost:8317/v1/messages \
  -H "x-api-key: dummy" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 2. ChatGPT / Codex (OpenAI)

### BEFORE - Using OpenAI API directly
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Costs money per token
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Write a Python function to sort a list"}
    ]
)

print(response.choices[0].message.content)
```

### AFTER - Using VibeProxy with ChatGPT Plus/Pro subscription
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8317/v1",  # VibeProxy (note the /v1!)
    api_key="dummy-not-used"              # Any value works
)

response = client.chat.completions.create(
    model="gpt-5-codex",  # Use Codex models through your subscription
    messages=[
        {"role": "user", "content": "Write a Python function to sort a list"}
    ]
)

print(response.choices[0].message.content)
```

### Available OpenAI/Codex Models
- `gpt-5-codex` - Best for coding (GPT-5 Codex)
- `gpt-5` - General purpose GPT-5
- `gpt-5-codex-low` - Faster, cheaper Codex variant
- `gpt-5-codex-mini` - Cheapest, fastest Codex
- `gpt-5.1` - Latest GPT-5.1
- `gpt-5.1-codex` - Latest Codex variant
- `gpt-4` - GPT-4
- `gpt-4-turbo` - Faster GPT-4
- `gpt-3.5-turbo` - Fastest, cheapest

### Node.js Example
```javascript
// BEFORE - Direct to OpenAI
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const response = await client.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: 'Hello!' }]
});

console.log(response.choices[0].message.content);

// AFTER - Through VibeProxy
import OpenAI from 'openai';

const client = new OpenAI({
    baseURL: 'http://localhost:8317/v1',
    apiKey: 'dummy-not-used'
});

const response = await client.chat.completions.create({
    model: 'gpt-5-codex',
    messages: [{ role: 'user', content: 'Hello!' }]
});

console.log(response.choices[0].message.content);
```

### cURL Example
```bash
# BEFORE - Direct to OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# AFTER - Through VibeProxy
curl http://localhost:8317/v1/chat/completions \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-codex",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 3. Google Gemini

### BEFORE - Using Google Gemini API directly
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content("Explain neural networks")

print(response.text)
```

### AFTER - Using VibeProxy with Gemini subscription
```python
from openai import OpenAI

# Gemini through VibeProxy uses OpenAI-compatible format
client = OpenAI(
    base_url="http://localhost:8317/v1",
    api_key="dummy-not-used"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash-exp",
    messages=[
        {"role": "user", "content": "Explain neural networks"}
    ]
)

print(response.choices[0].message.content)
```

### Available Gemini Models
- `gemini-2.0-flash-exp` - Latest Gemini 2.0 (experimental)
- `gemini-1.5-pro` - Most capable Gemini 1.5
- `gemini-1.5-flash` - Fast Gemini 1.5

### cURL Example
```bash
# BEFORE - Direct to Google
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Hello!"}]
    }]
  }'

# AFTER - Through VibeProxy (OpenAI format)
curl http://localhost:8317/v1/chat/completions \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 4. Qwen (Alibaba Cloud)

### BEFORE - Using Qwen API directly
```python
import requests
import os

response = requests.post(
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    headers={
        "Authorization": f"Bearer {os.environ.get('QWEN_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": "Hello!"}]}
    }
)

print(response.json())
```

### AFTER - Using VibeProxy with Qwen subscription
```python
from openai import OpenAI

# Qwen through VibeProxy uses OpenAI-compatible format
client = OpenAI(
    base_url="http://localhost:8317/v1",
    api_key="dummy-not-used"
)

response = client.chat.completions.create(
    model="qwen-max",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Available Qwen Models
- `qwen-max` - Most capable
- `qwen-plus` - Balanced performance
- `qwen-turbo` - Fastest

### cURL Example
```bash
# BEFORE - Direct to Qwen
curl https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-max",
    "input": {"messages": [{"role": "user", "content": "Hello!"}]}
  }'

# AFTER - Through VibeProxy (OpenAI format)
curl http://localhost:8317/v1/chat/completions \
  -H "Authorization: Bearer dummy" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-max",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Summary of Changes

### For Anthropic SDK:
```python
# Add these two parameters:
client = anthropic.Anthropic(
    base_url="http://localhost:8317",    # No /v1!
    api_key="dummy-not-used"
)
```

### For OpenAI SDK (works for OpenAI, Gemini, Qwen):
```python
# Add these two parameters:
client = OpenAI(
    base_url="http://localhost:8317/v1",  # With /v1!
    api_key="dummy-not-used"
)
```

### For Requests/cURL:
- Change URL from official API to `http://localhost:8317` or `http://localhost:8317/v1`
- Replace real API key with any dummy value

---

## Troubleshooting

### "Connection refused"
- ✅ Check VibeProxy is running (menu bar icon)
- ✅ Verify status shows "Running (port 8317)"

### "Authentication failed" or "No credentials"
- ✅ Open VibeProxy Settings
- ✅ Click "Connect" for the service you're trying to use
- ✅ Complete browser authentication
- ✅ Wait for green checkmark

### "Model not found"
- ✅ Make sure you're using the correct model name
- ✅ Check you've authenticated for that provider
- ✅ Try `curl http://localhost:8317/v1/models` to see available models

### "Expired credentials"
- ✅ VibeProxy Settings will show "expired" in red
- ✅ Click "Reconnect" to refresh your OAuth tokens

---

## Benefits of Using VibeProxy

### Cost Savings
- **Before:** Pay per token ($0.01-$0.10 per 1K tokens)
- **After:** Use unlimited with your existing subscription

### Convenience
- **Before:** Manage API keys, track usage, worry about billing
- **After:** Just authenticate once, use unlimited

### Use Cases
- Personal projects using your subscriptions
- Prototyping without API costs
- Using AI coding assistants (Factory, Cursor, Cline) with your subscriptions
- Scripts and automation with unlimited usage

---

## Security Notes

✅ **All traffic stays local** - Your computer → localhost:8317 → Official APIs
✅ **OAuth tokens stored locally** in `~/.cli-proxy-api/`
✅ **No third-party servers** - Direct connection to Anthropic/OpenAI/Google/Qwen
✅ **Self-built binary** - You compiled CLIProxyAPI from source for maximum trust

---

Generated for David's VibeProxy setup
Built from CLIProxyAPI v6.3.41 (commit cf9b9be)
