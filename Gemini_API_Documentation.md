# Gemini API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Models](#models)
4. [Core Capabilities](#core-capabilities)
5. [Tools & Extensions](#tools--extensions)
6. [Advanced Features](#advanced-features)
7. [Configuration & Optimization](#configuration--optimization)
8. [Best Practices](#best-practices)
9. [Pricing & Limits](#pricing--limits)

---

## Introduction

The Gemini API provides access to Google's most advanced multimodal AI models, capable of understanding and generating text, images, video, audio, and code. Built to be multimodal from the ground up, Gemini unlocks a wide range of capabilities from simple text generation to complex reasoning, vision understanding, and real-time interactions.

### Key Features

- **Multimodal Understanding**: Process text, images, video, audio, and PDFs in a single unified model
- **Long Context**: Support for 1 million+ token context windows
- **Advanced Reasoning**: Built-in thinking capabilities for complex problem solving
- **Function Calling**: Connect to external tools and APIs seamlessly
- **Structured Outputs**: Generate validated JSON conforming to your schemas
- **Real-Time Interaction**: Live API for low-latency voice and video conversations
- **Grounding**: Connect responses to real-time web search and Google Maps data
- **Code Execution**: Generate and run Python code iteratively

---

## Getting Started

### Prerequisites

You need a Gemini API key, which you can obtain for free from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

Using Python 3.9 or later, install the SDK via pip:

```bash
pip install -q -U google-genai
```

### Authentication

The client automatically retrieves your API key from the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, you can pass it explicitly when initializing the client:

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")
```

### Your First Request

Here's a simple implementation to generate text content:

```python
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)
```

### Security Best Practices

- **Never commit API keys to source control** - Avoid checking keys into version control systems like Git
- **Never expose API keys on client-side** - Client-side code can be easily extracted
- Use server-side applications to keep keys confidential
- Consider adding API key restrictions to limit permissions

---

## Models

### Current Generation Models

#### Gemini 3 Pro (Most Advanced)

- **Model code**: `gemini-3-pro-preview`
- **Input types**: Text, Image, Video, Audio, PDF
- **Context window**: 1,048,576 tokens input / 65,536 tokens output
- **Key capabilities**: Multimodal understanding with state-of-the-art reasoning
- **Supports**: Batch API, caching, code execution, file search, function calling, search grounding, structured outputs, thinking, URL context
- **Knowledge cutoff**: January 2025

#### Gemini 2.5 Pro (Advanced Thinking)

- **Model code**: `gemini-2.5-pro`
- **Input types**: Audio, images, video, text, PDF
- **Context window**: 1,048,576 tokens input / 65,536 tokens output
- **Specialization**: Reasoning over complex problems in code, math, and STEM
- **Supports**: Batch API, caching, code execution, file search, function calling, Maps grounding, search grounding, structured outputs, thinking, URL context

#### Gemini 2.5 Flash (Best Price-Performance)

- **Model code**: `gemini-2.5-flash`
- **Input types**: Text, images, video, audio
- **Context window**: 1,048,576 tokens input / 65,536 tokens output
- **Use case**: Large scale processing, low-latency, high volume tasks
- **Supports**: All major features including thinking capability

#### Gemini 2.5 Flash-Lite (Ultra-Fast)

- **Model code**: `gemini-2.5-flash-lite`
- **Input types**: Text, image, video, audio, PDF
- **Context window**: 1,048,576 tokens input / 65,536 tokens output
- **Optimized for**: Cost-efficiency and high throughput

### Version Naming Conventions

Models use four release types:

- **Stable**: Production-ready, consistent versions (e.g., `gemini-2.5-flash`)
- **Preview**: Production-capable with potential rate limits (e.g., `gemini-2.5-flash-preview-09-2025`)
- **Latest**: Hot-swapped alias with 2-week deprecation notice
- **Experimental**: Unstable, feedback-gathering releases with restrictive limits

### Embedding Model

**Primary Model**: `gemini-embedding-001`
- **Input**: Text only
- **Input token limit**: 2,048
- **Output dimensions**: Flexible range from 128-3,072 (recommended: 768, 1536, or 3072)
- **Latest update**: June 2025

### Image Generation Models

**Imagen 4** (Latest - June 2025)
- Model codes: `imagen-4.0-generate-001`, `imagen-4.0-ultra-generate-001`, `imagen-4.0-fast-generate-001`
- Input: Text prompts (480 token limit)
- Output: 1-4 images

**Imagen 3** (February 2025)
- Model code: `imagen-3.0-generate-002`
- Output: Up to 4 images

### Video Generation Model

**Veo 3.1**
- Model code: `veo-3.1-generate-preview`
- Capabilities: High-fidelity 8-second 720p or 1080p videos with natively generated audio
- Features: Text-to-video, image-to-video, reference images, frame interpolation, video extension

---

## Core Capabilities

### Text Generation

#### Basic Text Generation

The simplest way to generate text is with a single prompt:

```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

#### Streaming Responses

Receive incremental response chunks instead of waiting for full completion:

```python
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"]
)

for chunk in response:
    print(chunk.text, end="")
```

#### Multi-Turn Conversations

Create chat sessions that maintain conversation history automatically:

```python
chat = client.chats.create(model="gemini-2.5-flash")

response = chat.send_message("I have 2 dogs in my house.")
print(response.text)

response = chat.send_message("How many paws are in my house?")
print(response.text)
```

#### System Instructions

Guide model behavior using system instructions:

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."
    ),
    contents="Hello there"
)
```

#### Configuration Parameters

Control generation behavior with various parameters:

```python
config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant.",
    temperature=0.1,  # Lower = more deterministic
    max_output_tokens=1000,
    top_p=0.95,
    top_k=40
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt here",
    config=config
)
```

**Important**: When using Gemini 3 models, keep the `temperature` at its default value of 1.0 to avoid unexpected issues.

### Image Understanding

Gemini models are built to be multimodal from the ground up, unlocking a wide range of image processing and computer vision tasks.

#### Passing Images - Inline Local File

Best for files under 20MB total request size:

```python
from google import genai
from google.genai import types

with open('path/to/small-sample.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client()
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg',
        ),
        'Caption this image.'
    ]
)

