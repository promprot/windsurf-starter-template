# Windsurf Agent Starter Template

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A production-ready template for creating AI agents with the Windsurf framework. This template includes everything you need to build, test, and deploy a robust AI agent with tools, memory, and MCP server integration.

## ✨ Features

- 🛠️ **Tool System**: Easily extend agent capabilities with custom tools
- 🧠 **Memory**: Built-in support for persistent memory
- 🔌 **MCP Integration**: Pre-configured with essential MCP servers
- 🧪 **Testing**: Comprehensive test suite with pytest
- 🚀 **Production Ready**: CI/CD, linting, and type checking out of the box
- 📦 **Packaging**: Ready for PyPI distribution
- 📚 **Documentation**: Complete developer and API documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/windsurf-starter-template.git
   cd windsurf-starter-template
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\\venv\\Scripts\\activate
   
   # On Unix or MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and update it with your configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🏗️ Project Structure

```
.
├── .github/              # GitHub workflows and templates
├── .windsurf/            # Windsurf configuration
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md   # System architecture
│   ├── API_REFERENCE.md  # API documentation
│   ├── DEVELOPMENT.md    # Development guide
│   └── DEPLOYMENT.md     # Deployment guide
├── src/                  # Source code
│   ├── agents/          # Agent implementations
│   ├── tools/           # Custom tools
│   └── utils/           # Utility functions
└── tests/               # Test suite
    ├── unit/           # Unit tests
    ├── integration/    # Integration tests
    └── fixtures/       # Test fixtures
```

## 🛠️ Creating a New Tool

1. Create a new Python file in `src/tools/`
2. Implement your tool following the example in `src/tools/example_tool.py`
3. The tool will be automatically discovered and loaded by the agent

## 🧪 Running Tests

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## 🚀 Running the Agent

Start the agent in interactive mode:

```bash
python -m src.main
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Windsurf](https://windsurf.com) for the amazing framework
- All contributors who have helped improve this template
