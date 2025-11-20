# nbdev Comprehensive Reference Guide

> **For Offline LLM Development Use** - Complete documentation for notebook-driven development

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Project Initialization](#project-initialization)
5. [Notebook Structure](#notebook-structure)
6. [Directives & Annotations](#directives--annotations)
7. [Exporting Code](#exporting-code)
8. [Testing](#testing)
9. [Documentation](#documentation)
10. [Git Integration](#git-integration)
11. [Publishing](#publishing)
12. [CLI Commands](#cli-commands)
13. [Best Practices](#best-practices)
14. [Complete Examples](#complete-examples)

---

## Overview

**nbdev** is a notebook-driven development platform that enables you to write, test, document, and distribute software packages and technical articles — all in one place, your notebook.

### Philosophy

nbdev embraces **literate programming** and **exploratory programming**, allowing you to develop software in Jupyter Notebooks while maintaining software engineering best practices.

### Key Benefits

1. **Unified Development**: Write code, tests, and documentation in one place
2. **Exploratory**: Live objects always at your fingertips for debugging and refactoring
3. **Best Practices**: Tests and documentation are first-class citizens
4. **Professional Output**: Generates beautiful docs, packages, and CI/CD automatically
5. **IDE Compatible**: Two-way sync between notebooks and plaintext source files

### What nbdev Provides

- ✅ **Beautiful Documentation**: Auto-generated using Quarto on GitHub Pages
- ✅ **Continuous Integration**: Pre-configured GitHub Actions
- ✅ **Package Publishing**: Deploy to PyPI and conda automatically
- ✅ **Parallel Testing**: Run tests from notebook cells with a single command
- ✅ **Git-Friendly**: Human-readable merge conflicts and clean metadata
- ✅ **IDE Integration**: Edit in notebooks or your IDE with auto-sync

---

## Installation & Setup

### Prerequisites

- Python 3.7 or later
- Jupyter (JupyterLab or Jupyter Notebook)
- Git
- Quarto (for documentation)
- GitHub account (for hosting docs and CI/CD)

### Installation

**Via pip:**
```bash
pip install nbdev
```

**Via conda:**
```bash
conda install -c fastai nbdev
```

**Via mamba:**
```bash
mamba install -c fastai nbdev
```

### Platform Support

- ✅ macOS
- ✅ Linux
- ✅ Unix systems
- ⚠️ Windows: Requires WSL (Windows Subsystem for Linux)

### Verify Installation

```bash
nbdev_help
```

This should display available nbdev commands.

### Install Quarto

Download and install from: https://quarto.org/docs/get-started/

Quarto is required for documentation generation.

---

## Core Concepts

### Literate Programming

nbdev enables **literate programming**: write prose explaining your code, with the code itself interspersed throughout. This creates documentation that reads like a narrative.

### Exploratory Programming

With notebooks, you maintain **live objects** in memory, making debugging and refactoring easier. You can:
- Inspect variables at any time
- Test functions immediately
- Iterate quickly on ideas

### Single Source of Truth

The notebook is the **single source** for:
- Source code (exported to .py files)
- Tests (run with nbdev_test)
- Documentation (rendered with Quarto)
- Examples and tutorials

### Two-Way Sync

Edit in notebooks OR in your IDE:
- Changes in notebooks → exported to .py files
- Changes in .py files → synced back to notebooks

---

## Project Initialization

### Creating a New Project

#### Step 1: Create GitHub Repository

1. Go to GitHub and create a new **empty** repository
2. **Do not** initialize with README, .gitignore, or license
3. Enable **GitHub Pages** in repository settings (Settings → Pages → Source: GitHub Actions)

#### Step 2: Initialize Locally

```bash
# Clone your empty repo
git clone https://github.com/username/repo-name.git
cd repo-name

# Initialize nbdev project
nbdev_new
```

#### Step 3: Answer Setup Questions

nbdev_new will ask:
- **Project name**: Your package name (e.g., "myproject")
- **Description**: Short description
- **Author**: Your name
- **Author email**: Your email
- **License**: Choose license (MIT, Apache, GPL, etc.)

#### Step 4: Complete Setup

```bash
# Install git hooks
nbdev_install_hooks

# Install package in editable mode
pip install -e '.[dev]'

# Make first commit
git add .
git commit -m "Initial nbdev project setup"
git push
```

### Project Structure

After initialization:

```
repo-name/
├── nbs/                    # Notebooks (source of truth)
│   ├── 00_core.ipynb      # Core module
│   ├── index.ipynb        # Homepage/README
│   └── ...
├── repo_name/              # Exported Python package
│   ├── __init__.py
│   ├── core.py            # Exported from 00_core.ipynb
│   └── ...
├── .github/
│   └── workflows/
│       └── deploy.yaml    # CI/CD for docs and tests
├── settings.ini           # Project configuration
├── setup.py               # Package setup (auto-generated)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md              # Auto-generated from index.ipynb
```

---

## Notebook Structure

### Notebook Naming Convention

```
nbs/
├── 00_core.ipynb          # Exports to: repo_name/core.py
├── 01_utils.ipynb         # Exports to: repo_name/utils.py
├── 02_models.ipynb        # Exports to: repo_name/models.py
├── 10_advanced.ipynb      # Exports to: repo_name/advanced.py
└── index.ipynb            # Becomes README.md and docs homepage
```

**Numbering**: Use numbers to control order in documentation.

### Basic Notebook Template

```python
# Cell 1: Module designation
#| default_exp core

# Cell 2: Imports
#| export
from fastcore.utils import *
import numpy as np

# Cell 3: Function definition
#| export
def greet(name: str) -> str:
    "Say hello to `name`"
    return f"Hello, {name}!"

# Cell 4: Test
assert greet("World") == "Hello, World!"

# Cell 5: Example (not exported)
greet("nbdev")
```

### Markdown Cells

Use markdown for:
- Explanations
- Tutorials
- Examples
- API documentation

```markdown
# Core Functionality

This module provides core utilities for the project.

## Greeting Function

The `greet` function provides a simple greeting:
```

---

## Directives & Annotations

Directives are special comments that control nbdev behavior.

### Export Directives

#### #| default_exp

Specifies which module this notebook exports to:

```python
#| default_exp core
# This notebook exports to: package_name/core.py
```

```python
#| default_exp models.neural
# This notebook exports to: package_name/models/neural.py
```

#### #| export

Mark cells to export to .py files:

```python
#| export
def my_function():
    "This function will be exported"
    pass
```

#### #| exporti

Export but hide from documentation (internal functions):

```python
#| exporti
def _internal_helper():
    "Not shown in docs"
    pass
```

### Test Directives

#### #| test

Mark a cell as a test:

```python
#| test
assert greet("World") == "Hello, World!"
assert greet("") == "Hello, !"
```

#### #| slow

Mark slow tests (skipped in quick test runs):

```python
#| slow
# This test takes a long time
for i in range(1000000):
    complex_operation(i)
```

### Documentation Directives

#### #| hide

Hide cell from documentation (but still execute):

```python
#| hide
# Setup code not shown in docs
import internal_test_utils
setup_test_environment()
```

#### #| hide_input

Show output but hide code:

```python
#| hide_input
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
# Plot appears in docs, code doesn't
```

#### #| echo: false

Don't show cell in docs and don't execute:

```python
#| echo: false
# Neither code nor output in docs
```

### Execution Control

#### #| eval: false

Show code but don't execute:

```python
#| eval: false
# This code is shown but not run
dangerous_operation()
```

#### #| include: false

Execute but hide from docs (code and output):

```python
#| include: false
# Runs during testing but not in docs
```

---

## Exporting Code

### Basic Export

```bash
# Export all notebooks to .py files
nbdev_export
```

This converts notebook cells marked with `#| export` to Python modules.

### How Export Works

```python
# In nbs/00_core.ipynb

#| default_exp core

#| export
def add(a, b):
    "Add two numbers"
    return a + b

#| export
class Calculator:
    "A simple calculator"
    def __init__(self):
        self.result = 0
```

Exports to `package_name/core.py`:

```python
# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb

from __future__ import annotations

def add(a, b):
    "Add two numbers"
    return a + b

class Calculator:
    "A simple calculator"
    def __init__(self):
        self.result = 0
```

### Conditional Exports

```python
#| export
import sys

if sys.version_info >= (3, 8):
    # Python 3.8+ only
    from typing import Protocol
else:
    Protocol = object
```

### Multi-Module Projects

```python
# nbs/00_core.ipynb
#| default_exp core

# nbs/01_utils.ipynb
#| default_exp utils

# nbs/02_models.ipynb
#| default_exp models.neural

# Creates:
# package/core.py
# package/utils.py
# package/models/neural.py (with models/__init__.py)
```

---

## Testing

### Writing Tests

Tests are written inline with your code:

```python
#| export
def divide(a, b):
    "Divide `a` by `b`"
    return a / b

# Test (not exported)
assert divide(10, 2) == 5
assert divide(9, 3) == 3
```

### Using test_fail

```python
from fastcore.test import test_fail

#| export
def must_be_positive(x):
    "Raises ValueError if `x` is negative"
    if x < 0:
        raise ValueError("x must be positive")
    return x

# Test that it raises correctly
test_fail(lambda: must_be_positive(-1), contains="positive")
```

### Using test_eq and Friends

```python
from fastcore.test import test_eq, test_ne, test_close

test_eq(divide(10, 2), 5)
test_ne(divide(10, 3), 3)
test_close(divide(10, 3), 3.333, eps=0.001)
```

### Running Tests

```bash
# Test all notebooks
nbdev_test

# Test specific notebook
nbdev_test --path nbs/00_core.ipynb

# Skip slow tests
nbdev_test --skip_slow

# Parallel testing
nbdev_test --n_workers 4

# Verbose output
nbdev_test --verbose
```

### Test in CI/CD

Tests run automatically on GitHub Actions when you push:

```yaml
# .github/workflows/deploy.yaml (auto-generated)
- name: Run tests
  run: nbdev_test --n_workers 2
```

---

## Documentation

### Documentation Generation

nbdev uses **Quarto** to generate beautiful documentation from notebooks.

### Basic Documentation

```bash
# Build documentation
nbdev_docs

# Preview locally
nbdev_preview

# This opens a browser with live-reloading docs
```

### Doc Structure

- `index.ipynb` → Homepage (README.md)
- Other notebooks → Individual doc pages
- API reference auto-generated from docstrings

### Docstrings

Write docstrings in your exported functions:

```python
#| export
def calculate(x: int, y: int, operation: str = 'add') -> int:
    """Perform a calculation on two numbers.

    Args:
        x: First number
        y: Second number
        operation: Operation to perform ('add', 'subtract', 'multiply', 'divide')

    Returns:
        Result of the calculation

    Examples:
        >>> calculate(5, 3, 'add')
        8
        >>> calculate(10, 2, 'divide')
        5
    """
    if operation == 'add':
        return x + y
    elif operation == 'subtract':
        return x - y
    # ... etc
```

### show_doc

Display documentation for any function:

```python
from nbdev.showdoc import show_doc

show_doc(calculate)
```

This renders the function signature and docstring beautifully in docs.

### Documenting Classes

```python
#| export
class DataProcessor:
    """Process and transform data.

    This class provides utilities for data processing.
    """

    def __init__(self, name: str):
        """Initialize processor.

        Args:
            name: Name of this processor
        """
        self.name = name

    def process(self, data: list) -> list:
        """Process the data.

        Args:
            data: Input data to process

        Returns:
            Processed data
        """
        return [x * 2 for x in data]

# Show full class documentation
show_doc(DataProcessor)

# Show specific method
show_doc(DataProcessor.process)
```

### Adding Documentation Across Cells

Use `@patch` to add methods in separate cells:

```python
#| export
class Calculator:
    """A calculator class"""
    def __init__(self):
        self.result = 0
```

```python
#| export
from fastcore.basics import patch

@patch
def add(self: Calculator, x):
    """Add `x` to result"""
    self.result += x
    return self.result

@patch
def multiply(self: Calculator, x):
    """Multiply result by `x`"""
    self.result *= x
    return self.result
```

### Doclinks

Reference other functions/classes automatically:

```markdown
The `calculate` function uses `DataProcessor` internally.

Use `DataProcessor.process` to transform data.
```

nbdev automatically creates links to the referenced items.

### Cross-References

```markdown
See `module.function` for more details.

Related: `OtherClass.method`
```

### Math and Code

**LaTeX math:**
```markdown
The formula is $E = mc^2$

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

**Code blocks:**
````markdown
```python
result = calculate(5, 3, 'add')
print(result)  # 8
```
````

### Customizing Docs

Edit `_quarto.yml` to customize:

```yaml
project:
  type: website

website:
  title: "My Project"
  navbar:
    left:
      - text: "Documentation"
        href: index.html
      - text: "Tutorials"
        href: tutorials.html
```

---

## Git Integration

### Git Hooks

nbdev provides git hooks for notebook-friendly workflows.

#### Install Hooks

```bash
nbdev_install_hooks
```

This installs hooks that:
- Clean notebook metadata before commits
- Render merge conflicts in human-readable format

### Clean Notebooks

```bash
# Clean all notebooks (remove metadata, outputs for clean commits)
nbdev_clean

# Clean and add to git
nbdev_clean --clear_all
```

### Merge Conflicts

When merge conflicts occur in notebooks, nbdev renders them in a readable format showing:
- Code changes
- Output changes
- Metadata conflicts

Resolve normally in your editor.

### Pre-Commit Hook

The git hook runs `nbdev_clean` automatically before each commit, ensuring:
- Consistent metadata
- No extraneous outputs
- Clean diffs

### .gitignore

nbdev creates a .gitignore that includes:
```
# nbdev
_docs/
_proc/
*.py[cod]
__pycache__/
```

---

## Publishing

### Publishing to PyPI

#### Step 1: Update Version

Edit `settings.ini`:
```ini
version = 0.0.1
```

Update `CHANGELOG.md` with changes.

#### Step 2: Prepare Release

```bash
# Export, test, clean
nbdev_prepare
```

This runs:
1. `nbdev_export` - Export notebooks to .py
2. `nbdev_test` - Run all tests
3. `nbdev_clean` - Clean notebooks
4. `nbdev_readme` - Update README

#### Step 3: Build Package

```bash
# Create distribution files
python -m build
```

This creates:
- `dist/package_name-0.0.1.tar.gz`
- `dist/package_name-0.0.1-py3-none-any.whl`

#### Step 4: Upload to PyPI

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*
```

Enter your PyPI credentials when prompted.

#### Step 5: Tag Release

```bash
git tag v0.0.1
git push --tags
```

### Publishing to Conda

Edit `settings.ini`:
```ini
conda_channel = your-channel
```

Use conda-forge or your own channel.

Build and upload:
```bash
conda build .
anaconda upload /path/to/package.tar.bz2
```

### Automated Publishing

Set up GitHub Secrets:
- `PYPI_TOKEN`: Your PyPI API token

The GitHub workflow will auto-publish on tagged releases.

### Releasing Workflow

```bash
# 1. Update version in settings.ini
# 2. Update CHANGELOG.md

# 3. Prepare release
nbdev_prepare

# 4. Commit and tag
git add .
git commit -m "Release v0.0.1"
git tag v0.0.1

# 5. Push
git push
git push --tags

# 6. Build and publish
python -m build
twine upload dist/*
```

---

## CLI Commands

### Essential Commands

```bash
# Project setup
nbdev_new                  # Initialize new project
nbdev_install_hooks        # Install git hooks

# Development
nbdev_export              # Export notebooks to .py files
nbdev_test                # Run tests
nbdev_clean               # Clean notebooks
nbdev_prepare             # Export, test, clean, and update README

# Documentation
nbdev_docs                # Build documentation
nbdev_preview             # Preview docs locally
nbdev_readme              # Update README from index.ipynb

# Publishing
nbdev_release_git         # Tag and push release
nbdev_release_gh          # Create GitHub release
nbdev_conda               # Build conda package

# Utilities
nbdev_help                # Show all commands
nbdev_install_quarto      # Install Quarto
nbdev_upgrade             # Upgrade nbdev
```

### Command Details

#### nbdev_prepare

Runs the complete pre-release workflow:
```bash
nbdev_prepare

# Equivalent to:
nbdev_export && nbdev_test && nbdev_clean && nbdev_readme
```

#### nbdev_test Options

```bash
nbdev_test                        # Test all notebooks
nbdev_test --path nbs/00_core.ipynb  # Test one notebook
nbdev_test --n_workers 4          # Parallel testing
nbdev_test --skip_slow            # Skip slow tests
nbdev_test --verbose              # Verbose output
```

#### nbdev_export Options

```bash
nbdev_export                      # Export all
nbdev_export --path nbs/00_core.ipynb  # Export one
```

#### nbdev_clean Options

```bash
nbdev_clean                       # Clean all notebooks
nbdev_clean --clear_all           # Remove all outputs
nbdev_clean --fname nbs/00_core.ipynb  # Clean specific file
```

---

## Best Practices

### 1. Notebook Organization

**Good structure:**
```
00-09: Core functionality
10-19: Utilities
20-29: Models
30-39: Data processing
40-49: Visualization
50-59: Advanced features
```

**Naming:**
- Use numbers for ordering
- Use descriptive names: `05_data_preprocessing.ipynb`

### 2. Writing Good Documentation

```markdown
# Module Name

> Brief description

## Overview

Detailed explanation of what this module does.

## Core Functions

### Function Name

Detailed explanation with examples.
```

**Example:**
```python
#| export
def process_data(data: list, method: str = 'standard') -> list:
    """Process data using specified method.

    This function transforms input data according to the chosen
    processing method. Supports multiple algorithms.

    Args:
        data: Input data as a list
        method: Processing method ('standard', 'advanced', 'minimal')

    Returns:
        Processed data

    Examples:
        >>> process_data([1, 2, 3])
        [2, 4, 6]

        >>> process_data([1, 2, 3], method='minimal')
        [1, 2, 3]
    """
    if method == 'standard':
        return [x * 2 for x in data]
    elif method == 'minimal':
        return data
    # ... etc
```

### 3. Testing Strategy

**Test coverage:**
- Test normal cases
- Test edge cases
- Test error conditions

```python
#| export
def safe_divide(a, b):
    """Safely divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Normal cases
test_eq(safe_divide(10, 2), 5)
test_eq(safe_divide(9, 3), 3)

# Edge cases
test_close(safe_divide(1, 3), 0.333, eps=0.001)
test_eq(safe_divide(0, 5), 0)

# Error cases
test_fail(lambda: safe_divide(5, 0), contains="divide by zero")
```

### 4. Modular Design

**Separate concerns:**
- Core functionality in `00_core.ipynb`
- Utilities in `01_utils.ipynb`
- Specific features in separate notebooks

**Example:**
```python
# 00_core.ipynb
#| default_exp core
#| export
class BaseModel:
    """Base model class"""
    pass

# 10_models.ipynb
#| default_exp models
from mypackage.core import BaseModel

#| export
class SpecificModel(BaseModel):
    """Specific implementation"""
    pass
```

### 5. Documentation First

Write documentation while developing:

1. Write explanation of what you want to build
2. Write function signature and docstring
3. Write examples and tests
4. Implement the function

This ensures good documentation and clear thinking.

### 6. Version Control

**Commit workflow:**
```bash
# After making changes
nbdev_prepare              # Export, test, clean, update README
git add .
git commit -m "Add new feature"
git push
```

**Before merging:**
```bash
nbdev_test                # Ensure all tests pass
nbdev_clean               # Clean notebooks
```

### 7. Continuous Integration

Let CI/CD do the work:
- Tests run on every push
- Docs deploy automatically
- Releases can be automated

Review the `.github/workflows/deploy.yaml` file.

### 8. Package Configuration

Edit `settings.ini` for package metadata:

```ini
[DEFAULT]
repo = repo-name
lib_name = package_name
version = 0.0.1
min_python = 3.7
license = apache2
black_formatting = True

description = A short description
author = Your Name
author_email = you@email.com
copyright = Your Name
keywords = keyword1 keyword2
user = github-username

requirements = numpy pandas
dev_requirements = matplotlib pytest

nbs_path = nbs
doc_path = _docs
```

---

## Complete Examples

### Example 1: Simple Math Library

**File: `nbs/00_core.ipynb`**

```python
#| default_exp core
```

```markdown
# Core Math Functions

> Basic mathematical operations
```

```python
#| export
def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    Examples:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
    """
    return a + b

#| export
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b

    Examples:
        >>> multiply(4, 5)
        20
        >>> multiply(-2, 3)
        -6
    """
    return a * b
```

```python
# Tests
from fastcore.test import test_eq

test_eq(add(2, 3), 5)
test_eq(add(-1, 1), 0)
test_eq(add(0, 0), 0)

test_eq(multiply(4, 5), 20)
test_eq(multiply(-2, 3), -6)
test_eq(multiply(0, 100), 0)
```

```markdown
## Calculator Class

A simple calculator that maintains state.
```

```python
#| export
class Calculator:
    """A simple calculator with memory."""

    def __init__(self):
        """Initialize calculator with result = 0"""
        self.result = 0

    def add(self, x: float) -> float:
        """Add x to result"""
        self.result += x
        return self.result

    def multiply(self, x: float) -> float:
        """Multiply result by x"""
        self.result *= x
        return self.result

    def reset(self):
        """Reset result to 0"""
        self.result = 0
```

```python
# Test Calculator
calc = Calculator()
test_eq(calc.add(5), 5)
test_eq(calc.add(3), 8)
test_eq(calc.multiply(2), 16)
calc.reset()
test_eq(calc.result, 0)
```

### Example 2: Data Processing Library

**File: `nbs/01_data.ipynb`**

```python
#| default_exp data
```

```markdown
# Data Processing

> Tools for processing and transforming data
```

```python
#| export
from typing import List, Callable
import numpy as np

def transform(data: List[float], func: Callable) -> List[float]:
    """Apply function to each element.

    Args:
        data: Input data
        func: Function to apply

    Returns:
        Transformed data

    Examples:
        >>> transform([1, 2, 3], lambda x: x * 2)
        [2, 4, 6]
    """
    return [func(x) for x in data]

#| export
def normalize(data: List[float]) -> List[float]:
    """Normalize data to [0, 1] range.

    Args:
        data: Input data

    Returns:
        Normalized data

    Examples:
        >>> normalize([0, 50, 100])
        [0.0, 0.5, 1.0]
    """
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val

    if range_val == 0:
        return [0.0] * len(data)

    return [(x - min_val) / range_val for x in data]
```

```python
# Tests
from fastcore.test import test_eq, test_close

test_eq(transform([1, 2, 3], lambda x: x * 2), [2, 4, 6])
test_eq(transform([1, 2, 3], lambda x: x + 1), [2, 3, 4])

normalized = normalize([0, 50, 100])
test_close(normalized, [0.0, 0.5, 1.0], eps=0.001)

# Edge case: all same values
test_eq(normalize([5, 5, 5]), [0.0, 0.0, 0.0])
```

### Example 3: Complete Project Setup

**Step 1: Create Project**

```bash
# Create GitHub repo
gh repo create mymath --public

# Clone and initialize
git clone https://github.com/username/mymath.git
cd mymath
nbdev_new

# Answer prompts:
# - Package: mymath
# - Description: Mathematical utilities
# - Author: Your Name
# - Email: you@email.com
# - License: Apache 2.0

# Setup
nbdev_install_hooks
pip install -e '.[dev]'
```

**Step 2: Create Notebooks**

`nbs/index.ipynb`:
```python
# mymath

> A collection of mathematical utilities

This project provides efficient mathematical operations.

## Install

```sh
pip install mymath
```

## How to use

```python
from mymath.core import add, multiply

add(2, 3)  # 5
multiply(4, 5)  # 20
```
```

`nbs/00_core.ipynb`: (as shown in Example 1)

**Step 3: Develop and Test**

```bash
# Export notebooks
nbdev_export

# Run tests
nbdev_test

# Preview docs
nbdev_preview
```

**Step 4: Commit and Push**

```bash
nbdev_prepare
git add .
git commit -m "Initial implementation"
git push
```

**Step 5: Release**

```bash
# Update version in settings.ini to 0.0.1
# Update CHANGELOG.md

nbdev_prepare
git add .
git commit -m "Release v0.0.1"
git tag v0.0.1
git push --tags

# Build and publish
python -m build
twine upload dist/*
```

---

## Troubleshooting

### Common Issues

**Issue: "No module named 'mypackage'"**

Solution:
```bash
pip install -e '.[dev]'
nbdev_export
```

**Issue: Tests failing**

Solution:
```bash
# Run tests with verbose output
nbdev_test --verbose

# Test specific notebook
nbdev_test --path nbs/00_core.ipynb
```

**Issue: Documentation not building**

Solution:
```bash
# Ensure Quarto is installed
quarto --version

# Rebuild docs
nbdev_docs
```

**Issue: Git merge conflicts**

Solution:
- nbdev hooks make conflicts readable
- Resolve in notebook interface or editor
- Run `nbdev_clean` after resolving

**Issue: Import errors in notebooks**

Solution:
```bash
# Make sure package is installed
pip install -e '.[dev]'

# Restart Jupyter kernel
```

---

## Advanced Topics

### Custom Export Behavior

Modify `settings.ini`:
```ini
# Custom module path
lib_path = src/mypackage

# Black formatting
black_formatting = True

# Custom doc path
doc_path = documentation
```

### Multiple Languages

Use Quarto's multilang support:
```yaml
# _quarto.yml
project:
  type: website

format:
  html:
    code-tools: true
    code-fold: show
```

### Private Packages

For private packages:
1. Use private GitHub repo
2. Configure PyPI credentials
3. Set up private package index

### Monorepo Setup

Multiple packages in one repo:
```
repo/
├── package1/
│   └── nbs/
├── package2/
│   └── nbs/
└── shared/
    └── nbs/
```

---

## Resources

### Official Resources
- **Documentation**: https://nbdev.fast.ai/
- **GitHub**: https://github.com/AnswerDotAI/nbdev
- **Tutorial**: https://nbdev.fast.ai/tutorials/
- **Examples**: fastai, fastcore, execnb libraries

### Community
- **Forum**: https://forums.fast.ai/
- **Discord**: Fast.ai community

### Related Tools
- **Quarto**: Documentation generation
- **fastcore**: Utilities used by nbdev
- **execnb**: Notebook execution engine

### Notable Projects Using nbdev
- **fastai**: Deep learning library
- **fastcore**: Python utilities
- **ghapi**: GitHub API wrapper
- **execnb**: Execute notebooks programmatically

---

**End of nbdev Comprehensive Reference**

*This documentation covers notebook-driven development with nbdev, from project setup to publishing packages. Designed for offline LLM use during development.*