print(response.text)
```

#### Passing Images - File API Upload

Recommended for larger files or repeated use:

```python
from google import genai

client = genai.Client()
my_file = client.files.upload(file="path/to/sample.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[my_file, "Caption this image."],
)

print(response.text)
```

#### Supported Image Formats

The API accepts these MIME types:
- PNG (`image/png`)
- JPEG (`image/jpeg`)
- WEBP (`image/webp`)
- HEIC (`image/heic`)
- HEIF (`image/heif`)

#### Advanced Vision Capabilities

**Object Detection**: Gemini 2.0+ models detect objects and provide normalized bounding box coordinates (0-1000 scale). Coordinates require rescaling based on actual image dimensions.

**Segmentation**: Starting with Gemini 2.5, the model provides segmentation masks as base64-encoded PNG probability maps within bounding boxes, enabling precise object boundary identification.

#### Key Use Cases

- Image captioning
- Visual question answering
- Image classification
- Object detection and localization
- Semantic segmentation
- Text extraction from images

#### Technical Constraints

- **Maximum images per request**: 3,600 files
- **Token cost**: Images ≤384px on both sides = 258 tokens; larger images tile at 768×768px per tile
- **Total inline request limit**: 20MB including all content

### Video Understanding

#### Generating Videos with Veo 3.1

Veo 3.1 enables creation of high-fidelity, 8-second 720p or 1080p videos featuring stunning realism and natively generated audio.

```python
import time
from google import genai

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A close up of two people staring at a cryptic drawing on a wall"
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("output.mp4")
```

#### Video Capabilities

- **Text-to-video generation** with dialogue and sound effects
- **Image-to-video** conversion using generated or uploaded images as starting frames
- **Reference images** (up to 3) to guide video content while preserving subject appearance
- **Frame interpolation** by specifying both first and last frames
- **Video extension** to lengthen previously generated clips by up to 7 seconds

**Important**: Generated videos persist on servers for 2 days, after which they are removed, requiring prompt local downloads.

### Audio Capabilities

#### Audio Understanding Features

The Gemini API enables several audio analysis capabilities:

- **Description and summarization**: Describe, summarize, or answer questions about audio content
- **Transcription**: Generate text transcripts from audio files
- **Segment analysis**: Analyze specific segments of the audio

#### Input Methods

Two approaches exist for providing audio:

1. **File Upload**: Use the Files API to upload audio before making requests (recommended for files >20 MB)
2. **Inline Data**: Pass audio directly in the request (limited to 20 MB total request size)

#### Supported Audio Formats

The platform accepts: WAV, MP3, AIFF, AAC, OGG Vorbis, and FLAC files.

#### Technical Specifications

- Each second of audio is represented as 32 tokens (one minute = 1,920 tokens)
- Maximum audio length: 9.5 hours per prompt
- Gemini downsamples audio files to a 16 Kbps data resolution
- Multi-channel audio is combined into a single channel
- Non-speech audio (birdsong, sirens) is understood

#### Timestamp References

Users can request specific segments using MM:SS format:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[audio_file, "Provide a transcript of the speech from 02:30 to 03:29."]
)
```

