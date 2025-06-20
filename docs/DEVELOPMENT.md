# Development Guide

*Version: 1.0.0*  
*Last Updated: 2025-06-20*  
*Maintainer: Red Team*

## Overview
This guide provides comprehensive instructions for setting up a development environment, understanding the project structure, and contributing to the Windsurf Agent Starter Template.

## Getting Started

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git
- (Optional) Docker for MCP servers

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/windsurf-starter-template.git
   cd windsurf-starter-template
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r tests/requirements.txt  # Test dependencies
   ```

## Project Structure

```
.
├── .github/              # GitHub workflows and templates
├── .windsurf/            # Windsurf configuration
├── docs/                 # Documentation
├── src/                  # Source code
│   ├── agents/          # Agent implementations
│   ├── tools/           # Custom tools
│   └── utils/           # Utility functions
└── tests/               # Test suite
```

## Creating a New Tool

1. Create a new Python file in `src/tools/`
2. Implement the tool class:
   ```python
   from typing import Dict, Any
   
   class ExampleTool:
       name = "example_tool"
       description = "An example tool that does something useful"
       
       def __init__(self, config=None):
           self.config = config or {}
       
       async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
           """
           Execute the tool with the given input.
           
           Args:
               input_data: Dictionary containing input parameters
               
           Returns:
               Dictionary containing the result
           """
           # Your implementation here
           return {"result": "success"}
   ```

3. The tool will be automatically discovered and loaded by the agent.

## Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

## Changelog

### [1.0.0] - 2025-06-20
#### Added
- Initial development guide
- Setup instructions
- Project structure overview
- Tool creation guide
- Testing procedures
- Code style guidelines

#### Changed
- Updated to follow new documentation standards

#### Removed
- N/A

To format and check your code:

```bash
black .
isort .
flake8 .
mypy .
```

## Version Control

We follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Example:
```
feat(tools): add new example tool

Adds a new example tool that demonstrates tool creation.

Closes #123
```

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Update documentation if needed
4. Add tests for new features
5. Run tests and linters
6. Submit a pull request
