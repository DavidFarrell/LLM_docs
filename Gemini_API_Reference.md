# Gemini API Reference

## Table of Contents

1. [Client Initialization](#client-initialization)
2. [Models API](#models-api)
3. [Files API](#files-api)
4. [Caching API](#caching-api)
5. [File Search API](#file-search-api)
6. [Embeddings API](#embeddings-api)
7. [Image Generation API](#image-generation-api)
8. [Video Generation API](#video-generation-api)
9. [Chat API](#chat-api)
10. [Live API](#live-api)
11. [Configuration Types](#configuration-types)
12. [Response Objects](#response-objects)
13. [Error Handling](#error-handling)

---

## Client Initialization

### Creating a Client

```python
from google import genai

# Using environment variable GEMINI_API_KEY
client = genai.Client()

# Explicit API key
client = genai.Client(api_key="YOUR_API_KEY")
```

### Environment Variables

The client automatically detects these environment variables:
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`

---

## Models API

### generate_content()

Generates a model response given an input request.

#### Signature

```python
client.models.generate_content(
    model: str,
    contents: Union[str, List[Union[str, Part]]],
    config: Optional[GenerateContentConfig] = None
) -> GenerateContentResponse
```

#### Parameters

- **model** (required): Model identifier (e.g., `"gemini-2.5-flash"`)
- **contents** (required): Prompt content as string, list of strings, or list of Parts
- **config** (optional): Configuration object for generation parameters

#### Example

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing"
)
print(response.text)
```

#### Advanced Example with Configuration

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt here",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant.",
        temperature=0.7,
        max_output_tokens=1000,
        top_p=0.95,
        top_k=40,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )
        ]
    )
)
```

### generate_content_stream()

Generates a streamed response from the model.

#### Signature

```python
client.models.generate_content_stream(
    model: str,
    contents: Union[str, List[Union[str, Part]]],
    config: Optional[GenerateContentConfig] = None
) -> Iterator[GenerateContentResponse]
```

#### Example

```python
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write a long story"
)

for chunk in response:
    print(chunk.text, end="")
```

### count_tokens()

Counts the number of tokens in the provided content.

#### Signature

```python
client.models.count_tokens(
    model: str,
    contents: Union[str, List[Union[str, Part]]]
) -> int
```

#### Example

```python
token_count = client.models.count_tokens(
    model="gemini-2.5-flash",
    contents="How many tokens is this?"
)
print(f"Total tokens: {token_count}")
```

### get()

Retrieves information about a specific model.

#### Signature

```python
client.models.get(
    name: str
) -> Model
```

#### Example

```python
model_info = client.models.get(name="gemini-2.5-flash")
print(f"Input token limit: {model_info.input_token_limit}")
print(f"Output token limit: {model_info.output_token_limit}")
```

### list()

Lists all available models.

#### Signature

```python
client.models.list() -> Iterator[Model]
```

#### Example

```python
for model in client.models.list():
    print(f"{model.name}: {model.display_name}")
```

---

## Files API

### upload()

Uploads a file for use with Gemini models.

#### Signature

```python
client.files.upload(
    file: Union[str, Path],
    config: Optional[UploadFileConfig] = None
) -> File
```

#### Parameters

- **file** (required): Path to the file to upload
- **config** (optional): Configuration including display name and metadata

#### Example

```python
myfile = client.files.upload(file="path/to/image.jpg")
print(f"Uploaded file: {myfile.name}")
```

#### With Configuration

```python
from google.genai import types

myfile = client.files.upload(
    file="document.pdf",
    config=types.UploadFileConfig(
        display_name="Important Document"
    )
)
```

### get()

Retrieves metadata about an uploaded file.

#### Signature

```python
client.files.get(
    name: str
) -> File
```

#### Example

```python
file_info = client.files.get(name="files/abc123")
print(f"File size: {file_info.size_bytes}")
print(f"MIME type: {file_info.mime_type}")
```

### list()

Lists all uploaded files.

#### Signature

```python
client.files.list() -> Iterator[File]
```

#### Example

```python
for file in client.files.list():
    print(f"{file.name}: {file.display_name}")
```

### delete()

Deletes an uploaded file.

#### Signature

```python
client.files.delete(
    name: str
) -> None
```

#### Example

```python
client.files.delete(name="files/abc123")
```

### download()

Downloads a file from the Files API.

#### Signature

```python
client.files.download(
    file: File,
    path: Optional[str] = None
) -> bytes
```

#### Example

```python
file_data = client.files.download(file=myfile)
# Or save to specific path
client.files.download(file=myfile, path="downloaded_file.mp4")
```

---

## Caching API

### create()

Creates a cached content object for reuse.

#### Signature

```python
client.caches.create(
    model: str,
    config: CreateCachedContentConfig
) -> CachedContent
```

#### Example

```python
from google.genai import types

files = [client.files.upload(file=f) for f in ["doc1.pdf", "doc2.pdf"]]

cache = client.caches.create(
    model="gemini-2.5-flash",
    config=types.CreateCachedContentConfig(
        contents=files,
        system_instruction="You are an expert analyst.",
        ttl="3600s"  # 1 hour
    )
)
```

### get()

Retrieves information about a cached content object.

#### Signature

```python
client.caches.get(
    name: str
) -> CachedContent
```

#### Example

```python
cache_info = client.caches.get(name="cachedContents/xyz789")
print(f"Expires at: {cache_info.expire_time}")
```

### list()

Lists all cached content objects.

#### Signature

```python
client.caches.list() -> Iterator[CachedContent]
```

#### Example

```python
for cache in client.caches.list():
    print(f"{cache.name}: {cache.display_name}")
```

### update()

Updates the TTL or expiration time of a cached content object.

#### Signature

```python
client.caches.update(
    name: str,
    config: UpdateCachedContentConfig
) -> CachedContent
```

#### Example

```python
from google.genai import types

updated_cache = client.caches.update(
    name="cachedContents/xyz789",
    config=types.UpdateCachedContentConfig(
        ttl="7200s"  # Extend to 2 hours
    )
)
```

### delete()

Deletes a cached content object.

#### Signature

```python
client.caches.delete(
    name: str
) -> None
```

#### Example

```python
client.caches.delete(name="cachedContents/xyz789")
```

---

## File Search API

### create()

Creates a file search store for RAG applications.

#### Signature

```python
client.file_search_stores.create(
    config: CreateFileSearchStoreConfig
) -> FileSearchStore
```

#### Example

```python
store = client.file_search_stores.create(
    config={'display_name': 'Knowledge Base'}
)
```

### upload_to_file_search_store()

Uploads a file directly to a file search store.

#### Signature

```python
client.file_search_stores.upload_to_file_search_store(
    file: Union[str, Path],
    file_search_store_name: str,
    config: Optional[UploadToFileSearchStoreConfig] = None
) -> Operation
```

#### Example

```python
import time

operation = client.file_search_stores.upload_to_file_search_store(
    file='document.txt',
    file_search_store_name=store.name,
    config={'display_name': 'Important Document'}
)

while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)
```

### import_file()

Imports an already-uploaded file into a file search store.

#### Signature

```python
client.file_search_stores.import_file(
    file_search_store_name: str,
    file_name: str,
    custom_metadata: Optional[List[Dict]] = None
) -> Operation
```

#### Example

```python
operation = client.file_search_stores.import_file(
    file_search_store_name=store.name,
    file_name="files/abc123",
    custom_metadata=[
        {"key": "author", "string_value": "Jane Doe"},
        {"key": "year", "numeric_value": 2024}
    ]
)
```

### list()

Lists all file search stores.

#### Signature

```python
client.file_search_stores.list() -> Iterator[FileSearchStore]
```

#### Example

```python
for store in client.file_search_stores.list():
    print(f"{store.name}: {store.display_name}")
```

### delete()

Deletes a file search store.

#### Signature

```python
client.file_search_stores.delete(
    name: str
) -> None
```

#### Example

```python
client.file_search_stores.delete(name=store.name)
```

---

## Embeddings API

### embed_content()

Generates embeddings for the provided content.

#### Signature

```python
client.models.embed_content(
    model: str,
    contents: Union[str, List[str]],
    config: Optional[EmbedContentConfig] = None
) -> EmbedContentResponse
```

#### Parameters

- **model** (required): Embedding model identifier (e.g., `"gemini-embedding-001"`)
- **contents** (required): Text or list of texts to embed
- **config** (optional): Configuration including task type and output dimensionality

#### Example

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)
print(result.embeddings)
```

#### Advanced Example

```python
from google.genai import types

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "First text to embed",
        "Second text to embed",
        "Third text to embed"
    ],
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768
    )
)

for i, embedding in enumerate(result.embeddings):
    print(f"Embedding {i}: {len(embedding.values)} dimensions")
```

#### Task Types

- `SEMANTIC_SIMILARITY` - For measuring text similarity
- `CLASSIFICATION` - For text classification tasks
- `CLUSTERING` - For grouping similar texts
- `RETRIEVAL_DOCUMENT` - For indexing documents
- `RETRIEVAL_QUERY` - For search queries
- `CODE_RETRIEVAL_QUERY` - For code search
- `QUESTION_ANSWERING` - For Q&A systems
- `FACT_VERIFICATION` - For fact-checking

---

## Image Generation API

### generate_images()

Generates images from text prompts using Imagen models.

#### Signature

```python
client.models.generate_images(
    model: str,
    prompt: str,
    config: Optional[GenerateImagesConfig] = None
) -> GenerateImagesResponse
```

#### Parameters

- **model** (required): Image generation model (e.g., `"imagen-4.0-generate-001"`)
- **prompt** (required): Text description of the image to generate
- **config** (optional): Configuration for image generation

#### Example

```python
from google.genai import types

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='A serene mountain landscape at sunset',
    config=types.GenerateImagesConfig(
        number_of_images=4,
        aspect_ratio="16:9",
        image_size="2K"
    )
)

for i, generated_image in enumerate(response.generated_images):
    generated_image.image.show()
    # Or save to file
    generated_image.image.save(f"image_{i}.png")
```

#### Configuration Options

- **number_of_images**: 1-4 (default: 4)
- **image_size**: "1K" or "2K" (default: "1K")
- **aspect_ratio**: "1:1", "3:4", "4:3", "9:16", "16:9" (default: "1:1")
- **person_generation**: "dont_allow", "allow_adult", "allow_all" (default: "allow_adult")
- **negative_prompt**: Text describing what to avoid in the image

---

## Video Generation API

### generate_videos()

Generates videos from text prompts using Veo models.

#### Signature

```python
client.models.generate_videos(
    model: str,
    prompt: str,
    config: Optional[GenerateVideosConfig] = None
) -> Operation
```

#### Example

```python
import time
from google import genai

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A robot walking through a futuristic city"
)

# Poll for completion
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("output.mp4")
```

#### Video Generation Features

- Text-to-video with audio
- Image-to-video conversion
- Reference image support (up to 3 images)
- Frame interpolation
- Video extension (up to 7 seconds)

---

## Chat API

### create()

Creates a chat session for multi-turn conversations.

#### Signature

```python
client.chats.create(
    model: str,
    config: Optional[GenerateContentConfig] = None
) -> Chat
```

#### Example

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful coding assistant.",
        temperature=0.7
    )
)
```

### send_message()

Sends a message in the chat session.

#### Signature

```python
chat.send_message(
    message: Union[str, List[Part]]
) -> GenerateContentResponse
```

#### Example

```python
# First turn
response = chat.send_message("What is Python?")
print(response.text)

# Second turn (context maintained)
response = chat.send_message("What are its key features?")
print(response.text)
```

### history

Access the conversation history.

#### Example

```python
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text}")
```

---

## Live API

### Sessions

The Live API uses WebSocket connections for real-time interactions.

#### send_realtime_input()

Sends audio, video, or text input to a live session.

#### Example

```python
import librosa
import soundfile as sf

# Load and convert audio
audio, sr = librosa.load("input.mp3", sr=16000, mono=True)
audio_16bit = (audio * 32767).astype('int16')

# Send to session
session.send_realtime_input(
    audio_blob=audio_16bit.tobytes()
)
```

---

## Configuration Types

### GenerateContentConfig

Main configuration object for content generation.

#### Fields

```python
class GenerateContentConfig:
    system_instruction: Optional[str]
    temperature: Optional[float]
    max_output_tokens: Optional[int]
    top_p: Optional[float]
    top_k: Optional[int]
    response_mime_type: Optional[str]
    response_json_schema: Optional[dict]
    tools: Optional[List[Tool]]
    safety_settings: Optional[List[SafetySetting]]
    thinking_config: Optional[ThinkingConfig]
    cached_content: Optional[str]
```

#### Example

```python
from google.genai import types

config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant.",
    temperature=0.7,
    max_output_tokens=2000,
    top_p=0.95,
    top_k=40
)
```

### ThinkingConfig

Configuration for thinking mode.

#### Fields

```python
class ThinkingConfig:
    include_thoughts: Optional[bool]
    thinking_budget: Optional[int]  # Gemini 2.5
    thinking_level: Optional[str]   # Gemini 3: "low" or "high"
```

#### Example

```python
from google.genai import types

# Enable thinking with thought summaries
thinking_config = types.ThinkingConfig(
    include_thoughts=True,
    thinking_budget=1024
)

# Disable thinking
thinking_config = types.ThinkingConfig(
    thinking_budget=0
)
```

### SafetySetting

Configuration for content safety filtering.

#### Fields

```python
class SafetySetting:
    category: HarmCategory
    threshold: HarmBlockThreshold
```

#### Harm Categories

- `HARM_CATEGORY_HARASSMENT`
- `HARM_CATEGORY_HATE_SPEECH`
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`
- `HARM_CATEGORY_DANGEROUS_CONTENT`

#### Block Thresholds

- `BLOCK_NONE`
- `BLOCK_ONLY_HIGH`
- `BLOCK_MEDIUM_AND_ABOVE`
- `BLOCK_LOW_AND_ABOVE`
- `OFF`

#### Example

```python
from google.genai import types

safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
    )
]
```

### Tool

Configuration for tools and function calling.

#### Tool Types

```python
# Code execution
tool = types.Tool(code_execution=types.ToolCodeExecution)

# Google Search grounding
tool = types.Tool(google_search=types.GoogleSearch())

# File Search
tool = types.Tool(
    file_search=types.FileSearch(
        file_search_store_names=[store.name]
    )
)

# URL Context
tool = types.Tool(url_context={})

# Computer Use
tool = types.Tool(
    computer_use=types.ComputerUse(
        environment=types.Environment.ENVIRONMENT_BROWSER
    )
)

# Function calling
tool = types.Tool(
    function_declarations=[function_declaration]
)
```

### Part

Represents a part of the content (text, image, video, etc.).

#### Creating Parts

```python
from google.genai import types

# Text part
text_part = "Your text here"

# Image part from bytes
with open('image.jpg', 'rb') as f:
    image_bytes = f.read()

image_part = types.Part.from_bytes(
    data=image_bytes,
    mime_type='image/jpeg'
)

# File part
file_part = client.files.upload(file="video.mp4")
```

---

## Response Objects

### GenerateContentResponse

Response from generate_content() or generate_content_stream().

#### Fields

```python
class GenerateContentResponse:
    text: str                           # Convenience property
    candidates: List[Candidate]
    prompt_feedback: PromptFeedback
    usage_metadata: UsageMetadata
    model_version: str
    response_id: str
```

#### Example

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello!"
)

print(response.text)
print(f"Total tokens: {response.usage_metadata.total_token_count}")
print(f"Model version: {response.model_version}")
```

### Candidate

Individual response candidate.

#### Fields

```python
class Candidate:
    content: Content
    finish_reason: FinishReason
    safety_ratings: List[SafetyRating]
    grounding_metadata: Optional[GroundingMetadata]
    citation_metadata: Optional[CitationMetadata]
```

#### Finish Reasons

- `STOP` - Natural completion
- `MAX_TOKENS` - Reached token limit
- `SAFETY` - Blocked by safety filters
- `RECITATION` - Blocked due to recitation
- `OTHER` - Other reason

#### Example

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write a story"
)

candidate = response.candidates[0]
print(f"Finish reason: {candidate.finish_reason}")
print(f"Content: {candidate.content.parts[0].text}")
```

### UsageMetadata

Token usage information.

#### Fields

```python
class UsageMetadata:
    prompt_token_count: int
    candidates_token_count: int
    total_token_count: int
    thoughts_token_count: Optional[int]  # For thinking mode
    cached_content_token_count: Optional[int]
```

#### Example

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt"
)

usage = response.usage_metadata
print(f"Prompt tokens: {usage.prompt_token_count}")
print(f"Response tokens: {usage.candidates_token_count}")
print(f"Total tokens: {usage.total_token_count}")
```

### GroundingMetadata

Metadata for grounded responses (from Google Search or File Search).

#### Fields

```python
class GroundingMetadata:
    web_search_queries: List[str]
    grounding_chunks: List[GroundingChunk]
    grounding_supports: List[GroundingSupport]
    search_entry_point: Optional[SearchEntryPoint]
```

#### Example

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What happened at CES 2025?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)

grounding = response.candidates[0].grounding_metadata
print("Search queries used:")
for query in grounding.web_search_queries:
    print(f"  - {query}")

print("\nSources:")
for chunk in grounding.grounding_chunks:
    print(f"  - {chunk.web.title}: {chunk.web.uri}")
```

### File

Represents an uploaded file.

#### Fields

```python
class File:
    name: str
    display_name: str
    mime_type: str
    size_bytes: int
    create_time: str
    update_time: str
    expiration_time: str
    sha256_hash: str
    uri: str
    state: FileState
    error: Optional[Status]
```

#### File States

- `PROCESSING` - File is being processed
- `ACTIVE` - File is ready for use
- `FAILED` - File processing failed

#### Example

```python
file = client.files.upload(file="document.pdf")

print(f"File name: {file.name}")
print(f"Size: {file.size_bytes} bytes")
print(f"MIME type: {file.mime_type}")
print(f"Expires: {file.expiration_time}")
print(f"State: {file.state}")
```

### Model

Information about a model.

#### Fields

```python
class Model:
    name: str
    display_name: str
    description: str
    input_token_limit: int
    output_token_limit: int
    supported_generation_methods: List[str]
    temperature: Optional[float]
    top_p: Optional[float]
    top_k: Optional[int]
```

#### Example

```python
model = client.models.get(name="gemini-2.5-flash")

print(f"Model: {model.display_name}")
print(f"Description: {model.description}")
print(f"Input limit: {model.input_token_limit} tokens")
print(f"Output limit: {model.output_token_limit} tokens")
```

### EmbedContentResponse

Response from embed_content().

#### Fields

```python
class EmbedContentResponse:
    embeddings: List[ContentEmbedding]
```

#### ContentEmbedding

```python
class ContentEmbedding:
    values: List[float]
```

#### Example

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=["Text to embed"]
)