### Document Processing

#### PDF Support Overview

Gemini models can process documents in PDF format, using native vision to understand entire document contexts.

#### Key Capabilities

- Analyze content including text, images, diagrams, charts, and tables
- Extract information into structured output formats
- Summarize documents and answer questions based on visual and textual elements
- Transcribe content while preserving layouts and formatting

#### Size and Scale Limitations

PDF files up to 50MB or 1000 pages are supported. This limit applies to both inline data and Files API uploads.

#### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(
            data=pdf_data,
            mime_type='application/pdf',
        ),
        "Summarize this document"
    ]
)
print(response.text)
```

#### Technical Details

The system supports up to 1,000 document pages, with each page equivalent to 258 tokens. Pages are automatically scaled to preserve aspect ratios while maintaining processing efficiency.

---

## Tools & Extensions

### Function Calling

Function calling enables models to connect with external tools and APIs, acting as a bridge between natural language and real-world actions.

#### Core Process

The function calling workflow involves four steps:

1. **Define Function Declarations** - Describe the function's name, parameters, and purpose in structured format
2. **Call LLM with Declarations** - Send user prompts alongside function definitions; the model determines if calling a function would help
3. **Execute Function Code** - Your application extracts function names and arguments from the model's response and executes them
4. **Generate User-Friendly Response** - Send function results back to the model for incorporation into final answers

#### Function Declaration Structure

Declarations use a subset of OpenAPI schema format:

```python
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees...",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {"type": "array", "items": {"type": "string"}},
            "date": {"type": "string"},
            "time": {"type": "string"},
            "topic": {"type": "string"}
        },
        "required": ["attendees", "date", "time", "topic"]
    }
}
```

#### Advanced Capabilities

**Parallel Function Calling**: Execute multiple independent functions simultaneously in a single model response.

**Compositional Function Calling**: Chain sequential function calls where results from one function inform subsequent calls.

#### Function Calling Modes

- **AUTO** (default) - Model decides between natural language or function calls
- **ANY** - Forces function calls with optional allowed function restrictions
- **NONE** - Prohibits function calling
- **VALIDATED** - Ensures schema adherence for either function calls or text

#### Key Best Practices

- Provide extremely clear and specific descriptions for accurate tool selection
- Use strong typing and enums to minimize errors
- Limit active tool sets to 10-20 for optimal performance
- Employ low temperature settings (e.g., 0) for deterministic results
- Validate function calls with significant consequences before execution
- Implement robust error handling within functions

### Code Execution

The Gemini API provides a code execution tool enabling Python code generation and execution. The model can then learn iteratively from the code execution results until it arrives at a final output.

#### Enabling Code Execution

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the sum of the first 50 prime numbers?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)

print(response.text)
```

#### Code Execution Example

When enabled, the model generates and executes Python code. The response includes three components:

1. **Text**: Model's explanation
2. **Executable Code**: Generated Python code
3. **Code Execution Result**: Output from running the code

#### Key Limitations

- The model can only generate and execute code. It can't return other artifacts like media files
- Only Python execution is supported, though the model can generate code in other languages without executing it

### Google Search Grounding

Grounding with Google Search connects Gemini models to real-time web content, enabling more accurate responses with verifiable sources.

#### Key Benefits

- **Increase accuracy**: Reduce model hallucinations by basing responses on real-world information
- **Access real-time data**: Answer questions about recent events beyond the model's training cutoff
- **Provide citations**: Display sources for claims, building user trust

#### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)
```

#### Response Structure

Grounded responses include `groundingMetadata` with:
- **webSearchQueries**: Search terms the model used
- **groundingChunks**: Web sources (URIs and titles)
- **groundingSupports**: Links between response segments and source chunks
- **searchEntryPoint**: HTML/CSS for rendering search suggestions

#### Pricing

Billing occurs per search query executed—multiple searches within a single API call count as separate billable uses.

### File Search Tool

The File Search tool enables Retrieval Augmented Generation (RAG) through the Gemini API. It imports, chunks, and indexes your data to enable fast retrieval of relevant information based on a user's prompt.

#### How It Works

File Search uses semantic search to find contextually relevant information. Documents are converted into numerical embeddings that capture semantic meaning, then stored in a specialized database.

#### Python Implementation

##### Basic Setup

```python
from google import genai
from google.genai import types
import time

client = genai.Client()

# Create a File Search store
file_search_store = client.file_search_stores.create(
    config={'display_name': 'my-store-name'}
)

# Upload file directly
operation = client.file_search_stores.upload_to_file_search_store(
    file='sample.txt',
    file_search_store_name=file_search_store.name,
    config={'display_name': 'display-file-name'}
)

# Wait for completion
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)
```

##### Querying Documents

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Can you tell me about Robert Graves",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store.name]
                )
            )
        ]
    )
)
print(response.text)
```

#### Key Features

**Metadata Filtering**: Add custom key-value pairs to files for selective searching:

```python
op = client.file_search_stores.import_file(
    file_search_store_name=file_search_store.name,
    file_name=sample_file.name,
    custom_metadata=[
        {"key": "author", "string_value": "Robert Graves"},
        {"key": "year", "numeric_value": 1934}
    ]
)
```

**Chunking Configuration**: Control how documents are split:

```python
operation = client.file_search_stores.upload_to_file_search_store(
    file_search_store_name=file_search_store.name,
    config={
        'chunking_config': {
            'white_space_config': {
                'max_tokens_per_chunk': 200,
                'max_overlap_tokens': 20
            }
        }
    }
)
```

#### Citations

Access citation information through the `grounding_metadata` attribute:

```python
print(response.candidates[0].grounding_metadata)
```

#### Rate Limits & Pricing

- Maximum file size: 100 MB per document
- Storage tiers from 1 GB (free) to 1 TB (Tier 3)
- Indexing: $0.15 per 1M embedding tokens
- Query embeddings: Free
- Retrieved tokens: Charged as context tokens

### URL Context

The URL context tool enables the model to retrieve and process content from web URLs.

#### How to Use

```python
from google import genai
from google.genai.types import Tool, GenerateContentConfig

client = genai.Client()
model_id = "gemini-2.5-flash"

tools = [{"url_context": {}}]

response = client.models.generate_content(
    model=model_id,
    contents="Compare the ingredients and cooking times from the recipes at [URL1] and [URL2]",
    config=GenerateContentConfig(tools=tools)
)
```

Simply embed the URLs directly in your prompt text, and the model will retrieve their content.

#### Supported Content Types

- **Text formats**: HTML, JSON, plain text, XML, CSS, JavaScript, CSV, RTF
- **Images**: PNG, JPEG, BMP, WebP
- **Documents**: PDF files

#### Key Limitations

- Cannot access paywalled content, YouTube videos, Google Workspace files, or video/audio files
- Up to 20 URLs per request
- Maximum content size of 34MB per URL
- Content retrieved from URLs is counted as part of input tokens

### Computer Use

The Gemini 2.5 Computer Use Preview model enables developers to build browser control agents that interact with and automate tasks by analyzing screenshots and executing UI actions.

#### Key Use Cases

- Automating repetitive data entry and form filling on websites
- Performing automated testing of web applications and user flows
- Conducting research across multiple websites for product information and comparisons

#### How It Works

The system operates through a four-step loop:

1. **Send Request**: Include the Computer Use tool in your API request with the user's goal
2. **Receive Response**: The model analyzes screenshots and generates function calls representing UI actions
3. **Execute Actions**: Client-side code translates and executes these actions in the target environment
4. **Capture State**: New screenshots are captured and returned to the model for the next iteration

#### Supported UI Actions

- `click_at` (click at specific coordinates)
- `type_text_at` (text input)
- `scroll_document` (page scrolling)
- `navigate` (URL navigation)
- `drag_and_drop`
- `key_combination` (keyboard shortcuts)

#### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client()
config = genai.types.GenerateContentConfig(
    tools=[types.Tool(computer_use=types.ComputerUse(
        environment=types.Environment.ENVIRONMENT_BROWSER
    ))]
)

