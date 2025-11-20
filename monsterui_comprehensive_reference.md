# MonsterUI Comprehensive Reference Guide

> **For Offline LLM Development Use** - Complete documentation for building beautiful FastHTML UIs with Tailwind CSS

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Theme System](#theme-system)
5. [Typography Components](#typography-components)
6. [Layout & Containers](#layout--containers)
7. [Form Components](#form-components)
8. [Navigation Components](#navigation-components)
9. [Data Display](#data-display)
10. [Interactive Components](#interactive-components)
11. [DaisyUI Components](#daisyui-components)
12. [Utilities & Helpers](#utilities--helpers)
13. [Complete Examples](#complete-examples)
14. [Best Practices](#best-practices)

---

## Overview

**MonsterUI** is a Python UI framework built on FastHTML that enables developers to create beautiful web interfaces using Tailwind CSS with minimal code. It's specifically designed for data scientists, ML engineers, and developers who want to rapidly prototype web applications without traditional frontend complexity.

### Key Features

- **No CSS Required**: Pre-styled components using Tailwind CSS
- **Python-First**: Build entire UIs in pure Python
- **FastHTML Integration**: Seamless integration with FastHTML applications
- **Rich Component Library**: Comprehensive set of UI components
- **Responsive by Default**: Mobile-first responsive design
- **Theme Support**: 12 built-in color themes
- **Advanced Features**: Markdown rendering, syntax highlighting, LaTeX support

### Core Libraries Integrated

MonsterUI combines several powerful open-source projects:

- **FrankenUI**: Tailwind-based component library (framework-free)
- **DaisyUI**: Additional styling utilities and components
- **Mistletoe**: Python markdown processing
- **HighlightJS**: Syntax highlighting for code blocks
- **KaTeX**: Mathematical notation rendering
- **Lucide Icons**: Beautiful icon library
- **ApexCharts**: Data visualization

---

## Installation & Setup

### Installation

```bash
pip install MonsterUI
```

### Minimal Example

```python
from fasthtml.common import *
from monsterui.all import *

# Create theme headers
hdrs = Theme.blue.headers()

# Create FastHTML app
app, rt = fast_app(hdrs=hdrs)

@rt("/")
def index():
    return Titled("Your First App",
        Card(
            H1("Welcome to MonsterUI!"),
            P("Building beautiful UIs with Python")
        )
    )

serve()
```

### Theme Configuration

```python
from monsterui.all import *

# Choose from 12 color themes
themes = [
    Theme.slate, Theme.stone, Theme.gray, Theme.neutral,
    Theme.red, Theme.rose, Theme.orange, Theme.green,
    Theme.blue, Theme.yellow, Theme.violet, Theme.zinc
]

# Basic headers
hdrs = Theme.blue.headers()

# With optional features
hdrs = Theme.blue.headers(
    katex=True,          # Enable LaTeX math rendering
    highlightjs=True,    # Enable code syntax highlighting
    daisy=True,          # Enable DaisyUI components (default: True)
    fontawesome=True     # Enable FontAwesome icons
)

app, rt = fast_app(hdrs=hdrs)
```

### Using Local Files vs CDN

```python
# CDN (default - faster, no downloads)
hdrs = Theme.blue.headers()

# Local files (for offline use)
hdrs = Theme.blue.headers(use_local=True)
```

---

## Core Concepts

### Module Organization

MonsterUI is organized into several modules:

- **monsterui.core**: Theme system and foundations
- **monsterui.franken**: Main UI components (FrankenUI-based)
- **monsterui.daisy**: DaisyUI-specific components
- **monsterui.foundations**: Utility functions and helpers

### Import Strategy

```python
# Import everything (recommended for quick start)
from monsterui.all import *

# Import specific modules
from monsterui.core import Theme
from monsterui.franken import Card, Button, NavBar
from monsterui.daisy import Alert, Loading, Steps

# Selective imports for production
from monsterui.franken import (
    H1, H2, P,              # Typography
    Card, Container,         # Layout
    Button, Form, Input,     # Forms
    Table, TableFromDicts    # Data display
)
```

### Component Philosophy

MonsterUI components are:
1. **Python functions** that return FastHTML/FT objects
2. **Pre-styled** with Tailwind CSS classes
3. **Composable** - can be nested and combined
4. **Type-safe** with enums for style variants

---

## Theme System

### Theme Colors

```python
from monsterui.core import Theme

# Available themes
Theme.slate     # Cool gray
Theme.stone     # Warm gray
Theme.gray      # Neutral gray
Theme.neutral   # Pure gray
Theme.red       # Vibrant red
Theme.rose      # Pink-red
Theme.orange    # Bright orange
Theme.green     # Fresh green
Theme.blue      # Classic blue (default)
Theme.yellow    # Sunny yellow
Theme.violet    # Purple-violet
Theme.zinc      # Industrial gray
```

### Theme Components

```python
# Theme configuration
class Theme(Enum):
    # Color options
    slate = "slate"
    blue = "blue"
    # ... etc

    def headers(
        self,
        katex: bool = False,        # Math rendering
        highlightjs: bool = False,  # Code highlighting
        daisy: bool = True,         # DaisyUI components
        use_local: bool = False     # Use local files
    ):
        """Generate headers for theme"""
        pass
```

### Theme Customization

```python
# Custom CSS overrides
custom_style = Style("""
    :root {
        --primary: #007bff;
        --secondary: #6c757d;
    }
    .custom-btn {
        background: var(--primary);
        color: white;
    }
""")

hdrs = Theme.blue.headers()
app, rt = fast_app(hdrs=(*hdrs, custom_style))
```

### Theme Picker Component

```python
from monsterui.franken import ThemePicker

@rt("/")
def index():
    return Titled("Theme Demo",
        ThemePicker(),  # User can switch themes
        H1("This title will change with theme"),
        P("Content adapts to selected theme")
    )
```

### Dark Mode

MonsterUI uses Tailwind's selector-based dark mode with localStorage persistence:

```python
# Dark mode is automatic based on:
# 1. User's system preference
# 2. User's theme picker selection (if used)
# 3. localStorage persistence

# Components automatically support dark mode
Card(
    H2("This card"),
    P("Automatically adapts to dark mode")
)
```

---

## Typography Components

### Headings

```python
from monsterui.franken import H1, H2, H3, H4, H5, H6

# Basic headings
H1("Main Title")
H2("Section Title")
H3("Subsection")
H4("Minor Heading")
H5("Small Heading")
H6("Tiny Heading")

# Headings are pre-styled with appropriate:
# - Font sizes
# - Font weights
# - Margins
# - Line heights
```

### Text Elements

```python
from monsterui.franken import P, Span, Strong, Em, I, Small

# Paragraph
P("This is a paragraph with proper spacing and line height.")

# Inline text
Span("Inline text")

# Emphasis
Strong("Bold text")      # <strong>
Em("Italic text")        # <em>
I("Also italic")         # <i>

# Small text
Small("Fine print or metadata")
```

### Specialized Text

```python
from monsterui.franken import Mark, Del, Ins, Sub, Sup
from monsterui.franken import Kbd, Samp, Var, Abbr, Dfn

# Highlighted text
Mark("Important highlighted text")

# Deleted/Inserted (for showing edits)
Del("Removed text")
Ins("Added text")

# Subscript/Superscript
P("H", Sub("2"), "O")           # H₂O
P("E = mc", Sup("2"))           # E = mc²

# Code and keyboard
Kbd("Ctrl+C")                   # Keyboard shortcut
Samp("Sample output")           # Sample program output
Var("variable_name")            # Variable name

# Definitions
Abbr("HTML", title="HyperText Markup Language")
Dfn("Responsive Design")
```

### Text Styling with TextT Enum

```python
from monsterui.franken import TextT

# Size variants
TextT.xs     # Extra small
TextT.sm     # Small
TextT.base   # Base size
TextT.lg     # Large
TextT.xl     # Extra large

# Weight variants
TextT.light      # Light weight
TextT.normal     # Normal weight
TextT.medium     # Medium weight
TextT.semibold   # Semi-bold
TextT.bold       # Bold
TextT.extrabold  # Extra bold

# Alignment
TextT.left       # Left aligned
TextT.center     # Center aligned
TextT.right      # Right aligned

# Semantic colors
TextT.primary    # Primary color
TextT.secondary  # Secondary color
TextT.success    # Success (green)
TextT.warning    # Warning (yellow)
TextT.error      # Error (red)

# Usage with components
P("Styled text", cls=str(TextT.lg + TextT.bold + TextT.center))
```

### Code Blocks

```python
from monsterui.franken import CodeSpan, CodeBlock

# Inline code
P("Use ", CodeSpan("print()"), " for output")

# Code block (with syntax highlighting if enabled)
CodeBlock("""
def hello_world():
    print("Hello, World!")

hello_world()
""", language="python")
```

---

## Layout & Containers

### Container

```python
from monsterui.franken import Container

# Responsive container with max-width
Container(
    H1("Welcome"),
    P("This content is contained and centered")
)

# Container size variants
Container.xs       # Extra small max-width
Container.sm       # Small max-width
Container.md       # Medium max-width (default)
Container.lg       # Large max-width
Container.xl       # Extra large max-width
Container.expand   # Full width

# Usage
Container(H1("Title"), size=Container.lg)
```

### Section

```python
from monsterui.franken import Section

# Styled section with margin control
Section(
    H2("Section Title"),
    P("Section content with proper spacing")
)

# Custom margin
Section(
    H2("Compact Section"),
    P("Less margin"),
    margin="small"
)
```

### Article

```python
from monsterui.franken import Article, ArticleTitle, ArticleMeta

# Blog-style article layout
Article(
    ArticleTitle("My Blog Post"),
    ArticleMeta("Published on Jan 20, 2025 by Author"),
    P("Article content here..."),
    P("More paragraphs...")
)
```

### Grid Layout

```python
from monsterui.franken import Grid

# Responsive grid (auto-adjusts columns)
Grid(
    Div("Column 1"),
    Div("Column 2"),
    Div("Column 3"),
    Div("Column 4")
)

# Grid with specific columns
Grid(
    Div("Item 1"),
    Div("Item 2"),
    Div("Item 3"),
    cols=3  # Force 3 columns
)

# Responsive grid with breakpoints
Grid(
    Div("Card 1"),
    Div("Card 2"),
    Div("Card 3"),
    cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
)
```

### Flexbox Helpers

```python
from monsterui.franken import (
    DivCentered,      # Center content
    DivFullySpaced,   # Space-between
    DivLAligned,      # Left aligned
    DivRAligned,      # Right aligned
    DivVStacked,      # Vertical stack
    DivHStacked,      # Horizontal stack
    FlexT             # Flex type enum
)

# Centered content
DivCentered(
    H1("Centered"),
    P("Both horizontally and vertically")
)

# Horizontal stack with spacing
DivHStacked(
    Button("Cancel"),
    Button("Save")
)

# Vertical stack
DivVStacked(
    P("Item 1"),
    P("Item 2"),
    P("Item 3")
)

# Full spacing (space-between)
DivFullySpaced(
    P("Left side"),
    P("Right side")
)

# FlexT enum for custom flex layouts
FlexT.row           # Flex row
FlexT.col           # Flex column
FlexT.wrap          # Flex wrap
FlexT.center        # Center items
FlexT.between       # Space between
FlexT.around        # Space around
FlexT.start         # Align start
FlexT.end           # Align end
```

---

## Form Components

### Basic Inputs

```python
from monsterui.franken import Input, TextArea, Form, Button

# Text input
Input(
    type="text",
    name="username",
    placeholder="Enter username",
    required=True
)

# Password input
Input(
    type="password",
    name="password",
    placeholder="Enter password"
)

# Email input
Input(
    type="email",
    name="email",
    placeholder="user@example.com"
)

# Number input
Input(
    type="number",
    name="age",
    min=0,
    max=120
)

# Textarea
TextArea(
    name="message",
    placeholder="Enter your message",
    rows=5
)
```

### Label-Paired Inputs

MonsterUI provides convenient label-input combinations:

```python
from monsterui.franken import (
    LabelInput,
    LabelTextArea,
    LabelSelect,
    LabelCheckboxX,
    LabelRadio,
    LabelRange
)

# Input with label (automatically linked)
LabelInput(
    "Username:",
    type="text",
    name="username",
    placeholder="Enter username"
)

# Textarea with label
LabelTextArea(
    "Message:",
    name="message",
    rows=4
)

# Select with label
LabelSelect(
    "Country:",
    name="country",
    options=["USA", "UK", "Canada", "Australia"]
)

# Checkbox with label
LabelCheckboxX(
    "I agree to terms",
    name="agree",
    value="yes"
)

# Radio with label
LabelRadio(
    "Option 1",
    name="choice",
    value="opt1"
)

# Range slider with label
LabelRange(
    "Volume:",
    name="volume",
    min=0,
    max=100,
    value=50
)
```

### Advanced Form Inputs

```python
from monsterui.franken import (
    CheckboxX,
    Radio,
    Range,
    Switch,
    Upload,
    UploadZone
)

# Styled checkbox
CheckboxX(
    name="subscribe",
    value="yes",
    checked=True
)

# Radio button
Radio(
    name="plan",
    value="premium",
    checked=True
)

# Range slider
Range(
    name="rating",
    min=1,
    max=10,
    value=5,
    step=1
)

# Toggle switch
Switch(
    name="notifications",
    checked=True
)

# File upload
Upload(
    name="avatar",
    accept="image/*"
)

# Drag-and-drop upload zone
UploadZone(
    name="documents",
    accept=".pdf,.doc,.docx",
    multiple=True
)
```

### Select and Options

```python
from monsterui.franken import Select, Options

# Basic select
Select(
    Options(["Option 1", "Option 2", "Option 3"]),
    name="choice"
)

# Select with values different from labels
Select(
    Option("Select...", value="", disabled=True, selected=True),
    Option("Small", value="sm"),
    Option("Medium", value="md"),
    Option("Large", value="lg"),
    name="size"
)

# Select with search (if enabled in headers)
Select(
    Options(["Apple", "Banana", "Cherry", "Date", "Fig"]),
    name="fruit",
    searchable=True
)
```

### Form Structure

```python
from monsterui.franken import Form, Fieldset, Legend

# Basic form
Form(
    LabelInput("Name:", name="name"),
    LabelInput("Email:", name="email", type="email"),
    Button("Submit", type="submit"),
    method="post",
    action="/submit"
)

# Form with fieldsets
Form(
    Fieldset(
        Legend("Personal Information"),
        LabelInput("First Name:", name="first_name"),
        LabelInput("Last Name:", name="last_name"),
        LabelInput("Email:", name="email", type="email")
    ),
    Fieldset(
        Legend("Address"),
        LabelInput("Street:", name="street"),
        LabelInput("City:", name="city"),
        LabelInput("ZIP:", name="zip")
    ),
    Button("Submit", type="submit"),
    method="post"
)
```

### Buttons

```python
from monsterui.franken import Button, ButtonT

# Basic button
Button("Click Me")

# Button types/variants
Button("Default", cls=str(ButtonT.default))
Button("Primary", cls=str(ButtonT.primary))
Button("Secondary", cls=str(ButtonT.secondary))
Button("Destructive", cls=str(ButtonT.destructive))
Button("Ghost", cls=str(ButtonT.ghost))
Button("Link", cls=str(ButtonT.link))
Button("Text", cls=str(ButtonT.text))

# Button sizes
Button("Extra Small", cls=str(ButtonT.xs))
Button("Small", cls=str(ButtonT.sm))
Button("Medium")  # Default
Button("Large", cls=str(ButtonT.lg))
Button("Extra Large", cls=str(ButtonT.xl))

# Icon button
Button("⚙", cls=str(ButtonT.icon))

# Button with HTMX
Button(
    "Load More",
    hx_get="/load-more",
    hx_target="#content",
    cls=str(ButtonT.primary)
)
```

---

## Navigation Components

### NavBar

```python
from monsterui.franken import NavBar

# Responsive navigation bar (collapses on mobile)
NavBar(
    # Logo/Brand
    A("MyApp", href="/", cls="navbar-brand"),

    # Navigation links
    A("Home", href="/"),
    A("About", href="/about"),
    A("Contact", href="/contact"),

    # Right-aligned items
    A("Login", href="/login", cls="ml-auto")
)

# The NavBar automatically:
# - Creates a hamburger menu on mobile
# - Handles collapse/expand behavior
# - Applies proper styling
```

### NavContainer (Sidebar)

```python
from monsterui.franken import (
    NavContainer,
    NavParentLi,
    NavDividerLi,
    NavHeaderLi,
    NavCloseLi
)

# Sidebar navigation
NavContainer(
    NavHeaderLi("Main Menu"),

    NavParentLi(
        "Dashboard",
        href="/dashboard",
        icon="📊"
    ),

    NavParentLi(
        "Users",
        href="/users",
        icon="👥"
    ),

    NavDividerLi(),  # Horizontal divider

    NavHeaderLi("Settings"),

    NavParentLi(
        "Profile",
        href="/profile",
        icon="⚙"
    ),

    NavCloseLi()  # Close button for mobile
)
```

### Tabs

```python
from monsterui.franken import TabContainer

# Tab navigation
TabContainer(
    # Tab buttons
    ("Overview", "#overview"),
    ("Details", "#details"),
    ("Settings", "#settings"),

    # Tab content
    Div(
        P("Overview content"),
        id="overview"
    ),
    Div(
        P("Details content"),
        id="details",
        style="display: none;"
    ),
    Div(
        P("Settings content"),
        id="settings",
        style="display: none;"
    )
)
```

### Dropdown Navigation

```python
from monsterui.franken import DropDownNavContainer

# Dropdown in navigation
NavBar(
    A("Home", href="/"),

    DropDownNavContainer(
        "Products",  # Dropdown trigger
        A("Product 1", href="/product/1"),
        A("Product 2", href="/product/2"),
        A("Product 3", href="/product/3")
    ),

    A("About", href="/about")
)
```

### Scrollspy

```python
from monsterui.franken import ScrollspyT

# Scrollspy navigation (highlights current section)
Nav(
    A("Section 1", href="#section1"),
    A("Section 2", href="#section2"),
    A("Section 3", href="#section3"),
    data_scrollspy=str(ScrollspyT.underline)  # or ScrollspyT.bold
)

# Content sections
Article(
    Section(H2("Section 1"), P("Content..."), id="section1"),
    Section(H2("Section 2"), P("Content..."), id="section2"),
    Section(H2("Section 3"), P("Content..."), id="section3")
)
```

---

## Data Display

### Cards

```python
from monsterui.franken import Card, CardHeader, CardBody, CardFooter, CardT

# Basic card
Card(
    H3("Card Title"),
    P("Card content goes here"),
    Button("Action")
)

# Card with explicit sections
Card(
    CardHeader(
        H3("Header")
    ),
    CardBody(
        P("Main content")
    ),
    CardFooter(
        Button("Cancel"),
        Button("Save")
    )
)

# Card variants
Card("Default card", cls=str(CardT.default))
Card("Primary card", cls=str(CardT.primary))
Card("Secondary card", cls=str(CardT.secondary))
Card("Destructive card", cls=str(CardT.destructive))
Card("Hover effect card", cls=str(CardT.hover))
```

### Tables

```python
from monsterui.franken import Table, TableFromDicts, TableFromLists

# Manual table
Table(
    Thead(
        Tr(
            Th("Name"),
            Th("Age"),
            Th("Email")
        )
    ),
    Tbody(
        Tr(
            Td("Alice"),
            Td("30"),
            Td("alice@example.com")
        ),
        Tr(
            Td("Bob"),
            Td("25"),
            Td("bob@example.com")
        )
    )
)

# Table from list of dicts (automatic generation)
users = [
    {"name": "Alice", "age": 30, "email": "alice@example.com"},
    {"name": "Bob", "age": 25, "email": "bob@example.com"},
    {"name": "Charlie", "age": 35, "email": "charlie@example.com"}
]

TableFromDicts(
    users,
    sortable=True  # Enable column sorting
)

# Table from lists
headers = ["Name", "Age", "Email"]
rows = [
    ["Alice", 30, "alice@example.com"],
    ["Bob", 25, "bob@example.com"],
    ["Charlie", 35, "charlie@example.com"]
]

TableFromLists(
    headers,
    rows,
    sortable=True
)

# Custom cell renderer
def render_email(value):
    return A(value, href=f"mailto:{value}")

TableFromDicts(
    users,
    cell_renderers={"email": render_email}
)
```

### Lists

```python
from fasthtml.common import Ul, Ol, Li

# Unordered list (styled by MonsterUI)
Ul(
    Li("First item"),
    Li("Second item"),
    Li("Third item")
)

# Ordered list
Ol(
    Li("Step 1"),
    Li("Step 2"),
    Li("Step 3")
)

# Nested lists
Ul(
    Li("Main item 1",
        Ul(
            Li("Sub-item 1.1"),
            Li("Sub-item 1.2")
        )
    ),
    Li("Main item 2")
)
```

---

## Interactive Components

### Modals

```python
from monsterui.franken import (
    Modal,
    ModalContainer,
    ModalDialog,
    ModalHeader,
    ModalBody,
    ModalFooter,
    ModalTitle,
    ModalCloseButton
)

# Complete modal
Modal(
    # Trigger button
    Button("Open Modal", data_modal_open="my-modal"),

    # Modal structure
    ModalContainer(
        ModalDialog(
            ModalHeader(
                ModalTitle("Confirm Action"),
                ModalCloseButton()
            ),
            ModalBody(
                P("Are you sure you want to continue?")
            ),
            ModalFooter(
                Button("Cancel", data_modal_close="my-modal"),
                Button("Confirm", cls=str(ButtonT.primary))
            )
        ),
        id="my-modal"
    )
)

# Simple modal helper
Modal(
    Button("Open"),
    ModalContainer(
        ModalDialog(
            H3("Title"),
            P("Content"),
            Button("Close", data_modal_close="modal-1")
        ),
        id="modal-1"
    )
)
```

### Accordions

```python
from monsterui.franken import Accordion, AccordionItem

# Accordion (collapsible sections)
Accordion(
    AccordionItem(
        "First Section",  # Title
        P("Content of first section")  # Content
    ),
    AccordionItem(
        "Second Section",
        P("Content of second section")
    ),
    AccordionItem(
        "Third Section",
        P("Content of third section")
    )
)

# Accordion with custom content
Accordion(
    AccordionItem(
        "User Profile",
        Div(
            P("Name: John Doe"),
            P("Email: john@example.com"),
            Button("Edit Profile")
        )
    ),
    AccordionItem(
        "Settings",
        Form(
            LabelCheckboxX("Email notifications"),
            LabelCheckboxX("Push notifications"),
            Button("Save")
        )
    )
)
```

### Details/Summary

```python
from monsterui.franken import Details, Summary

# Native HTML details (styled)
Details(
    Summary("Click to expand"),
    P("Hidden content revealed!"),
    P("More details here...")
)

# Multiple details
Div(
    Details(
        Summary("FAQ 1: What is MonsterUI?"),
        P("MonsterUI is a UI framework for FastHTML...")
    ),
    Details(
        Summary("FAQ 2: How do I install it?"),
        P("Run: pip install MonsterUI")
    ),
    Details(
        Summary("FAQ 3: Is it free?"),
        P("Yes, it's open source!")
    )
)
```

### Progress Bars

```python
from monsterui.franken import Progress

# Basic progress bar
Progress(value=75, max=100)

# Labeled progress
Div(
    Label("Upload Progress"),
    Progress(value=45, max=100),
    P("45% complete")
)

# Dynamic progress with HTMX
Progress(
    value=0,
    max=100,
    id="upload-progress",
    hx_get="/progress",
    hx_trigger="every 1s",
    hx_target="this",
    hx_swap="outerHTML"
)
```

### Sliders (Carousels)

```python
from monsterui.franken import Slider, SliderNav

# Image slider/carousel
Slider(
    Div(Img(src="/image1.jpg"), cls="slide"),
    Div(Img(src="/image2.jpg"), cls="slide"),
    Div(Img(src="/image3.jpg"), cls="slide"),

    # Navigation
    SliderNav()
)

# Content slider
Slider(
    Card(H3("Slide 1"), P("Content...")),
    Card(H3("Slide 2"), P("More content...")),
    Card(H3("Slide 3"), P("Even more..."))
)
```

### Lightbox (Image Gallery)

```python
from monsterui.franken import LightboxContainer, LightboxItem

# Image gallery with lightbox
LightboxContainer(
    LightboxItem(
        Img(src="/thumb1.jpg", alt="Image 1"),
        full_src="/full1.jpg"
    ),
    LightboxItem(
        Img(src="/thumb2.jpg", alt="Image 2"),
        full_src="/full2.jpg"
    ),
    LightboxItem(
        Img(src="/thumb3.jpg", alt="Image 3"),
        full_src="/full3.jpg"
    )
)
```

---

## DaisyUI Components

### Alerts

```python
from monsterui.daisy import Alert, AlertT

# Alert variants
Alert("This is an info alert", type=AlertT.info)
Alert("Success! Operation completed", type=AlertT.success)
Alert("Warning: Please check your input", type=AlertT.warning)
Alert("Error: Something went wrong", type=AlertT.error)

# Alert with icon
Alert(
    "✓ Successfully saved!",
    type=AlertT.success
)

# Alert with actions
Alert(
    "New update available",
    Button("Update Now", cls=str(ButtonT.sm)),
    Button("Later", cls=str(ButtonT.ghost)),
    type=AlertT.info
)
```

### Loading Indicators

```python
from monsterui.daisy import Loading, LoaderButton

# Loading animations
Loading(type="spinner")
Loading(type="dots")
Loading(type="ring")
Loading(type="ball")
Loading(type="bars")
Loading(type="infinity")

# Size variants
Loading(type="spinner", size="xs")
Loading(type="spinner", size="sm")
Loading(type="spinner", size="md")
Loading(type="spinner", size="lg")

# Button with loading indicator
LoaderButton(
    "Submit",
    hx_post="/submit",
    hx_indicator="#spinner"
)

Div(Loading(type="spinner"), id="spinner", cls="htmx-indicator")
```

### Steps

```python
from monsterui.daisy import Steps, LiStep

# Progress steps
Steps(
    LiStep("Account", completed=True),
    LiStep("Profile", active=True),
    LiStep("Confirm", completed=False)
)

# Vertical steps
Steps(
    LiStep("Step 1", completed=True),
    LiStep("Step 2", active=True),
    LiStep("Step 3"),
    vertical=True
)

# Steps with custom content
Steps(
    LiStep(
        Div(
            Strong("1. Register"),
            Small("Create your account")
        ),
        completed=True
    ),
    LiStep(
        Div(
            Strong("2. Verify"),
            Small("Check your email")
        ),
        active=True
    ),
    LiStep(
        Div(
            Strong("3. Complete"),
            Small("Finish setup")
        )
    )
)
```

### Toast Notifications

```python
from monsterui.daisy import Toast, ToastHT, ToastVT

# Toast positioning
# Horizontal: ToastHT.start, ToastHT.center, ToastHT.end
# Vertical: ToastVT.top, ToastVT.middle, ToastVT.bottom

# Top-right toast
Toast(
    Alert("Notification message", type=AlertT.info),
    horizontal=ToastHT.end,
    vertical=ToastVT.top
)

# Bottom-center toast
Toast(
    Alert("Action completed!", type=AlertT.success),
    horizontal=ToastHT.center,
    vertical=ToastVT.bottom
)

# Toast with HTMX (auto-appear)
Div(
    id="toast-container",
    hx_get="/check-notifications",
    hx_trigger="every 5s"
)
```

---

## Utilities & Helpers

### Icons

```python
from monsterui.franken import UkIcon, UkIconLink

# Lucide icons (if enabled)
UkIcon("home")
UkIcon("user")
UkIcon("settings")
UkIcon("search", size=24)

# Icon as link
UkIconLink(
    "external-link",
    href="https://example.com"
)

# Icon button
Button(
    UkIcon("trash"),
    "Delete",
    cls=str(ButtonT.destructive)
)
```

### Avatars

```python
from monsterui.franken import DiceBearAvatar

# Generate avatar from name
DiceBearAvatar(
    seed="John Doe",
    size=64
)

# Different styles
DiceBearAvatar(
    seed="user@example.com",
    style="avataaars",  # or "bottts", "identicon", etc.
    size=48
)
```

### Placeholder Images

```python
from monsterui.franken import PicSumImg, Placeholder

# Random placeholder image from Picsum
PicSumImg(
    width=800,
    height=600,
    id=237  # Specific image ID
)

# Random image
PicSumImg(width=400, height=300)

# Content placeholder
Placeholder(
    width="100%",
    height="200px",
    text="Loading..."
)
```

### Markdown Rendering

```python
from monsterui.franken import render_md

# Render markdown to HTML
markdown_text = """
# Hello World

This is **bold** and this is *italic*.

- Item 1
- Item 2
- Item 3

```python
print("Code block")
```
"""

@rt("/")
def index():
    return Titled("Markdown Demo",
        Div(
            render_md(markdown_text)
        )
    )

# Custom image handling
def custom_image_handler(src, alt):
    return Img(src=f"/images/{src}", alt=alt, cls="img-fluid")

render_md(
    markdown_text,
    image_handler=custom_image_handler
)
```

### Charts

```python
from monsterui.franken import ApexChart

# Line chart
ApexChart(
    chart_type="line",
    series=[{
        "name": "Sales",
        "data": [30, 40, 35, 50, 49, 60, 70]
    }],
    options={
        "xaxis": {
            "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
        }
    }
)

# Bar chart
ApexChart(
    chart_type="bar",
    series=[{
        "name": "Revenue",
        "data": [44, 55, 41, 64, 22, 43, 21]
    }],
    options={
        "chart": {"height": 350},
        "plotOptions": {
            "bar": {"horizontal": False}
        }
    }
)

# Pie chart
ApexChart(
    chart_type="pie",
    series=[44, 55, 13, 33],
    options={
        "labels": ["Team A", "Team B", "Team C", "Team D"]
    }
)
```

### Utility Functions

```python
from monsterui.foundations import stringify, VEnum

# Convert various types to FT-compatible strings
stringify("text")           # "text"
stringify(123)              # "123"
stringify(True)             # "true"
stringify([1, 2, 3])        # "[1, 2, 3]"

# VEnum: Enums with string concatenation
class MyStyles(VEnum):
    RED = "text-red-500"
    BOLD = "font-bold"
    LARGE = "text-xl"

# Combine enum values
cls = MyStyles.RED + MyStyles.BOLD + MyStyles.LARGE
# Result: "text-red-500 font-bold text-xl"

P("Styled text", cls=str(cls))
```

---

## Complete Examples

### Example 1: Landing Page

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt("/")
def index():
    return Titled("Welcome to MyApp",
        # Hero section
        Section(
            Container(
                DivCentered(
                    H1("Build Amazing Apps with Python", cls=str(TextT.xl)),
                    P("No JavaScript required. Just pure Python beauty."),
                    DivHStacked(
                        Button("Get Started", cls=str(ButtonT.primary)),
                        Button("Learn More", cls=str(ButtonT.ghost))
                    )
                ),
                cls="hero"
            ),
            style="padding: 4rem 0; text-align: center;"
        ),

        # Features section
        Section(
            Container(
                H2("Features", cls=str(TextT.lg)),
                Grid(
                    Card(
                        H3("🚀 Fast"),
                        P("Lightning-fast development with minimal code")
                    ),
                    Card(
                        H3("🎨 Beautiful"),
                        P("Pre-styled components with Tailwind CSS")
                    ),
                    Card(
                        H3("🐍 Python"),
                        P("100% Python - no context switching")
                    )
                )
            )
        ),

        # Footer
        Footer(
            Container(
                DivFullySpaced(
                    P("© 2025 MyApp"),
                    P(A("Docs", href="/docs"), " | ", A("GitHub", href="#"))
                )
            ),
            style="margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #eee;"
        )
    )

serve()
```

### Example 2: Dashboard

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.slate.headers(highlightjs=True))

@rt("/")
def dashboard(session):
    # Mock data
    stats = [
        {"label": "Users", "value": "1,234", "icon": "👥"},
        {"label": "Revenue", "value": "$45.2K", "icon": "💰"},
        {"label": "Orders", "value": "892", "icon": "📦"},
        {"label": "Growth", "value": "+12.5%", "icon": "📈"}
    ]

    recent_users = [
        {"name": "Alice Johnson", "email": "alice@example.com", "status": "active"},
        {"name": "Bob Smith", "email": "bob@example.com", "status": "active"},
        {"name": "Charlie Brown", "email": "charlie@example.com", "status": "inactive"}
    ]

    return Container(
        # Header
        DivFullySpaced(
            H1("Dashboard"),
            Button("Refresh", hx_get="/dashboard", hx_swap="outerHTML")
        ),

        # Stats grid
        Grid(
            *[
                Card(
                    Div(
                        Span(stat['icon'], style="font-size: 2rem;"),
                        Div(
                            H3(stat['value']),
                            P(stat['label'], cls=str(TextT.sm))
                        )
                    )
                )
                for stat in stats
            ]
        ),

        # Recent activity
        Section(
            H2("Recent Users"),
            TableFromDicts(
                recent_users,
                sortable=True
            )
        ),

        # Charts
        Section(
            H2("Analytics"),
            Grid(
                Card(
                    H3("Revenue Over Time"),
                    ApexChart(
                        chart_type="line",
                        series=[{"name": "Revenue", "data": [30, 40, 35, 50, 49, 60, 70]}],
                        options={
                            "xaxis": {"categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]}
                        }
                    )
                ),
                Card(
                    H3("User Distribution"),
                    ApexChart(
                        chart_type="pie",
                        series=[44, 55, 13],
                        options={"labels": ["Active", "Inactive", "Pending"]}
                    )
                ),
                cols=2
            )
        )
    )

serve()
```

### Example 3: Blog with Markdown

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.stone.headers(highlightjs=True, katex=True))

posts = [
    {
        "id": 1,
        "title": "Getting Started with MonsterUI",
        "date": "2025-01-15",
        "content": """
# Introduction

MonsterUI makes it easy to build **beautiful** web interfaces.

## Features

- 🎨 Pre-styled components
- 🐍 Pure Python
- ⚡ Lightning fast

```python
from monsterui.all import *

Card(H3("Hello"), P("World!"))
```

Try it yourself!
        """
    },
    {
        "id": 2,
        "title": "Advanced Techniques",
        "date": "2025-01-18",
        "content": """
# Advanced MonsterUI

Learn about advanced patterns...

## Math Support

Einstein's famous equation: $E = mc^2$

$$
\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
$$
        """
    }
]

@rt("/")
def index():
    return Container(
        Header(
            H1("My Technical Blog"),
            P("Python, Web Development, and More")
        ),

        # Post list
        Div(*[
            Card(
                ArticleTitle(A(post['title'], href=f"/post/{post['id']}")),
                ArticleMeta(post['date']),
                Div(render_md(post['content'][:100] + "...")),
                A("Read more →", href=f"/post/{post['id']}")
            )
            for post in posts
        ])
    )

@rt("/post/{pid}")
def post(pid: int):
    post = next((p for p in posts if p['id'] == pid), None)
    if not post:
        return Container(H1("404"), P("Post not found")), 404

    return Container(
        Article(
            H1(post['title']),
            Small(post['date']),
            Hr(),
            Div(render_md(post['content']))
        ),
        A("← Back to blog", href="/")
    )

serve()
```

### Example 4: Form with Validation

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt("/")
def index():
    return Container(
        Card(
            H2("Contact Us"),
            Form(
                LabelInput(
                    "Name:",
                    name="name",
                    required=True,
                    hx_post="/validate/name",
                    hx_trigger="blur",
                    hx_target="#name-error"
                ),
                Div(id="name-error"),

                LabelInput(
                    "Email:",
                    name="email",
                    type="email",
                    required=True,
                    hx_post="/validate/email",
                    hx_trigger="blur",
                    hx_target="#email-error"
                ),
                Div(id="email-error"),

                LabelTextArea(
                    "Message:",
                    name="message",
                    rows=5,
                    required=True
                ),

                DivHStacked(
                    Button("Cancel", cls=str(ButtonT.ghost)),
                    LoaderButton("Submit", cls=str(ButtonT.primary))
                ),

                hx_post="/submit",
                hx_target="#result"
            ),
            Div(id="result")
        )
    )

@rt("/validate/name")
def validate_name(name: str):
    if len(name) < 2:
        return Small("Name must be at least 2 characters", style="color: red;")
    return Small("✓ Valid", style="color: green;")

@rt("/validate/email")
def validate_email(email: str):
    if "@" not in email or "." not in email:
        return Small("Invalid email format", style="color: red;")
    return Small("✓ Valid", style="color: green;")

@rt("/submit")
def submit(name: str, email: str, message: str):
    # Process form
    return Alert(
        f"Thanks {name}! We'll contact you at {email}",
        type=AlertT.success
    )

serve()
```

---

## Best Practices

### 1. Component Organization

```python
# components.py - Reusable UI components
from monsterui.all import *

def UserCard(user):
    """Reusable user card component"""
    return Card(
        DivHStacked(
            DiceBearAvatar(seed=user['email'], size=48),
            Div(
                H3(user['name']),
                P(user['email'], cls=str(TextT.sm))
            )
        ),
        cls=str(CardT.hover)
    )

def StatCard(label, value, icon, trend=None):
    """Dashboard stat card"""
    return Card(
        DivHStacked(
            Span(icon, style="font-size: 2rem;"),
            Div(
                H2(value),
                P(label, cls=str(TextT.sm)),
                Small(trend, style="color: green;") if trend else None
            )
        )
    )

def PageLayout(title, *content):
    """Standard page layout"""
    return Container(
        Header(H1(title)),
        Main(*content),
        Footer(P("© 2025"), style="margin-top: 2rem;")
    )

# Usage in routes
@rt("/")
def index():
    return PageLayout(
        "Users",
        Grid(*[UserCard(user) for user in get_users()])
    )
```

### 2. Theming Strategy

```python
# config.py
from monsterui.core import Theme

# Centralize theme configuration
APP_THEME = Theme.blue

def get_headers():
    """Get app headers with consistent config"""
    return APP_THEME.headers(
        katex=True,
        highlightjs=True,
        daisy=True
    )

# app.py
from config import get_headers

app, rt = fast_app(hdrs=get_headers())
```

### 3. Form Patterns

```python
# Always use label-paired inputs for better UX
# GOOD:
Form(
    LabelInput("Username:", name="username"),
    LabelInput("Email:", type="email", name="email"),
    Button("Submit")
)

# AVOID (unless you have a reason):
Form(
    Input(name="username", placeholder="Username"),
    Input(name="email", placeholder="Email"),
    Button("Submit")
)

# Validate on blur for better UX
LabelInput(
    "Email:",
    name="email",
    hx_post="/validate",
    hx_trigger="blur",  # Validate when user leaves field
    hx_target="#error"
)
```

### 4. Responsive Design

```python
# Use Grid for responsive layouts
Grid(
    Card("Item 1"),
    Card("Item 2"),
    Card("Item 3"),
    Card("Item 4"),
    # Automatically responsive
)

# Custom responsive classes
Div(
    Card("Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols"),
    cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
)
```

### 5. Performance Tips

```python
# Lazy load images
Img(src="/placeholder.jpg", data_src="/actual.jpg", loading="lazy")

# Use HTMX for partial updates (faster than full page reloads)
Button(
    "Load More",
    hx_get="/more-items",
    hx_target="#items",
    hx_swap="beforeend"  # Append, don't replace
)

# Minimize unnecessary nesting
# GOOD:
Container(H1("Title"), P("Content"))

# AVOID:
Container(Div(Div(Div(H1("Title"), P("Content")))))
```

### 6. Accessibility

```python
# Always provide alt text for images
Img(src="/photo.jpg", alt="Description of photo")

# Use semantic HTML
Article(  # Not Div
    H1("Title"),
    P("Content")
)

# Label form inputs properly
LabelInput("Username:", name="username")  # Properly linked

# Provide ARIA labels when needed
Button(
    UkIcon("search"),
    aria_label="Search"
)
```

### 7. Error Handling

```python
@rt("/form")
def post(name: str = "", email: str = ""):
    errors = []

    if not name:
        errors.append("Name is required")
    if not email or "@" not in email:
        errors.append("Valid email is required")

    if errors:
        return Div(
            Alert(error, type=AlertT.error)
            for error in errors
        )

    # Process form
    return Alert("Success!", type=AlertT.success)
```

---

## API Quick Reference

### Core Modules

- `monsterui.core` - Theme system
- `monsterui.franken` - Main UI components
- `monsterui.daisy` - DaisyUI components
- `monsterui.foundations` - Utilities

### Common Imports

```python
# Everything
from monsterui.all import *

# Selective
from monsterui.core import Theme
from monsterui.franken import (
    # Layout
    Container, Section, Grid, Card,
    # Typography
    H1, H2, H3, P, Strong,
    # Forms
    Form, Input, Button, LabelInput,
    # Navigation
    NavBar, TabContainer,
    # Data
    Table, TableFromDicts
)
from monsterui.daisy import Alert, Loading, Steps
```

### Component Categories

**Layout**: Container, Section, Article, Grid, DivCentered, DivHStacked, DivVStacked

**Typography**: H1-H6, P, Span, Strong, Em, Code, CodeBlock

**Forms**: Input, TextArea, Select, CheckboxX, Radio, Range, Switch, Upload, Button

**Form Helpers**: LabelInput, LabelTextArea, LabelSelect, LabelCheckboxX

**Navigation**: NavBar, NavContainer, TabContainer, DropDownNavContainer

**Data**: Table, TableFromDicts, TableFromLists, Card

**Interactive**: Modal, Accordion, Details, Progress, Slider, Lightbox

**DaisyUI**: Alert, Loading, Steps, Toast

**Utilities**: UkIcon, DiceBearAvatar, PicSumImg, render_md, ApexChart

---

## Additional Resources

### Official Resources
- **Website**: https://monsterui.answer.ai/
- **GitHub**: https://github.com/AnswerDotAI/MonsterUI
- **Blog Post**: https://www.answer.ai/posts/2025-01-15-monsterui.html

### Learning Resources
- Official tutorial and documentation
- Example applications (dashboard, forms, authentication)
- Video demonstrations
- LLM context files (llms.txt, llms-ctx.txt, apilist.txt)

### Related Projects
- **FastHTML**: Web framework foundation
- **FrankenUI**: Core component library
- **DaisyUI**: Additional components
- **Tailwind CSS**: Styling system

---

**End of MonsterUI Comprehensive Reference**

*This documentation covers all MonsterUI components, patterns, and best practices for building beautiful web interfaces with Python. Designed for offline LLM use during development.*