embedding = result.embeddings[0]
print(f"Embedding dimensions: {len(embedding.values)}")
print(f"First few values: {embedding.values[:5]}")
```

### GenerateImagesResponse

Response from generate_images().

#### Fields

```python
class GenerateImagesResponse:
    generated_images: List[GeneratedImage]
```

#### GeneratedImage

```python
class GeneratedImage:
    image: Image
```

#### Example

```python
response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='A peaceful garden'
)

for i, generated_image in enumerate(response.generated_images):
    # Display image
    generated_image.image.show()

    # Save to file
    generated_image.image.save(f"image_{i}.png")
```

---

## Error Handling

### Common Exceptions

#### Rate Limit Errors

```python
from google.api_core import exceptions

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Your prompt"
    )
except exceptions.ResourceExhausted as e:
    print("Rate limit exceeded. Please retry later.")
    print(f"Error: {e}")
```

#### Safety Blocking

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt"
)

if response.candidates[0].finish_reason == "SAFETY":
    print("Response blocked by safety filters")
    for rating in response.candidates[0].safety_ratings:
        print(f"  {rating.category}: {rating.probability}")
```

#### Invalid API Key

```python
try:
    client = genai.Client(api_key="invalid_key")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Test"
    )
except exceptions.Unauthenticated as e:
    print("Invalid API key")
    print(f"Error: {e}")
```