response = client.models.generate_content(
    model='gemini-2.5-computer-use-preview-10-2025',
    contents=contents,
    config=config,
)
```

#### Safety Features

The API includes a `safety_decision` system that flags potentially risky actions as `require_confirmation`, requiring explicit user approval before execution.

#### Important Limitations

As a Preview model, it may be prone to errors and security vulnerabilities. Google recommends close supervision for important tasks and advises against use for critical decisions, sensitive data, or irreversible actions.

---

## Advanced Features

### Structured Outputs

The Gemini API enables developers to configure models to generate responses adhering to JSON Schema, ensuring predictable and parsable results with format and type-safety.

#### Key Applications

1. **Data extraction** - Pulling specific information from unstructured content
2. **Structured classification** - Categorizing text into predefined categories
3. **Agentic workflows** - Generating formatted data for calling external tools or APIs

#### Schema Definition in Python

Using Pydantic, developers define object schemas cleanly:

```python
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity with units.")
```

#### Generating Structured Responses

Configuration requires two parameters:

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List ingredients for chocolate chip cookies",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema=Ingredient.model_json_schema()
    )
)
```

#### Supported JSON Schema Features

- **Basic types**: string, number, integer, boolean, object, array, null
- **Descriptive properties**: title, description
- **Type-specific constraints**: enum, format, minimum/maximum, required fields

#### Streaming Support

Structured outputs support streaming, delivering valid partial JSON strings that concatenate into the complete object—improving perceived performance.

### Thinking Mode

Gemini 3 and 2.5 series models feature an internal thinking process that significantly improves their reasoning and multi-step planning abilities for complex tasks like coding, mathematics, and data analysis.

#### How It Works

The model engages in dynamic thinking by default, automatically adjusting reasoning effort based on request complexity. Thinking generates full internal thoughts, then outputs summaries for user insight.

#### When to Use Thinking

- **Simple tasks** (thinking optional): Fact retrieval, classification
- **Medium tasks** (default thinking): Comparisons, analogies, analysis
- **Complex tasks** (maximum thinking): Math problems, coding, detailed planning

2.5 Flash and Pro models have thinking enabled by default to enhance quality, but may increase processing time. You can disable this by setting `thinking_budget=0`.

#### Configuration in Python

##### Enable Thought Summaries

```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Your prompt here",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
    )
)
```

##### Control Thinking Budget (Gemini 2.5)

```python
thinking_config=types.ThinkingConfig(thinking_budget=1024)
# Disable: thinking_budget=0
# Dynamic: thinking_budget=-1
```

##### Set Thinking Level (Gemini 3)

```python
thinking_config=types.ThinkingConfig(thinking_level="low")
# Options: "low" or "high"
```

#### Pricing

Response costs include both output and thinking tokens. Access the token count via `response.usage_metadata.thoughts_token_count`.

### Long Context

The Gemini models support massive context windows of 1 million or more tokens. To put this in perspective, 1 million tokens would look like:
- 50,000 lines of code
- All text messages sent in 5 years
- 8 average-length English novels
- Transcripts of over 200 podcast episodes

#### Key Use Cases

**Text-based applications:**
- Summarizing large document collections
- Question-answering without retrieval augmented generation (RAG)
- Agentic workflows requiring sustained state tracking
- Many-shot in-context learning with hundreds or thousands of examples

**Multimodal applications:**
- Video question-answering and captioning
- Audio transcription, translation, and summarization
- Meeting analysis and real-time processing
- Video content moderation and recommendation systems

#### Best Practices

The model's performance will be better if you put your query/question at the end of the prompt (after all the other context), particularly for lengthy contexts.

#### Cost Optimization

Context caching is the primary optimization strategy. By caching frequently reused content, developers can reduce input costs significantly—approximately 4x less per request compared to standard rates when using Gemini Flash.

### Embeddings

The Gemini API offers text embedding models that convert words, phrases, sentences, and code into numerical representations. These embeddings enable advanced NLP tasks like semantic search, classification, and clustering with context-aware results.

#### Generating Embeddings

```python
from google import genai

client = genai.Client()

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)

print(result.embeddings)
```

