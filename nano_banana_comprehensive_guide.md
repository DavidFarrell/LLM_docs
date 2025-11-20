# Nano Banana & Nano Banana Pro: Comprehensive Guide

## Table of Contents

1. [Introduction](#introduction)
2. [What is Nano Banana?](#what-is-nano-banana)
3. [Model Versions](#model-versions)
4. [Getting Started](#getting-started)
5. [Core Capabilities](#core-capabilities)
6. [API Usage & Examples](#api-usage--examples)
7. [Advanced Features](#advanced-features)
8. [Prompting Best Practices](#prompting-best-practices)
9. [Configuration & Options](#configuration--options)
10. [Pricing & Availability](#pricing--availability)
11. [Limitations & Considerations](#limitations--considerations)
12. [Use Cases](#use-cases)

---

## Introduction

Nano Banana is the unofficial but widely-adopted name for Google's advanced image generation and editing models powered by Gemini. The name originated as a placeholder during secret public testing on LMArena and became so popular that Google embraced it, even incorporating banana icons 🍌 throughout the Gemini app.

### The Name Story

When the model was uploaded to the LM Arena benchmark site for early testing, a product manager named Nina typed "Nano Banana" as a personal placeholder to signify that its origins were unknown. The name stuck, went viral on social media, and eventually became the colloquial name for the model—much catchier than its official designation "Gemini 2.5 Flash Image."

After Nano Banana pushed the Gemini app to the top of mobile App Stores and powered over 5 billion image creations, Google officially launched **Nano Banana Pro** on November 20, 2025, powered by Gemini 3 Pro.

---

## What is Nano Banana?

Nano Banana represents Google's advanced image generation and editing AI, combining:

- **Deep language understanding** for interpreting complex prompts
- **Multimodal capabilities** blending text and images
- **Gemini's world knowledge** for contextually accurate outputs
- **Conversational editing** for iterative refinement
- **Character consistency** across multiple images
- **Real-time information** integration for up-to-date content

Unlike traditional image generators that rely on keyword matching, Nano Banana leverages Gemini's natural language reasoning to understand narrative descriptions and context.

---

## Model Versions

### Nano Banana (Gemini 2.5 Flash Image)

**Official Model ID:** `gemini-2.5-flash-image` or `gemini-2.5-flash-image-preview`

**Launch Date:** August 26, 2025

**Key Features:**
- Text-to-image generation
- Image editing with natural language
- Multi-image composition (up to 3 images recommended)
- Character consistency
- Aspect ratios from 1:1 to 21:9
- Output resolution: 1024×1024px (standard ratios)
- SynthID digital watermarking
- Conversational iterative refinement

**Best For:**
- Quick image generation
- Real-time editing
- Mobile and web app integration
- Cost-effective image creation

**Pricing:** $30 per 1 million output tokens (~$0.039 per image, 1290 tokens each)

### Nano Banana Pro (Gemini 3 Pro Image)

**Official Model ID:** `gemini-3-pro-image`

**Launch Date:** November 20, 2025

**Key Features:**
- All capabilities of original Nano Banana, plus:
- **4K resolution output** (up to 4K, also 2K options)
- **Advanced aspect ratio control** (16:9 to 9:16)
- **Blend up to 14 images** (vs. 3 in original)
- **Maintain consistency of up to 5 people** (vs. 1-2 in original)
- **Enhanced multilingual text rendering** in images
- **Advanced camera controls** (angles, focus, depth of field)
- **Sophisticated lighting control** (day-to-night, bokeh effects)
- **Professional color grading**
- **Localized editing** (select and transform specific regions)
- **Infographic and diagram generation** with real-time data
- **Watermark removal** (Ultra subscribers only)

**Best For:**
- Professional design work
- Marketing materials
- Print media
- High-resolution social content
- Complex multi-subject compositions
- Educational infographics

**Pricing:** Pricing details TBD; available with Gemini Pro/Ultra subscriptions

---

## Getting Started

### Prerequisites

1. **Google Account** - Required for API access
2. **API Key** - Obtain from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. **Python 3.9+** (for API usage)

### Installation

```bash
# Install the Google Generative AI SDK
pip install -q -U google-generativeai

# Or use the newer genai package
pip install -q -U google-genai
```

### Authentication

Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or pass it explicitly in code:

```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
```

### Your First Image

**Using the Gemini App (Easiest):**
1. Open the Gemini app (web or mobile)
2. For Nano Banana Pro: Select "Thinking" mode (Gemini 3 Pro)
3. Click "Create images" or type a prompt like "Generate an image of..."
4. Describe what you want in natural language

**Using Python:**

```python
from google import genai
from PIL import Image

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # or "gemini-3-pro-image" for Pro
    contents="A nano banana floating in space, photorealistic, 4K quality"
)

# Save the generated image
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("nano_banana.png")
```

---

## Core Capabilities

### 1. Text-to-Image Generation

Generate high-quality images from descriptive text prompts.

**Example:**
```python
prompt = "A futuristic laboratory with a tiny banana being examined under a microscope, cinematic lighting, bokeh effect, 16:9 aspect ratio"

response = model.generate_content([prompt])
```

**Best Practices:**
- Use narrative descriptions, not just keywords
- Specify style, lighting, and mood
- Include aspect ratio requirements for Nano Banana Pro
- Mention resolution needs (2K, 4K) when using Pro

### 2. Image Editing

Edit existing images using natural language instructions.

**Example:**
```python
import base64

# Load existing image
with open('original.jpg', 'rb') as img_file:
    img_data = base64.b64encode(img_file.read()).decode()

# Edit with natural language
response = model.generate_content([
    {
        'inline_data': {
            'mime_type': 'image/jpeg',
            'data': img_data
        }
    },
    "Change the background to a beach at sunset, add bokeh effect"
])
```

**Editing Capabilities:**
- Background replacement
- Object removal/addition
- Color grading and filters
- Lighting adjustments
- Pose modifications
- Style transfer
- Selective colorization
- Blur/focus effects

### 3. Multi-Image Composition

Blend multiple images into a cohesive composition.

**Nano Banana:** Up to 3 images
**Nano Banana Pro:** Up to 14 images

**Example:**
```python
response = model.generate_content([
    image1,
    image2,
    image3,
    "Blend these three images: place the person from image 1 in the environment from image 2, with the lighting style from image 3"
])
```

### 4. Character Consistency

Maintain the same character across multiple scenes and environments.

**Nano Banana Pro** can maintain consistency for up to 5 people simultaneously.

**Example:**
```python
response = model.generate_content([
    reference_image,
    "Show this same person in a business meeting, a coffee shop, and at the beach. Maintain facial features, style, and appearance across all three scenes."
])
```

### 5. Text Rendering in Images

Generate images containing legible, well-placed text—ideal for logos, diagrams, posters, and infographics.

**Nano Banana Pro** offers enhanced multilingual text support with varied fonts, textures, and calligraphy styles.

**Example:**
```python
response = model.generate_content([
    "Create a professional conference poster with the title 'AI Innovation Summit 2025' in bold modern font, featuring abstract tech imagery, 16:9 aspect ratio, 4K resolution"
])
```

### 6. Localized Editing (Pro Only)

Select and transform specific regions of an image.

**Example:**
```python
response = model.generate_content([
    original_image,
    "Select only the car in this image and change its color to metallic blue, leave everything else unchanged"
])
```

### 7. Advanced Camera & Lighting Control (Pro Only)

Professional-grade controls for photography and cinematography effects.

**Camera Controls:**
- Angle adjustments
- Focus and depth of field
- Bokeh effects
- Lens simulation

**Lighting Controls:**
- Day-to-night transformation
- Studio lighting setup
- Color temperature
- Shadow and highlight control

**Example:**
```python
response = model.generate_content([
    photo,
    "Adjust this photo to golden hour lighting, shallow depth of field with f/1.8 bokeh, cinematic color grading, camera angle slightly lower"
])
```

---

## API Usage & Examples

### Basic Python Setup

```python
import os
import base64
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize model
model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
```

### Example 1: Simple Text-to-Image

```python
response = model.generate_content([
    "A cute nano-sized banana wearing a tiny lab coat, 3D rendered, Pixar style"
])

# Extract and save image
generated_img = base64.b64decode(response.parts[0].inline_data.data)
with open('cute_nano_banana.png', 'wb') as f:
    f.write(generated_img)
```

### Example 2: Image Editing

```python
# Load original image
with open('banana.jpg', 'rb') as img_file:
    img_data = base64.b64encode(img_file.read()).decode()

# Apply edits
response = model.generate_content([
    {
        'inline_data': {
            'mime_type': 'image/jpeg',
            'data': img_data
        }
    },
    "Make this banana nano-sized, place it on a circuit board with tiny electronic components around it"
])

# Save edited image
output_img = base64.b64decode(response.parts[0].inline_data.data)
with open('nano_banana_circuit.png', 'wb') as f:
    f.write(output_img)
```

### Example 3: Multi-Turn Conversation

```python
# Start a chat for iterative editing
chat = model.start_chat(history=[])

# First generation
response1 = chat.send_message([
    "Create a minimalist logo with a banana and the word 'nano'"
])

# Iterative refinement
response2 = chat.send_message([
    "Make the banana smaller and add a circuit pattern inside it"
])

response3 = chat.send_message([
    "Change the color scheme to blue and gold"
])

# Each response builds on the previous context
```

### Example 4: Using Nano Banana Pro with 4K Output

```python
# Use Gemini 3 Pro Image model
pro_model = genai.GenerativeModel('gemini-3-pro-image')

response = pro_model.generate_content([
    "Professional product photography of a nano banana on a marble surface, studio lighting, macro lens, 16:9 aspect ratio, 4K resolution, color graded"
])

# Save high-resolution output
output_img = base64.b64decode(response.parts[0].inline_data.data)
with open('nano_banana_pro_4k.png', 'wb') as f:
    f.write(output_img)
```

### Example 5: Complex Multi-Image Composition (Pro)

```python
from PIL import Image
import io

# Load multiple images
images = []
for i in range(5):
    with open(f'image{i}.jpg', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode()
        images.append({
            'inline_data': {
                'mime_type': 'image/jpeg',
                'data': img_data
            }
        })

# Create complex composition
response = pro_model.generate_content([
    *images,
    "Create a professional team photo using these 5 people. Place them in a modern office setting with natural window lighting, maintain each person's appearance and facial features, 16:9 aspect ratio, 2K resolution"
])
```

### Example 6: Safety Configuration

```python
# Configure content safety filters
safety_settings = [
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    }
]

response = model.generate_content(
    [prompt],
    safety_settings=safety_settings
)
```

### Example 7: Infographic Generation (Pro)

```python
response = pro_model.generate_content([
    "Create an educational infographic showing the lifecycle of a banana from tree to market, include 5 stages with clear labels, icons, and arrows, modern flat design style, 9:16 vertical format for social media, 2K resolution"
])
```

---

## Advanced Features

### Conversational Image Creation

Nano Banana maintains context across multiple turns, allowing for iterative refinement:

```python
chat = model.start_chat()

# Initial creation
chat.send_message("Create a logo for a tech startup called NanoTech")

# Refinements
chat.send_message("Add a banana icon to represent the nano concept")
chat.send_message("Make it more minimalist and modern")
chat.send_message("Change the font to something more futuristic")
```

### Semantic Masking

The model understands which parts of an image to modify based on semantic understanding, not pixel-level masks:

```python
response = model.generate_content([
    original_image,
    "Remove all people from this image but keep everything else exactly the same"
])
```

### Style Transfer

Apply artistic styles or photographic techniques to existing images:

```python
response = model.generate_content([
    photo,
    style_reference,
    "Apply the artistic style from the second image to the first image"
])
```

### Template Adherence (Pro)

Nano Banana Pro excels at following visual templates for applications like:
- Real estate listing cards
- Product mockups
- Social media posts
- Presentation slides

```python
response = pro_model.generate_content([
    template_image,
    product_image,
    "Place this product into the template layout, maintaining the template's style and proportions, 16:9 format, 2K resolution"
])
```

### Real-Time Information Integration (Pro)

Gemini 3 Pro's world knowledge enables image generation with current information:

```python
response = pro_model.generate_content([
    "Create an infographic showing today's global renewable energy statistics with accurate data, modern design, clear data visualizations"
])
```

---

## Prompting Best Practices

### Core Principle: Describe, Don't List

The model's greatest strength is language understanding. Instead of keywords, write narrative descriptions.

**Poor Prompt:**
```
banana, nano, laboratory, blue, modern
```

**Good Prompt:**
```
A microscopic banana being examined in a state-of-the-art laboratory, bathed in cool blue LED lighting, with modern scientific equipment in the background, photorealistic style
```

### Prompting Strategies

#### 1. Be Hyper-Specific

Include details about:
- **Subject**: What is the main focus?
- **Setting**: Where does this take place?
- **Lighting**: What's the light source and quality?
- **Mood**: What emotion should it convey?
- **Style**: Photorealistic, artistic, 3D, illustration?
- **Perspective**: Camera angle and distance

**Example:**
```
A macro photograph of a nano-scale banana resting on a human fingertip, shot with a 100mm macro lens at f/2.8, soft natural window lighting from the left, shallow depth of field with creamy bokeh, warm color temperature, capturing the wonder of scale
```

#### 2. Use Photographic Terminology

For photorealistic images, employ professional photography language:

- Lens types: "50mm prime", "wide-angle 24mm", "telephoto 200mm"
- Aperture: "f/1.4 for shallow DOF", "f/8 for sharpness"
- Lighting: "golden hour", "studio softbox", "rim lighting"
- Composition: "rule of thirds", "leading lines", "symmetrical"

**Example:**
```
Product photography of a nano banana, 85mm lens, f/1.8 aperture creating smooth bokeh, three-point studio lighting setup, shot on a marble surface with subtle reflections, commercial photography style
```

#### 3. Specify Purpose and Context

Explain what the image will be used for:

**Example:**
```
Create a social media banner for Instagram (16:9) promoting a nanotechnology conference, featuring a stylized nano banana icon, modern gradient background (blue to purple), bold sans-serif typography saying "NanoTech Summit 2025", professional and eye-catching design
```

#### 4. Iterative Refinement

Start broad, then refine through conversation:

```
Turn 1: "Create a logo for a nano technology company"
Turn 2: "Make it more minimal and modern"
Turn 3: "Add a banana element to represent 'nano'"
Turn 4: "Change colors to teal and gold"
```

#### 5. Use Negative Space Strategically

For designs needing text overlay, request space:

**Example:**
```
Create a background image for a presentation slide, abstract tech pattern with circuit board elements in dark blue tones, leave the center third empty for text overlay, minimalist design, 16:9 format
```

#### 6. Style-Specific Prompts

**Photorealistic:**
```
Professional headshot photograph of a scientist holding a nano banana sample in a laboratory, natural window lighting, shot with 85mm f/1.4 lens, shallow depth of field, warm color grading, captured with high-end DSLR
```

**Illustration:**
```
Whimsical children's book illustration of a tiny banana exploring a giant kitchen, watercolor style, soft pastel colors, friendly and approachable art style, storybook quality
```

**3D Render:**
```
Cinema 4D style 3D render of a nano banana, glossy surface with subsurface scattering, studio lighting with colored gels, floating against a gradient background, raytraced reflections, 4K quality
```

**Minimalist Design:**
```
Ultra-minimalist logo design featuring a geometric banana shape, single color (navy blue), clean lines, negative space, suitable for app icon, SVG-style clarity
```

#### 7. Sequential Art and Storyboards

**Example:**
```
Create a 4-panel comic strip showing: Panel 1: A regular banana in a grocery store. Panel 2: Scientists shrinking it in a lab. Panel 3: The nano banana next to a regular paperclip for scale. Panel 4: The nano banana entering a human cell. Consistent art style throughout, modern scientific illustration style, clear panel divisions
```

#### 8. Aspect Ratio and Resolution Specification (Pro)

Always specify for professional work:

**Examples:**
```
"Create a product mockup, 16:9 aspect ratio, 4K resolution for print"
"Design an Instagram story graphic, 9:16 vertical format, 2K resolution"
"Generate a wide banner image, 21:9 ultra-wide format, 4K quality"
```

---

## Configuration & Options

### Output Modalities

Control what types of content the model returns:

```python
from google.genai import types

response = model.generate_content(
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]  # or ["TEXT", "IMAGE"]
    )
)
```

### Aspect Ratio Options

**Nano Banana (2.5 Flash Image):**
- 1:1 (1024×1024px)
- 3:4 (768×1024px)
- 4:3 (1024×768px)
- 9:16 (768×1344px)
- 16:9 (1344×768px)
- 21:9 (1536×672px)

All ratios use 1290 output tokens per image.

**Nano Banana Pro (3 Pro Image):**
- All above ratios plus more granular control
- Resolutions: Standard, 2K, 4K
- Specify in prompt: "16:9 aspect ratio, 4K resolution"

### Safety Settings

Configure content filtering thresholds:

```python
safety_settings = [
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'  # or BLOCK_LOW_AND_ABOVE, BLOCK_MEDIUM_AND_ABOVE, BLOCK_HIGH
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    },
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
    }
]
```

### Image Input Configuration

Supported formats:
- JPEG
- PNG
- WebP
- Base64-encoded images

**Recommended maximum image size:** ~4MB per image for optimal performance

```python
# Reading and encoding images
from PIL import Image
import io

def prepare_image(image_path):
    img = Image.open(image_path)
    # Resize if needed
    if img.size[0] > 2048 or img.size[1] > 2048:
        img.thumbnail((2048, 2048), Image.LANCZOS)

    # Convert to bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()

    return base64.b64encode(img_bytes).decode()
```

---

## Pricing & Availability

### Nano Banana (Gemini 2.5 Flash Image)

**Pricing:**
- **$30.00 per 1 million output tokens**
- Each image = 1290 output tokens
- **Cost per image: ~$0.039 (approximately 4 cents)**

**Availability:**
- Gemini API (stable)
- Google AI Studio
- Vertex AI
- Gemini App (web and mobile)

**Free Tier:**
- Available to all users with usage limits
- Rate limits apply

### Nano Banana Pro (Gemini 3 Pro Image)

**Pricing:**
- Included with Gemini Pro and Ultra subscriptions
- API pricing details TBD
- Higher resolution outputs may have different token costs

**Availability (as of November 20, 2025):**
- **Gemini App**: Global rollout
- **NotebookLM**: Paid users worldwide
- **Google AI Studio**: Available
- **Vertex AI**: Available
- **Gemini API**: Available
- **Google Workspace**: Coming to Slides and Vids
- **Google Ads**: Select availability
- **Flow**: Select availability

**Tier Access:**
- **Free users**: Limited quota
- **Google AI Plus subscribers**: Higher usage limits
- **Google AI Pro subscribers**: Higher usage limits
- **Google AI Ultra subscribers**: Highest limits + watermark removal

### Usage Quotas

Quotas vary by subscription tier and are subject to change. Check [Google AI Studio](https://aistudio.google.com/) for current limits.

---

## Limitations & Considerations

### Technical Limitations

**Input Constraints:**
- Maximum 3 input images recommended (Nano Banana)
- Maximum 14 input images (Nano Banana Pro)
- Image file size should be under ~4MB
- No video or audio input support
- Best performance with clear, high-quality input images

**Output Constraints:**
- All images include SynthID digital watermarks (removable for Ultra subscribers in Pro)
- Generation times vary based on complexity
- Rate limits apply based on subscription tier

### Language Support

**Best performance in:**
- English
- Spanish (Mexico)
- Japanese
- Mandarin Chinese
- Hindi

Other languages supported but may have reduced quality.

### Content Restrictions

**Prohibited Content:**
- Depictions of real people without consent (especially children)
- Copyrighted characters or brands
- Explicit or adult content
- Violent or harmful content
- Deceptive content (deepfakes, misinformation)

**Regional Restrictions:**
- Children's image uploads restricted in EEA, Switzerland, and UK
- Some features may be region-specific

### Quality Considerations

**Works Best For:**
- Clear, descriptive prompts
- Natural language instructions
- Iterative refinement
- Compositional tasks

**May Struggle With:**
- Extremely complex scenes with many subjects
- Highly specific technical diagrams without context
- Unusual perspective or impossible physics
- Very fine text in small areas (improved in Pro)

### Comparison: Nano Banana vs. Imagen

When to use **Nano Banana/Pro**:
- Conversational, iterative editing
- Multi-image composition
- Character consistency
- World knowledge integration
- Quick prototyping

When to use **Imagen** (Google's specialized image model):
- Maximum photorealism requirements
- Precise typography needs
- Specialized photography tasks

---

## Use Cases

### 1. Marketing & Advertising

**Social Media Content:**
```python
response = pro_model.generate_content([
    "Create an Instagram post (1:1) for a tech startup launch, featuring a nano banana icon with circuit patterns, gradient background (purple to blue), modern typography saying 'Innovation at Scale', professional design, 2K resolution"
])
```

**Product Mockups:**
```python
response = pro_model.generate_content([
    product_image,
    "Place this product in a luxurious lifestyle setting, natural lighting, shallow depth of field, magazine quality photography, 16:9 format, 4K resolution"
])
```

**Ad Campaigns:**
```python
response = pro_model.generate_content([
    "Design a billboard advertisement (horizontal) showing the concept of nanotechnology making big impact, dramatic lighting, bold typography, eye-catching colors, photorealistic style"
])
```

### 2. Education & Training

**Diagrams & Infographics:**
```python
response = pro_model.generate_content([
    "Create an educational diagram explaining how nanotechnology works, showing atoms and molecules with clear labels, colorful and engaging illustration style, suitable for high school students, 16:9 format"
])
```

**Study Materials:**
```python
response = pro_model.generate_content([
    textbook_page,
    "Transform this text into a visual flowchart with icons and color coding, modern educational design, clear hierarchy, 2K resolution"
])
```

### 3. Design & Prototyping

**Logo Design:**
```python
response = model.generate_content([
    "Design a minimal modern logo for 'NanoLabs', incorporating a banana element, suitable for tech startup, vector style clarity, single color version available"
])
```

**UI Mockups:**
```python
response = pro_model.generate_content([
    "Create a mobile app splash screen featuring a nano banana mascot, modern gradient background, app name 'NanoBanana', clean UI design, 9:16 vertical format"
])
```

### 4. Content Creation

**Blog Headers:**
```python
response = model.generate_content([
    "Create a blog header image about nanotechnology breakthroughs, abstract scientific imagery, professional and modern, 21:9 ultra-wide format, leave center clear for text overlay"
])
```

**YouTube Thumbnails:**
```python
response = model.generate_content([
    "Design a YouTube thumbnail about nano science, bright colors, eye-catching, include space for title text, 16:9 format, high contrast for visibility"
])
```

### 5. E-commerce

**Product Photography Enhancement:**
```python
response = pro_model.generate_content([
    product_photo,
    "Enhance this product photo with professional studio lighting, white background, subtle shadows, commercial photography quality, remove any imperfections, 4K resolution"
])
```

**Lifestyle Shots:**
```python
response = pro_model.generate_content([
    product_image,
    lifestyle_setting,
    "Place this product naturally into the lifestyle scene, maintain realistic lighting and perspective, magazine quality, 4K resolution"
])
```

### 6. Real Estate

**Property Cards:**
```python
response = pro_model.generate_content([
    property_photo,
    "Create a professional real estate listing card with this property photo, modern design layout, include space for property details, elegant typography, 3:4 vertical format"
])
```

**Virtual Staging:**
```python
response = pro_model.generate_content([
    empty_room,
    "Add modern furniture and decor to this empty room, contemporary style, natural lighting, realistic placement and scale, 16:9 format"
])
```

### 7. Character Design & Storytelling

**Character Consistency:**
```python
# Create base character
response1 = pro_model.generate_content([
    "Design a friendly robot character mascot for a nano tech company, cute and approachable, modern style, full body view"
])

# Use in multiple contexts
response2 = pro_model.generate_content([
    response1_image,
    "Show this same character in these three scenarios: 1) in a laboratory, 2) helping students, 3) in space. Maintain exact appearance and personality across all scenes, 16:9 format, 2K resolution"
])
```

**Storyboards:**
```python
response = pro_model.generate_content([
    "Create a 6-panel storyboard for a science video about nano bananas: Panel 1 - regular banana, Panel 2 - lab equipment, Panel 3 - shrinking process, Panel 4 - microscopic view, Panel 5 - applications, Panel 6 - future possibilities. Consistent art style, clear progression"
])
```

### 8. Presentations & Reports

**Presentation Backgrounds:**
```python
response = pro_model.generate_content([
    "Create a professional presentation background for a tech conference, abstract nano-scale particles pattern, corporate blue and white colors, minimalist design, leave center area clear for content, 16:9 format, 4K resolution"
])
```

**Data Visualizations:**
```python
response = pro_model.generate_content([
    "Transform this data into an engaging infographic: [data summary]. Use charts, icons, and color coding. Modern flat design style, professional business presentation quality, 16:9 format"
])
```

### 9. Personal Projects

**Custom Artwork:**
```python
response = model.generate_content([
    "Create a whimsical illustration of a nano banana character going on an adventure through a microscopic world, children's book style, warm colors, friendly and imaginative"
])
```

**Photo Restoration:**
```python
response = model.generate_content([
    old_photo,
    "Restore this old photograph, fix scratches and damage, enhance clarity and colors, maintain the original vintage feel"
])
```

---

## Quick Reference

### Model Comparison

| Feature | Nano Banana | Nano Banana Pro |
|---------|-------------|-----------------|
| **Model ID** | `gemini-2.5-flash-image` | `gemini-3-pro-image` |
| **Launch Date** | August 2025 | November 2025 |
| **Max Resolution** | 1024×1024px | Up to 4K |
| **Aspect Ratios** | 1:1 to 21:9 | 16:9 to 9:16+ |
| **Max Input Images** | 3 recommended | Up to 14 |
| **Character Consistency** | 1-2 people | Up to 5 people |
| **Localized Editing** | Basic | Advanced |
| **Text Rendering** | Good | Excellent (multilingual) |
| **Camera Controls** | Basic | Professional |
| **Lighting Controls** | Basic | Advanced |
| **Infographics** | Basic | Advanced with real-time data |
| **Watermark Removal** | No | Yes (Ultra subscribers) |
| **Best For** | Quick generation, mobile | Professional, print, marketing |

### Common Prompt Patterns

**Product Photography:**
```
"Product photography of [product], [lens specs], [lighting setup], [background], [style notes], [aspect ratio], [resolution]"
```

**Character/Mascot:**
```
"Design a [character type] for [purpose], [style], [mood/personality], [color scheme], [perspective]"
```

**Marketing Material:**
```
"Create a [format] for [purpose], featuring [main elements], [style], [color scheme], [typography notes], [aspect ratio], [resolution]"
```

**Photo Enhancement:**
```
"[Action] this photo: [specific changes], [lighting adjustments], [style notes], [quality requirements]"
```

**Infographic:**
```
"Create an infographic showing [topic], include [key elements], [design style], [color scheme], [target audience], [format]"
```

### API Quick Reference

**Initialize:**
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
```

**Generate:**
```python
response = model.generate_content([prompt])
```

**Edit:**
```python
response = model.generate_content([image_data, edit_prompt])
```

**Compose:**
```python
response = model.generate_content([image1, image2, image3, composition_prompt])
```

**Save:**
```python
import base64
output = base64.b64decode(response.parts[0].inline_data.data)
with open('output.png', 'wb') as f:
    f.write(output)
```

---

## Additional Resources

### Official Documentation
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google DeepMind: Gemini Models](https://deepmind.google/models/gemini-image/)

### Community Resources
- [LM Arena Benchmarks](https://lmarena.ai/)
- Google Gemini Community Forums

### Related Tools
- **NotebookLM**: AI-powered note-taking with Nano Banana Pro integration
- **Google Workspace**: Slides and Vids with image generation
- **Google Ads**: Campaign creative generation

---

## Conclusion

Nano Banana and Nano Banana Pro represent the cutting edge of conversational AI image generation and editing. By leveraging Gemini's deep language understanding and world knowledge, these models go beyond simple text-to-image generation to enable truly intelligent, contextual image creation.

**Key Takeaways:**

1. **Use natural language** - Describe what you want narratively, not with keywords
2. **Iterate conversationally** - Refine through multiple turns rather than perfecting a single prompt
3. **Be specific about purpose** - Context helps the model make better decisions
4. **Choose the right model** - Standard for speed and cost, Pro for quality and professional work
5. **Leverage Gemini's knowledge** - The model understands context, current events, and complex concepts

Whether you're creating marketing materials, educational content, product mockups, or personal art, Nano Banana provides an intuitive, powerful interface for image generation that understands what you mean, not just what you say.

Start experimenting in the Gemini app today, or integrate the API into your workflows for automated image generation at scale. With Nano Banana Pro now available with 4K output, professional controls, and advanced composition capabilities, there's never been a better time to explore AI-powered image creation. 🍌

---

*Last Updated: November 20, 2025*
*Document Version: 1.0*