#### File Not Found

```python
try:
    file = client.files.upload(file="nonexistent.txt")
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

#### Model Not Found

```python
try:
    response = client.models.generate_content(
        model="nonexistent-model",
        contents="Test"
    )
except exceptions.NotFound as e:
    print(f"Model not found: {e}")
```

### Best Practices for Error Handling

```python
from google.api_core import exceptions
import time

def generate_with_retry(client, model, contents, max_retries=3):
    """Generate content with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response

        except exceptions.ResourceExhausted:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) * 1  # Exponential backoff
            print(f"Rate limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)

        except exceptions.DeadlineExceeded:
            if attempt == max_retries - 1:
                raise
            print(f"Request timeout. Retrying...")
            time.sleep(2)

        except exceptions.ServiceUnavailable:
            if attempt == max_retries - 1:
                raise
            print(f"Service unavailable. Retrying...")
            time.sleep(5)

# Usage
response = generate_with_retry(
    client,
    model="gemini-2.5-flash",
    contents="Your prompt"
)
```

---

## HTTP REST API Reference

### Base URL

```
https://generativelanguage.googleapis.com/v1beta
```

### Authentication

Include your API key as a query parameter or header:

```
GET /v1beta/models/gemini-2.5-flash?key=YOUR_API_KEY
```

Or as a header:

```
Authorization: Bearer YOUR_API_KEY
```

### Generate Content Endpoint

#### Non-Streaming

```
POST /v1beta/models/{model}:generateContent
```

**Request Body:**

```json
{
  "contents": [
    {
      "parts": [
        {"text": "Your prompt here"}
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 1000,
    "topP": 0.95,
    "topK": 40
  },
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

**Response:**

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {"text": "Generated response here"}
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "safetyRatings": [...]
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 50,
    "totalTokenCount": 60
  }
}
```

#### Streaming

```
POST /v1beta/models/{model}:streamGenerateContent
```

Returns a stream of `GenerateContentResponse` objects.

### Embeddings Endpoint

```
POST /v1beta/models/{model}:embedContent
```

**Request Body:**

```json
{
  "content": {
    "parts": [
      {"text": "Text to embed"}
    ]
  },
  "taskType": "RETRIEVAL_DOCUMENT",
  "outputDimensionality": 768
}
```

**Response:**

```json
{
  "embedding": {
    "values": [0.123, -0.456, 0.789, ...]
  }
}
```

### List Models Endpoint

```
GET /v1beta/models
```

**Response:**

```json
{
  "models": [
    {
      "name": "models/gemini-2.5-flash",
      "displayName": "Gemini 2.5 Flash",
      "description": "Fast and versatile multimodal model",
      "inputTokenLimit": 1048576,
      "outputTokenLimit": 65536,
      ...
    },
    ...
  ]
}
```

### File Upload Endpoint

```
POST /upload/v1beta/files
```

Multipart upload with file data and metadata.

---

## OpenAI Compatibility

### Configuration

To use Gemini with OpenAI client libraries:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Supported Features

- Chat completions (streaming and non-streaming)
- Function calling
- Vision (image understanding)
- Embeddings
- Image generation (paid tier only)
- Audio understanding
- Structured outputs

### Gemini-Specific Parameters

Use `extra_body` to pass Gemini-specific parameters:

```python
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[{"role": "user", "content": "Solve this math problem"}],
    extra_body={
        "thinking_config": {
            "include_thoughts": True,
            "thinking_budget": 1024
        }
    }
)
```

---

## Rate Limits by Tier

### Free Tier

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Flash | 10 | 250,000 | 250 |
| Gemini 2.0 Flash | 15 | 1,000,000 | 200 |
| Gemini Embedding | 1,500 | 1,000,000 | - |

### Tier 1 (Billing Enabled)

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Flash | 1,000 | 4,000,000 | - |
| Gemini 2.0 Flash | 2,000 | 4,000,000 | - |

### Tier 2 ($250+ spent)

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Flash | 2,000 | 4,000,000 | - |
| Gemini 2.5 Pro | 1,000 | 4,000,000 | - |

### Tier 3 ($1000+ spent)

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Flash | 10,000 | 8,000,000 | - |
| Gemini 2.5 Pro | 5,000 | 8,000,000 | - |
| Gemini 2.0 Flash-Lite | 30,000 | 30,000,000 | - |

---

## Token Limits by Model

| Model | Input Tokens | Output Tokens |
|-------|--------------|---------------|
| Gemini 3 Pro Preview | 1,048,576 | 65,536 |
| Gemini 2.5 Pro | 1,048,576 | 65,536 |
| Gemini 2.5 Flash | 1,048,576 | 65,536 |
| Gemini 2.5 Flash-Lite | 1,048,576 | 65,536 |
| Gemini 2.0 Flash | 1,048,576 | 8,192 |
| Gemini Embedding | 2,048 | N/A |

---

## Multimodal Token Calculation

### Images

- Images ≤384px on both sides: **258 tokens**
- Larger images: Tiled at 768×768px, **258 tokens per tile**

### Video

- **263 tokens per second** of video

### Audio

- **32 tokens per second** of audio
- Maximum audio length: 9.5 hours (approximately 1,094,400 tokens)

### Documents (PDF)

- **258 tokens per page**
- Maximum: 1,000 pages

---

## SDK Version Information

### Python SDK

```bash
pip install -U google-genai
```

**Package:** `google-genai`

**Import:**
```python
from google import genai
from google.genai import types
```

### Version Checking

```python
import google.genai as genai
print(genai.__version__)
```

---

*Last Updated: November 2025*
*Based on Gemini API Documentation as of January 2025*