For multiple texts:

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "What is the meaning of life?",
        "What is the purpose of existence?",
        "How do I bake a cake?"
    ]
)
```

#### Supported Task Types

| Task Type | Purpose | Applications |
|-----------|---------|--------------|
| SEMANTIC_SIMILARITY | Assess text similarity | Recommendations, duplicate detection |
| CLASSIFICATION | Categorize texts by labels | Sentiment analysis, spam detection |
| CLUSTERING | Group similar texts | Document organization, anomaly detection |
| RETRIEVAL_DOCUMENT | Search documents | Indexing articles and web pages |
| RETRIEVAL_QUERY | General search queries | Custom search systems |
| CODE_RETRIEVAL_QUERY | Find code blocks | Code suggestions |
| QUESTION_ANSWERING | Match questions to answers | Chatbots |
| FACT_VERIFICATION | Verify statements | Automated fact-checking |

#### Controlling Dimensions

Use the `output_dimensionality` parameter to reduce storage needs:

```python
from google.genai import types

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?",
    config=types.EmbedContentConfig(output_dimensionality=768)
)
```

The model employs Matryoshka Representation Learning, preserving quality at lower dimensions.

#### Key Use Cases

- **RAG Systems**: Embeddings enhance the quality of generated text by retrieving and incorporating relevant information
- Information retrieval and semantic search
- Search result reranking
- Anomaly detection
- Text classification
- Document clustering

### Image Generation

Imagen is Google's high-fidelity image generation model that creates realistic images from text prompts. All generated images include a SynthID watermark.

#### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(number_of_images=4)
)

for generated_image in response.generated_images:
    generated_image.image.show()
```

#### Configuration Parameters

- **numberOfImages**: 1-4 images (default: 4)
- **imageSize**: "1K" or "2K" (Standard/Ultra models only; default: "1K")
- **aspectRatio**: "1:1", "3:4", "4:3", "9:16", "16:9" (default: "1:1")
- **personGeneration**: "dont_allow", "allow_adult" (default), or "allow_all"

#### Key Features

- **Language**: English prompts only
- **Text Generation**: Can incorporate up to 25 characters of text within images
- **Photography Styles**: Supports macro, telephoto, wide-angle, and specialized lenses
- **Art Styles**: Capable of rendering illustrations, paintings, sketches, and digital art
- **Quality Modifiers**: Supports "4K", "HDR", "high-quality" descriptors
- **Material/Shape Control**: Can generate objects "made of" specific materials or "in the shape of" specified forms

### Live API

The Live API enables low-latency, real-time voice and video interactions with Gemini. It processes continuous streams of audio, video, or text to deliver immediate spoken responses, creating natural conversational experiences.

#### Key Capabilities

- **Voice Activity Detection** for handling interruptions
- **Tool use and function calling** integration
- **Session management** for long-running conversations
- **Ephemeral tokens** for secure client-side authentication

#### Implementation Approaches

1. **Server-to-server**: Your backend connects via WebSockets, with clients sending data through your server to the API
2. **Client-to-server**: Frontend code connects directly to the API via WebSockets, offering better streaming performance but requiring ephemeral tokens for production security

#### Technical Requirements

- Audio format: 16-bit PCM, 16kHz, mono
- Output audio: 24kHz sample rate
- Libraries: `librosa` and `soundfile` for audio conversion

#### Basic Workflow

1. Load and convert audio to correct format
2. Send via `session.send_realtime_input()` with audio blob
3. Receive responses asynchronously
4. Write output to WAV file

---

## Configuration & Optimization

### Files API

The Files API enables uploading and managing media files for use with Gemini models. It supports audio, images, videos, documents, and other file types for multimodal processing.

#### Upload Operations

```python
myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Describe this audio clip", myfile]
)
```

#### File Management Operations

**Retrieve metadata:**
```python
myfile = client.files.get(name=file_name)
```

**List uploaded files:**
```python
for f in client.files.list():
    print(f.name)
```

**Delete files:**
```python
client.files.delete(name=myfile.name)
```

#### Key Specifications

- **Storage duration**: Files persist for 48 hours after upload
- **Size limits**: Per-file maximum of 2 GB; 20 GB per project
- **Cost**: Available at no cost across all supported regions
- **Use cases**: Required when total request size (including files and prompts) exceeds 20 MB

### Context Caching

The Gemini API provides two caching mechanisms to reduce costs when repeatedly using the same input tokens:

#### Implicit Caching

Automatically enabled on Gemini 2.5 models with no setup required. The system passes on cost savings when requests hit caches, effective as of May 8th, 2025.

