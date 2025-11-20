# FastHTML Comprehensive Reference Guide

> **For Offline LLM Development Use** - Complete documentation including API reference, best practices, and examples

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Routing & HTTP Methods](#routing--http-methods)
5. [HTML Construction](#html-construction)
6. [Styling with CSS](#styling-with-css)
7. [Interactivity with HTMX](#interactivity-with-htmx)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Complete Examples](#complete-examples)

---

## Overview

FastHTML is a next-generation Python web framework designed for building fast, scalable web applications with minimal, compact code. It's described as "the fastest, most powerful way to create an HTML app."

### Core Design Principles

1. **Powerful and expressive** - Build advanced, interactive web apps
2. **Fast and lightweight** - Write less code, get more done
3. **Easy to learn** - Simple, intuitive Python-first syntax

### Key Characteristics

- **Pure Python**: FastHTML apps are 100% Python - no separate HTML, CSS, or JavaScript files required
- **1:1 Mapping**: Direct mapping to HTML and HTTP fundamentals
- **HTMX Integration**: Built-in hypermedia support for dynamic interactions
- **Framework Foundation**: Built on Starlette/ASGI for production-ready performance

---

## Installation & Setup

### Basic Installation

```bash
pip install python-fasthtml
```

### Minimal Application

```python
from fasthtml.common import *

app, rt = fast_app()

@rt('/')
def get():
    return Div(P('Hello World!'), hx_get="/change")

serve()
```

### Running Your App

```bash
# Method 1: Direct Python execution
python main.py

# Method 2: Using Uvicorn (production)
uvicorn app:app --reload

# Method 3: Custom port
python main.py --port 8000
```

The app will be available at `http://localhost:5001` by default.

---

## Core Concepts

### Application Structure

FastHTML applications consist of:
- **App instance**: The main FastHTML application object
- **Route decorators**: Functions that handle HTTP requests
- **HTML components**: Python functions that generate HTML
- **Server**: The ASGI server (typically Uvicorn)

### The fast_app() Function

`fast_app()` returns a tuple containing:
1. **app**: The FastHTML application instance
2. **rt**: A route decorator factory

```python
from fasthtml.common import *

app, rt = fast_app()

# Optional: Add custom headers
app, rt = fast_app(hdrs=(picolink, custom_css))

# Optional: Enable sessions
app, rt = fast_app(secret_key="your-secret-key")
```

### Request/Response Flow

1. Client makes HTTP request
2. FastHTML matches URL to route
3. Route function executes
4. Python objects converted to HTML
5. HTML sent to client

If request comes from HTMX:
- Only partial HTML returned (not wrapped in `<html>` tag)
- Target element updated dynamically

---

## Routing & HTTP Methods

### Basic Routes

```python
@app.get("/")
def home():
    return H1("Home Page")

@app.post("/submit")
def submit():
    return P("Form submitted!")

@app.put("/update")
def update():
    return P("Resource updated")

@app.delete("/remove")
def remove():
    return P("Resource deleted")
```

### Alternative Route Syntax

```python
# Using @rt decorator (from fast_app)
@rt('/')
def home():
    return H1("Home")

# Using @app.route with method
@app.route("/", methods=["GET", "POST"])
def home():
    return H1("Home")
```

### Path Parameters

```python
# Basic path parameter
@app.get("/user/{name}")
def user_profile(name: str):
    return H1(f"Profile: {name}")

# Multiple parameters
@app.get("/post/{year}/{month}/{slug}")
def blog_post(year: int, month: int, slug: str):
    return Article(
        H1(f"Post from {month}/{year}"),
        P(f"Slug: {slug}")
    )

# Optional parameters with defaults
@app.get("/greet/{name}")
def greet(name: str = "Guest"):
    return P(f"Hello, {name}!")
```

### Type Conversion

FastHTML automatically converts path parameters:

```python
# Integer conversion
@app.get("/page/{num}")
def page(num: int):
    return P(f"Page {num + 1}")  # num is already an int

# Boolean conversion
@app.get("/feature/{enabled}")
def feature(enabled: bool):
    if enabled:
        return P("Feature is ON")
    return P("Feature is OFF")

# Enum conversion
from enum import Enum

class Status(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

@app.get("/posts/{status}")
def posts_by_status(status: Status):
    return P(f"Showing {status.value} posts")
```

### Advanced Path Parameters

```python
# Path objects (for file paths)
from pathlib import Path

@app.get("/files/{filepath:path}")
def serve_file(filepath: Path):
    return FileResponse(filepath)

# Regex matching
@app.get("/item/{id:int}")
def item(id: int):
    # Only matches numeric IDs
    return P(f"Item {id}")

# Dataclass parameters
from dataclasses import dataclass

@dataclass
class UserQuery:
    name: str
    age: int
    active: bool = True

@app.get("/search")
def search(q: UserQuery):
    return P(f"Searching for {q.name}, age {q.age}")
```

### Query Parameters

```python
@app.get("/search")
def search(q: str = "", page: int = 1, limit: int = 10):
    return Div(
        P(f"Search query: {q}"),
        P(f"Page {page}, showing {limit} results")
    )

# Access at: /search?q=fasthtml&page=2&limit=20
```

### Form Data

```python
@app.post("/login")
def login(username: str, password: str):
    # FastHTML automatically extracts form data
    if authenticate(username, password):
        return P("Login successful!")
    return P("Login failed")
```

### Special Route Arguments

FastHTML provides "magic" arguments that are automatically populated:

```python
@app.get("/profile")
def profile(
    request,      # or 'req': Raw Starlette Request object
    session,      # or 'sess': Session data dictionary
    htmx,        # HTMX request information
    app          # Application instance
):
    user_agent = request.headers.get('user-agent')
    user_id = session.get('user_id')
    is_htmx = htmx.request  # True if HTMX request

    return Div(
        P(f"User: {user_id}"),
        P(f"Browser: {user_agent}"),
        P(f"HTMX: {is_htmx}")
    )
```

---

## HTML Construction

### Using Python for HTML

FastHTML uses `fastcore.xml` for programmatic HTML generation:

```python
from fasthtml.common import *

# Simple elements
page = Html(
    Head(Title('My Page')),
    Body(
        H1('Welcome'),
        P('This is a paragraph'),
        A('Click here', href='https://example.com')
    )
)
```

### Common HTML Elements

```python
# Headings
H1("Title"), H2("Subtitle"), H3("Section"), H4("Subsection")

# Text elements
P("Paragraph"), Span("Inline text"), Strong("Bold"), Em("Italic")

# Lists
Ul(
    Li("Item 1"),
    Li("Item 2"),
    Li("Item 3")
)

Ol(
    Li("First"),
    Li("Second"),
    Li("Third")
)

# Links and images
A("Link text", href="/page")
Img(src="/image.jpg", alt="Description")

# Containers
Div("Content", cls="container")
Section("Section content")
Article("Article content")

# Forms
Form(
    Input(type="text", name="username", placeholder="Username"),
    Input(type="password", name="password"),
    Button("Submit", type="submit"),
    action="/login",
    method="post"
)
```

### Attributes

```python
# Using keyword arguments
Div("Content", id="main", cls="container")

# Note: 'cls' not 'class' (reserved keyword)
Button("Click", cls="btn btn-primary")

# 'fr' not 'for' (reserved keyword)
Label("Name:", fr="name-input")

# Data attributes
Div("Content", data_id="123", data_type="article")

# Boolean attributes
Input(type="checkbox", checked=True, disabled=False)

# Custom attributes
Div("Content", **{"x-data": "{ open: false }"})
```

### Building Complex Structures

```python
def create_card(title, content, link):
    return Div(
        H3(title, cls="card-title"),
        P(content, cls="card-content"),
        A("Read more", href=link, cls="card-link"),
        cls="card"
    )

@app.get("/")
def home():
    return Main(
        H1("Blog Posts"),
        create_card(
            "First Post",
            "This is the first post",
            "/post/1"
        ),
        create_card(
            "Second Post",
            "This is the second post",
            "/post/2"
        ),
        cls="container"
    )
```

### The Titled Helper

```python
# Creates a complete page with title
from fasthtml.common import Titled

@app.get("/")
def home():
    return Titled("My Page",
        P("Welcome to my page!"),
        Div("Some content")
    )

# Equivalent to:
# Html(
#     Head(Title("My Page")),
#     Body(P("Welcome..."), Div("Some..."))
# )
```

### XT Format (Custom Rendering)

Create custom classes that render to HTML:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __xt__(self):
        # Return [tag, children, attributes]
        return Div(
            Strong(self.name),
            Span(f" (age {self.age})"),
            cls="person"
        )

@app.get("/")
def home():
    person = Person("Alice", 30)
    return Div(
        H1("People"),
        person  # Automatically rendered via __xt__
    )
```

---

## Styling with CSS

### Built-in Pico CSS

FastHTML includes Pico CSS for clean, responsive styling:

```python
from fasthtml.common import *

# Enable Pico CSS
app, rt = fast_app(hdrs=(picolink,))

@rt("/")
def get():
    return Main(
        H1('Hello World'),
        P('Styled with Pico CSS'),
        cls="container"
    )
```

### Custom CSS

```python
# Inline styles
custom_css = Style("""
    :root {
        --pico-font-size: 100%;
        --primary-color: #007bff;
    }
    .hero {
        text-align: center;
        padding: 3rem 0;
    }
    .btn-custom {
        background: var(--primary-color);
        color: white;
    }
""")

app, rt = fast_app(hdrs=(picolink, custom_css))

# External stylesheet
external_css = Link(rel="stylesheet", href="/static/style.css")
app, rt = fast_app(hdrs=(picolink, external_css))
```

### Inline Styles

```python
# Using style attribute
Div(
    "Highlighted text",
    style="color: red; font-weight: bold;"
)

# Dynamic styles
def get_color(status):
    colors = {
        'success': 'green',
        'error': 'red',
        'warning': 'orange'
    }
    return colors.get(status, 'black')

@app.get("/status/{status}")
def show_status(status: str):
    return Div(
        f"Status: {status}",
        style=f"color: {get_color(status)};"
    )
```

### Responsive Design with Pico

```python
@app.get("/")
def home():
    return Main(
        # Grid layout (responsive)
        Div(
            Article("Column 1"),
            Article("Column 2"),
            Article("Column 3"),
            cls="grid"
        ),
        # Container (centered, max-width)
        cls="container"
    )
```

---

## Interactivity with HTMX

### HTMX Basics

HTMX enables partial page updates without full page reloads:

```python
@app.get("/")
def home():
    return Div(
        H1("Click Counter"),
        P("Count: 0", id="count"),
        Button(
            "Increment",
            hx_get="/increment",
            hx_target="#count",
            hx_swap="innerHTML"
        )
    )

@app.get("/increment")
def increment():
    # This would normally use a database or session
    # For demo, returning static value
    return "Count: 1"
```

### HTMX Attributes

```python
# hx_get: Make GET request
Button("Load", hx_get="/data")

# hx_post: Make POST request
Form(
    Input(name="text"),
    Button("Submit", hx_post="/submit"),
    hx_target="#result"
)

# hx_put: Make PUT request
Button("Update", hx_put="/update/123")

# hx_delete: Make DELETE request
Button("Delete", hx_delete="/delete/123")

# hx_target: Element to update
Button("Load", hx_get="/data", hx_target="#content")

# hx_swap: How to swap content
# - innerHTML: Replace inner content (default)
# - outerHTML: Replace entire element
# - beforebegin: Insert before element
# - afterbegin: Insert at start of element
# - beforeend: Insert at end of element
# - afterend: Insert after element
# - delete: Delete target element
# - none: Don't swap anything

Button("Replace", hx_get="/data", hx_swap="outerHTML")

# hx_trigger: What triggers the request
Input(
    hx_get="/search",
    hx_trigger="keyup changed delay:500ms",
    hx_target="#results"
)

# hx_indicator: Show loading indicator
Button(
    "Load",
    hx_get="/slow",
    hx_indicator="#spinner"
)
```

### Complete HTMX Example: Todo App

```python
from fasthtml.common import *

app, rt = fast_app()

# In-memory storage (use database in production)
todos = []
todo_id = 0

@rt("/")
def get():
    return Titled("Todo App",
        Form(
            Input(
                name="task",
                placeholder="New task...",
                required=True
            ),
            Button("Add", type="submit"),
            hx_post="/add",
            hx_target="#todo-list",
            hx_swap="beforeend",
            hx_on="htmx:afterRequest: this.reset()"
        ),
        Ul(id="todo-list")
    )

@rt("/add")
def post(task: str):
    global todo_id
    todo_id += 1
    tid = todo_id
    todos.append({"id": tid, "task": task})

    return Li(
        Span(task),
        Button(
            "Delete",
            hx_delete=f"/delete/{tid}",
            hx_target="closest li",
            hx_swap="outerHTML"
        ),
        id=f"todo-{tid}"
    )

@rt("/delete/{tid}")
def delete(tid: int):
    todos[:] = [t for t in todos if t["id"] != tid]
    return ""  # Return empty (element will be deleted)

serve()
```

### Out-of-Band Swaps

Update multiple elements in a single response:

```python
@app.post("/action")
def action():
    return Div(
        # Main response (targeted element)
        P("Action completed!"),

        # Out-of-band updates (by ID)
        Div(
            "Notification: Success!",
            id="notifications",
            hx_swap_oob="true"
        ),
        Div(
            f"Updated at: {datetime.now()}",
            id="timestamp",
            hx_swap_oob="true"
        )
    )
```

### Loading States

```python
@app.get("/")
def home():
    return Div(
        Button(
            "Load Data",
            hx_get="/slow-data",
            hx_target="#content",
            hx_indicator="#spinner"
        ),
        Div(
            Span("Loading...", cls="htmx-indicator"),
            id="spinner"
        ),
        Div(id="content")
    )

@app.get("/slow-data")
async def slow_data():
    await asyncio.sleep(2)  # Simulate slow operation
    return P("Data loaded!")
```

### Form Validation

```python
@app.get("/")
def home():
    return Form(
        Input(
            name="email",
            type="email",
            hx_post="/validate-email",
            hx_trigger="blur",
            hx_target="#email-error"
        ),
        Div(id="email-error"),
        Button("Submit", type="submit"),
        hx_post="/submit"
    )

@app.post("/validate-email")
def validate_email(email: str):
    if "@" not in email:
        return Span(
            "Invalid email",
            style="color: red;",
            id="email-error"
        )
    return Span(
        "Valid email",
        style="color: green;",
        id="email-error"
    )
```

---

## Advanced Features

### Sessions

```python
from fasthtml.common import *

app, rt = fast_app(secret_key="your-secret-key-here")

@rt("/login")
def get(session):
    return Form(
        Input(name="username"),
        Button("Login"),
        method="post"
    )

@rt("/login")
def post(username: str, session):
    session['username'] = username
    session['logged_in'] = True
    return RedirectResponse("/dashboard", status_code=303)

@rt("/dashboard")
def get(session):
    if not session.get('logged_in'):
        return RedirectResponse("/login", status_code=303)

    return Titled(
        f"Dashboard - {session['username']}",
        P(f"Welcome back, {session['username']}!")
    )

@rt("/logout")
def post(session):
    session.clear()
    return RedirectResponse("/", status_code=303)
```

### Static Files

```python
# Serve static files from a directory
@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return FileResponse(f'static/{fname}.{ext}')

# Usage:
# Place files in ./static/
# Access at: /styles.css, /images/logo.png, etc.
```

### Database Integration

```python
from fasthtml.common import *
import sqlite3

# Simple database helper
def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT
            )
        ''')
        db.commit()

app, rt = fast_app()
init_db()

@rt("/users")
def get():
    with get_db() as db:
        users = db.execute('SELECT * FROM users').fetchall()

    return Titled("Users",
        Table(
            Thead(Tr(Th("ID"), Th("Username"), Th("Email"))),
            Tbody(*[
                Tr(
                    Td(user['id']),
                    Td(user['username']),
                    Td(user['email'])
                )
                for user in users
            ])
        )
    )

@rt("/users/add")
def post(username: str, email: str):
    with get_db() as db:
        db.execute(
            'INSERT INTO users (username, email) VALUES (?, ?)',
            (username, email)
        )
        db.commit()

    return RedirectResponse("/users", status_code=303)
```

### WebSockets

```python
from fasthtml.common import *

app, rt = fast_app()

@rt("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            # Echo back
            await websocket.send_text(f"Echo: {data}")
    except:
        pass

@rt("/")
def get():
    return Titled("WebSocket Demo",
        Script("""
            const ws = new WebSocket('ws://localhost:5001/ws');
            ws.onmessage = (event) => {
                console.log('Received:', event.data);
            };
        """)
    )
```

### Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers['X-Process-Time'] = str(duration)
        return response

app.add_middleware(TimingMiddleware)
```

### Background Tasks

```python
from starlette.background import BackgroundTask

def send_email(email: str, message: str):
    # Simulate sending email
    print(f"Sending email to {email}: {message}")

@app.post("/notify")
def notify(email: str, message: str):
    task = BackgroundTask(send_email, email, message)
    return Response(
        "Notification queued!",
        background=task
    )
```

### Error Handling

```python
from fasthtml.common import *

app, rt = fast_app()

@app.exception_handler(404)
def not_found(request, exc):
    return Titled("404 Not Found",
        H1("Page Not Found"),
        P("The page you're looking for doesn't exist."),
        A("Go Home", href="/")
    ), 404

@app.exception_handler(500)
def server_error(request, exc):
    return Titled("500 Server Error",
        H1("Something Went Wrong"),
        P("We're working on fixing it!")
    ), 500

# Custom exception
class Unauthorized(Exception):
    pass

@app.exception_handler(Unauthorized)
def handle_unauthorized(request, exc):
    return RedirectResponse("/login", status_code=303)
```

### Testing

```python
from starlette.testclient import TestClient
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return H1("Hello")

# Test
client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello" in response.text

def test_api():
    response = client.post("/api", json={"key": "value"})
    assert response.status_code == 200
```

---

## Best Practices

### 1. Project Structure

```
my_fasthtml_app/
├── app.py              # Main application
├── models.py           # Database models
├── components.py       # Reusable UI components
├── routes/
│   ├── __init__.py
│   ├── auth.py        # Authentication routes
│   ├── api.py         # API routes
│   └── pages.py       # Page routes
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # If using any templates
├── requirements.txt
└── README.md
```

### 2. Reusable Components

```python
# components.py
from fasthtml.common import *

def NavBar(current_page=None):
    """Reusable navigation component"""
    pages = [
        ("Home", "/"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    return Nav(
        Ul(*[
            Li(
                A(
                    name,
                    href=url,
                    cls="active" if url == current_page else ""
                )
            )
            for name, url in pages
        ]),
        cls="navbar"
    )

def PageLayout(title, *content, current_page=None):
    """Standard page layout"""
    return Titled(title,
        NavBar(current_page),
        Main(*content, cls="container"),
        Footer(
            P("© 2025 My App"),
            cls="footer"
        )
    )

# Usage in routes
@app.get("/")
def home():
    return PageLayout(
        "Home",
        H1("Welcome"),
        P("This is the home page"),
        current_page="/"
    )
```

### 3. Separation of Concerns

```python
# models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: str

    @classmethod
    def from_db(cls, row):
        return cls(
            id=row['id'],
            username=row['username'],
            email=row['email']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# routes/users.py
from fasthtml.common import *
from models import User

def setup_user_routes(rt):
    @rt("/users")
    def get():
        users = User.get_all()  # Database query
        return render_users(users)

    @rt("/users/{uid}")
    def get(uid: int):
        user = User.get_by_id(uid)
        return render_user(user)

# components.py
def render_user(user: User):
    return Div(
        H2(user.username),
        P(user.email),
        cls="user-card"
    )
```

### 4. Environment Configuration

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT: int = int(os.getenv('PORT', 5001))

config = Config()

# app.py
from fasthtml.common import *
from config import config

app, rt = fast_app(
    secret_key=config.SECRET_KEY,
    debug=config.DEBUG
)

if __name__ == "__main__":
    serve(port=config.PORT)
```

### 5. Security Best Practices

```python
# CSRF Protection (built-in with forms)
@rt("/form")
def get(session):
    return Form(
        Input(name="data"),
        Button("Submit"),
        method="post"
    )

# Input Validation
from pydantic import BaseModel, EmailStr, validator

class UserInput(BaseModel):
    username: str
    email: EmailStr
    age: int

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('age')
    def age_valid(cls, v):
        assert 0 < v < 150, 'must be valid age'
        return v

@rt("/register")
def post(user: UserInput):
    # user is validated automatically
    save_user(user)
    return P("User registered!")

# SQL Injection Prevention (use parameterized queries)
# GOOD:
cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))

# BAD:
# cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')

# XSS Prevention (FastHTML escapes by default)
@rt("/display")
def get(user_input: str):
    # This is safe - FastHTML escapes HTML
    return P(user_input)
```

### 6. Performance Optimization

```python
# Use async for I/O operations
@rt("/data")
async def get():
    # Parallel requests
    results = await asyncio.gather(
        fetch_api_1(),
        fetch_api_2(),
        fetch_database()
    )
    return render_results(results)

# Cache static responses
from functools import lru_cache

@lru_cache(maxsize=100)
def get_config():
    # Expensive operation
    return load_config_from_file()

# Use streaming for large responses
@rt("/download")
async def get():
    async def generate():
        for chunk in get_large_file():
            yield chunk

    return StreamingResponse(generate())
```

### 7. Error Handling and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@rt("/process")
def post(data: str):
    try:
        result = process_data(data)
        logger.info(f"Processed data: {data}")
        return P(f"Result: {result}")

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return P(f"Invalid data: {e}"), 400

    except Exception as e:
        logger.exception("Unexpected error")
        return P("An error occurred"), 500
```

### 8. API Design

```python
# RESTful API routes
@rt("/api/users")
def get():
    """List all users"""
    users = get_all_users()
    return {"users": [u.to_dict() for u in users]}

@rt("/api/users/{uid}")
def get(uid: int):
    """Get specific user"""
    user = get_user(uid)
    return user.to_dict()

@rt("/api/users")
def post(user: UserInput):
    """Create user"""
    new_user = create_user(user)
    return new_user.to_dict(), 201

@rt("/api/users/{uid}")
def put(uid: int, user: UserInput):
    """Update user"""
    updated = update_user(uid, user)
    return updated.to_dict()

@rt("/api/users/{uid}")
def delete(uid: int):
    """Delete user"""
    delete_user(uid)
    return {"status": "deleted"}, 204
```

---

## Complete Examples

### Example 1: Simple Blog

```python
from fasthtml.common import *
from datetime import datetime

app, rt = fast_app(hdrs=(picolink,))

# Mock database
posts = [
    {"id": 1, "title": "First Post", "content": "Hello world!", "date": "2025-01-01"},
    {"id": 2, "title": "Second Post", "content": "FastHTML is great!", "date": "2025-01-02"},
]

def PostCard(post):
    return Article(
        H3(A(post['title'], href=f"/post/{post['id']}")),
        P(post['content'][:100] + "..."),
        Small(post['date']),
        cls="post-card"
    )

@rt("/")
def get():
    return Titled("My Blog",
        Header(
            H1("My Blog"),
            P("Thoughts and ideas"),
            cls="hero"
        ),
        Main(
            *[PostCard(post) for post in posts],
            cls="container"
        )
    )

@rt("/post/{pid}")
def get(pid: int):
    post = next((p for p in posts if p['id'] == pid), None)
    if not post:
        return Titled("404", H1("Post not found")), 404

    return Titled(post['title'],
        Article(
            H1(post['title']),
            Small(post['date']),
            P(post['content']),
            A("← Back", href="/"),
            cls="container"
        )
    )

serve()
```

### Example 2: Todo App with Database

```python
from fasthtml.common import *
import sqlite3

app, rt = fast_app(hdrs=(picolink,))

# Database setup
def get_db():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

init_db()

def TodoItem(todo):
    return Li(
        Div(
            Input(
                type="checkbox",
                checked=bool(todo['completed']),
                hx_post=f"/toggle/{todo['id']}",
                hx_target=f"#todo-{todo['id']}",
                hx_swap="outerHTML"
            ),
            Span(
                todo['task'],
                style="text-decoration: line-through;" if todo['completed'] else ""
            ),
            Button(
                "×",
                hx_delete=f"/delete/{todo['id']}",
                hx_target=f"#todo-{todo['id']}",
                hx_swap="outerHTML",
                cls="close-btn"
            ),
            cls="todo-item"
        ),
        id=f"todo-{todo['id']}"
    )

@rt("/")
def get():
    with get_db() as db:
        todos = db.execute(
            'SELECT * FROM todos ORDER BY created_at DESC'
        ).fetchall()

    return Titled("Todo List",
        Main(
            H1("My Todos"),
            Form(
                Input(
                    name="task",
                    placeholder="What needs to be done?",
                    required=True,
                    autofocus=True
                ),
                Button("Add", type="submit"),
                hx_post="/add",
                hx_target="#todo-list",
                hx_swap="afterbegin",
                hx_on="htmx:afterRequest: this.reset()"
            ),
            Ul(
                *[TodoItem(todo) for todo in todos],
                id="todo-list"
            ),
            cls="container"
        )
    )

@rt("/add")
def post(task: str):
    with get_db() as db:
        cursor = db.execute(
            'INSERT INTO todos (task) VALUES (?)',
            (task,)
        )
        db.commit()
        todo_id = cursor.lastrowid
        todo = db.execute(
            'SELECT * FROM todos WHERE id = ?',
            (todo_id,)
        ).fetchone()

    return TodoItem(todo)

@rt("/toggle/{tid}")
def post(tid: int):
    with get_db() as db:
        db.execute(
            'UPDATE todos SET completed = NOT completed WHERE id = ?',
            (tid,)
        )
        db.commit()
        todo = db.execute(
            'SELECT * FROM todos WHERE id = ?',
            (tid,)
        ).fetchone()

    return TodoItem(todo)

@rt("/delete/{tid}")
def delete(tid: int):
    with get_db() as db:
        db.execute('DELETE FROM todos WHERE id = ?', (tid,))
        db.commit()

    return ""

serve()
```

### Example 3: Authentication System

```python
from fasthtml.common import *
import hashlib
import sqlite3

app, rt = fast_app(
    secret_key="your-secret-key-change-in-production",
    hdrs=(picolink,)
)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        db.commit()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash):
    return hash_password(password) == hash

@rt("/")
def get(session):
    if session.get('user_id'):
        return RedirectResponse("/dashboard", status_code=303)
    return RedirectResponse("/login", status_code=303)

@rt("/register")
def get():
    return Titled("Register",
        Main(
            H1("Register"),
            Form(
                Input(
                    name="username",
                    placeholder="Username",
                    required=True
                ),
                Input(
                    name="password",
                    type="password",
                    placeholder="Password",
                    required=True
                ),
                Button("Register", type="submit"),
                hx_post="/register",
                hx_target="#message"
            ),
            Div(id="message"),
            P(A("Already have an account? Login", href="/login")),
            cls="container"
        )
    )

@rt("/register")
def post(username: str, password: str):
    try:
        with get_db() as db:
            db.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, hash_password(password))
            )
            db.commit()

        return Div(
            P("Registration successful!"),
            A("Go to login", href="/login"),
            style="color: green;"
        )

    except sqlite3.IntegrityError:
        return Div(
            P("Username already exists"),
            style="color: red;"
        )

@rt("/login")
def get(session):
    if session.get('user_id'):
        return RedirectResponse("/dashboard", status_code=303)

    return Titled("Login",
        Main(
            H1("Login"),
            Form(
                Input(
                    name="username",
                    placeholder="Username",
                    required=True
                ),
                Input(
                    name="password",
                    type="password",
                    placeholder="Password",
                    required=True
                ),
                Button("Login", type="submit"),
                method="post"
            ),
            P(A("Don't have an account? Register", href="/register")),
            cls="container"
        )
    )

@rt("/login")
def post(username: str, password: str, session):
    with get_db() as db:
        user = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

    if user and verify_password(password, user['password_hash']):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return RedirectResponse("/dashboard", status_code=303)

    return Titled("Login Failed",
        Main(
            H1("Login Failed"),
            P("Invalid username or password"),
            A("Try again", href="/login"),
            cls="container"
        )
    )

@rt("/dashboard")
def get(session):
    if not session.get('user_id'):
        return RedirectResponse("/login", status_code=303)

    return Titled(f"Dashboard - {session['username']}",
        Main(
            H1(f"Welcome, {session['username']}!"),
            P("This is your dashboard"),
            Form(
                Button("Logout", type="submit"),
                method="post",
                action="/logout"
            ),
            cls="container"
        )
    )

@rt("/logout")
def post(session):
    session.clear()
    return RedirectResponse("/login", status_code=303)

serve()
```

---

## Additional Resources

### Official Resources
- **Documentation**: https://docs.fastht.ml/
- **GitHub Repository**: https://github.com/AnswerDotAI/fasthtml
- **Examples Repository**: https://github.com/AnswerDotAI/fasthtml-example
- **FastHTML Gallery**: Component and pattern examples
- **Discord Community**: Community support and discussions

### Learning Path
1. Start with the minimal example
2. Learn HTML construction with Python
3. Add styling with Pico CSS
4. Implement interactivity with HTMX
5. Add database integration
6. Build authentication
7. Deploy to production

### Related Technologies
- **Starlette**: ASGI framework (FastHTML foundation)
- **HTMX**: Hypermedia-driven interactions
- **Pico CSS**: Classless CSS framework
- **fastcore.xml**: XML/HTML generation library

### LLM Integration Tips

When using this documentation with LLMs:
- FastHTML is newer than most LLM training data
- Provide this documentation as context for accurate responses
- FastHTML maps directly to HTML/HTTP - no magic or abstraction
- All functionality is pure Python - no separate template languages
- HTMX is central to interactivity - understand its patterns

---

**End of FastHTML Comprehensive Reference**

*This documentation is designed for offline LLM use during development. It covers installation, core concepts, routing, HTML construction, styling, HTMX interactivity, advanced features, best practices, and complete working examples.*