#### Explicit Caching

Manually enabled feature offering guaranteed cost savings through deliberate token caching with configurable time-to-live (TTL) settings.

#### Minimum Token Requirements

Different models have varying thresholds for caching:
- Gemini 2.5 Flash: 1,024 tokens
- Gemini 3 Pro Preview: 2,048 tokens
- Gemini 2.5 Pro: 4,096 tokens

#### Creating Cached Content

```python
from google import genai
from google.genai import types

client = genai.Client()

# Upload files
files = [client.files.upload(file=f) for f in file_paths]

# Create cache
cache = client.caches.create(
    model="gemini-2.5-flash",
    config=types.CreateCachedContentConfig(
        contents=files,
        system_instruction="Your system instruction here",
        ttl="3600s"
    )
)

# Use cache in requests
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your query here",
    config=types.GenerateContentConfig(
        cached_content=cache.name
    )
)
```

#### Cost Benefits

Context caching is a paid feature designed to reduce overall operational costs. Cached tokens are billed at a reduced rate compared to regular input tokens.

#### Ideal Use Cases

- Chatbots with extensive system instructions
- Repetitive video file analysis
- Recurring queries against large document sets
- Frequent code repository analysis

### Safety Settings

The Gemini API provides five adjustable safety filter categories:

1. **Harassment** - Negative or harmful comments targeting identity and/or protected attributes
2. **Hate speech** - Content that is rude, disrespectful, or profane
3. **Sexually explicit** - References to sexual acts or lewd content
4. **Dangerous** - Promotes, facilitates, or encourages harmful acts
5. **Civic integrity** - Election-related queries

#### Block Threshold Levels

- **OFF** - Disables the safety filter entirely
- **BLOCK_NONE** - Allows all content regardless of safety probability
- **BLOCK_ONLY_HIGH** - Blocks only high-probability unsafe content
- **BLOCK_MEDIUM_AND_ABOVE** - Blocks medium and high probability issues
- **BLOCK_LOW_AND_ABOVE** - Blocks low, medium, and high probability concerns

#### Python Configuration

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=['Your prompt here'],
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ]
    )
)
```

#### Key Best Practices

- Adjust safety settings only when consistently needed for specific use cases
- Understand that blocking is based on probability rather than severity of harm
- Test thoroughly to balance protecting users while supporting legitimate applications
- Applications that use less restrictive safety settings may be subject to review
- Built-in protections against child safety threats cannot be adjusted

### Token Counting

#### Basic Token Information

For Gemini models, a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words.

#### Counting Tokens

```python
from google import genai

client = genai.Client()

total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash",
    contents="Your text here"
)
```

You can also extract token counts from API responses through the `usage_metadata` field:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt"
)

print(response.usage_metadata.prompt_token_count)
print(response.usage_metadata.candidates_token_count)
print(response.usage_metadata.total_token_count)
```

#### Multimodal Token Calculation

- **Images**: Images with both dimensions ≤384 pixels = 258 tokens; larger images are tiled at 768x768 pixels, each tile = 258 tokens
- **Video**: 263 tokens per second
- **Audio**: 32 tokens per second

---

## Best Practices

### Prompt Engineering

#### Core Principles

An effective and efficient way to customize model behavior is to provide it with clear and specific instructions. This includes question-based, task-based, or entity-based inputs depending on your needs.

#### Few-Shot vs. Zero-Shot Learning

The guide emphasizes that examples dramatically improve results. We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective. Few-shot prompts show the model desired patterns through 2-5 concrete examples.

#### Positive Pattern Examples

Rather than showing what to avoid, demonstrate correct behavior. Use consistent formatting across examples to avoid confusing the model about expected output structure.

#### Contextual Information

Adding relevant context helps the model understand constraints. Include troubleshooting guides, reference materials, or domain-specific information the model needs.

#### Output Prefixes

Use markers like "JSON:" or "The answer is:" to signal expected response formats, making outputs easier to parse.

#### Prompt Composition

Break complex tasks into sequential components. Chain simpler prompts together, or aggregate parallel operations on different data portions.

#### Parameter Optimization

Control response behavior through:
- **Temperature**: Randomness in token selection (0 = deterministic; note: keep Gemini 3 at default 1.0)
- **Max tokens**: Response length limits
- **Top-K/Top-P**: Token selection filtering

#### Iteration Tips

Try rephrasing, switching to analogous tasks, or reordering prompt components when results disappoint.

### File Management Best Practices

- Position single images before text prompts
- Provide specific instructions rather than generic requests
- Use few-shot examples to guide output format
- Break complex tasks into step-by-step instructions
- Request explanations of model reasoning

---

## Pricing & Limits

### Pricing Overview

Google offers three pricing tiers:

#### Free Tier
- Limited access to certain models
- Free input & output tokens
- Google AI Studio access

#### Paid Tier
- Higher rate limits for production deployments
- Context caching
- Batch API with 50% cost reduction

#### Enterprise
- Custom solutions via Vertex AI
- Dedicated support and volume discounts

### Model Pricing (Paid Tier, per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Gemini 3 Pro Preview | $2.00-$4.00 | $12.00-$18.00 |
| Gemini 2.5 Pro | $1.25-$2.50 | $10.00-$15.00 |
| Gemini 2.5 Flash | $0.30-$1.00 | $2.50 |
| Gemini 2.5 Flash-Lite | $0.10-$0.30 | $0.40 |
| Gemini 2.0 Flash | $0.10-$0.70 | $0.40 |

### Batch API Discounts

Batch processing offers approximately 50% cost reduction across all models.

### Additional Features

**Context Caching**: Ranges from $0.01-$0.40 per 1M tokens, plus $1.00/1M tokens per hour storage.

**Grounding**:
- Google Search: $35/1,000 grounded prompts (1,500 RPD free)
- Google Maps: $25/1,000 queries

**Image Generation**:
- Imagen 4: $0.02-$0.06 per image
- Imagen 3: $0.03 per image

**Video Generation**: Veo 3 pricing starts at $0.15-$0.40 per second.

### Rate Limits

The Gemini API evaluates usage across three key metrics:

- **RPM (Requests Per Minute)**: Maximum number of API calls allowed per minute
- **TPM (Tokens Per Minute)**: Maximum input tokens allowed per minute
- **RPD (Requests Per Day)**: Maximum API calls allowed per day

Your usage is evaluated against each limit, and exceeding any of them will trigger a rate limit error.

#### Usage Tiers

| Tier | Qualification |
|------|---------------|
| Free | Eligible country users |
| Tier 1 | Billing account linked |
| Tier 2 | >$250 spent + 30 days |
| Tier 3 | >$1,000 spent + 30 days |

#### Sample Rate Limits

**Free Tier:**
- Gemini 2.5 Flash: 10 RPM, 250,000 TPM, 250 RPD
- Gemini 2.0 Flash: 15 RPM, 1,000,000 TPM, 200 RPD

**Tier 3:**
- Gemini 2.5 Flash: 10,000 RPM, 8,000,000 TPM
- Gemini 2.0 Flash-Lite: 30,000 RPM, 30,000,000 TPM

### OpenAI Compatibility

Gemini models are accessible through OpenAI libraries (Python and TypeScript/JavaScript) and REST API by making minimal code changes.

#### Key Configuration Changes

1. **API Key**: Replace with your Gemini API key from Google AI Studio
2. **Base URL**: Set to `https://generativelanguage.googleapis.com/v1beta/openai/`
3. **Model**: Select a compatible Gemini model like `gemini-2.0-flash` or `gemini-2.5-flash`

#### Supported Features

- Text generation and streaming responses
- Function calling for structured outputs
- Image understanding (vision tasks)
- Image generation via Imagen models (paid tier only)
- Audio understanding and transcription
- Embeddings generation
- Structured JSON outputs
- Batch API operations
- Thinking capabilities with configurable reasoning effort levels
- Context caching via `extra_body` parameter

---

## Additional Resources

### Google AI Studio

[Google AI Studio](https://aistudio.google.com/) provides a web-based interface for:
- Testing and prototyping with Gemini models
- Managing API keys
- Exploring model capabilities
- Generating code snippets

### Documentation Links

- Main Documentation: https://ai.google.dev/gemini-api/docs
- API Reference: https://ai.google.dev/api
- Pricing Details: https://ai.google.dev/gemini-api/docs/pricing
- Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits

### Support

For additional support and community resources:
- GitHub Issues and Discussions
- Stack Overflow (tag: google-gemini-api)
- Official Google AI Developer Community

---

*Last Updated: November 2025*
*Based on Gemini API Documentation as of January 2025 model knowledge cutoff*
