# 🏄‍♂️ Windsurf Agent Starter Template

*Version: 1.0.0*  
*Last Updated: 2025-06-20*  
*Maintainer: Prometheus*

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Tests](https://github.com/promprot/windsurf-starter-template/actions/workflows/ci.yml/badge.svg)](https://github.com/promprot/windsurf-starter-template/actions)
[![codecov](https://codecov.io/gh/promprot/windsurf-starter-template/branch/main/graph/badge.svg?token=YOUR-TOKEN)](https://codecov.io/gh/promprot/windsurf-starter-template)

A production-ready template for creating AI agents with the Windsurf framework. This template includes everything you need to build, test, secure, and deploy a robust AI agent with tools, memory, and MCP server integration.

## 🆕 What's New in v1.0.0

- **Enhanced Configuration System**: Pydantic-based configuration with environment variable overrides
- **Improved Security**: Built-in security scanning and dependency vulnerability checks
- **Better Developer Experience**: Comprehensive type hints and improved error handling
- **Production-Ready**: Health checks, metrics, and graceful shutdown
- **CI/CD Pipeline**: Automated testing, security scanning, and dependency updates

## ✨ Features

- 🛠️ **Tool System**: Easily extend agent capabilities with custom tools
- ⚙️ **Configuration**: Pydantic-based settings with environment variable overrides
- 🔒 **Security**: Built-in security scanning and dependency checks
- 🧠 **Memory**: Built-in support for persistent memory
- 🔌 **MCP Integration**: Pre-configured with essential MCP servers
- 🧪 **Testing**: Comprehensive test suite with pytest (unit + integration)
- 🚀 **Production Ready**: Health checks, metrics, and graceful shutdown
- 🔄 **CI/CD**: Automated testing, security scanning, and dependency updates
- 📦 **Packaging**: Ready for PyPI distribution
- 📚 **Documentation**: Complete developer and API documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/promprot/windsurf-starter-template.git
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
   # For production
   pip install -r requirements.txt
   
   # For development (includes testing and documentation tools)
   pip install -r requirements-dev.txt
   ```

4. Configure your environment:
   ```bash
   # Copy and edit the example configuration
   cp .windsurf/agent_settings.example.json .windsurf/agent_settings.json
   cp .env.example .env
   
   # Edit the configuration files as needed
   # .windsurf/agent_settings.json - Agent configuration
   # .env - Environment variables (API keys, etc.)
   ```

5. (Optional) Run the agent locally:
   ```bash
   python -m src.main
   ```
   
   The agent will be available at `http://localhost:8080` with the following endpoints:
   - `GET /health` - Health check
   - `GET /metrics` - Prometheus metrics (if enabled)
   - `POST /process` - Process agent requests

## 🏗️ Project Structure

```
.
├── .github/                  # GitHub workflows and issue templates
│   └── workflows/            # CI/CD pipelines
│   └── ISSUE_TEMPLATE/       # GitHub issue templates
├── .windsurf/                # Windsurf configuration
│   ├── agent_settings.json   # Agent configuration
│   └── mcp_config.json       # MCP server configuration
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # System architecture
│   ├── API_REFERENCE.md      # API documentation
│   ├── DEVELOPMENT.md        # Development guide
│   └── DEPLOYMENT.md         # Deployment guide
├── src/                      # Source code
│   ├── config.py            # Pydantic configuration models
│   ├── main.py              # Main application entry point
│   └── tools/               # Custom tools
│       └── example_tool.py  # Example tool implementation
└── tests/                   # Test suite
    ├── conftest.py          # Test configuration
    ├── unit/               # Unit tests
    └── integration/        # Integration tests
        └── test_agent_integration.py
```

## 🛠️ Creating a New Tool

1. Create a new Python file in `src/tools/`
2. Implement your tool following the example in `src/tools/example_tool.py`
3. The tool will be automatically discovered and loaded by the agent

Example tool structure:

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class MyToolConfig:
    """Configuration for MyTool."""
    param1: str = "default"
    param2: int = 42

class MyTool:
    """Documentation for your tool."""
    
    name = "my_tool"
    description = "Description of what this tool does"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = MyToolConfig(**(config or {}))
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with the given input."""
        try:
            # Your tool logic here
            return {
                "status": "success",
                "result": "Tool execution result"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def cleanup(self) -> None:
        """Clean up any resources used by the tool."""
        pass
```

## 🧪 Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run unit tests only:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```

Run with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

### Security Scanning

The CI pipeline includes several security checks:

- **Bandit**: Static code analysis for security issues
- **Safety**: Check for known vulnerable dependencies
- **TruffleHog**: Scan for accidentally committed secrets

To run security checks locally:

```bash
# Install security tools
pip install bandit safety trufflehog

# Run Bandit
bandit -r src/

# Run Safety (requires API key for full scan)
safety check

# Run TruffleHog
trufflehog --max_depth 50 --entropy=False --regex .
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on every push and pull request. The pipeline includes:

1. **Linting**: Black, isort, flake8, mypy
2. **Testing**: Unit and integration tests with coverage reporting
3. **Security Scanning**: Bandit, Safety, TruffleHog
4. **Dependency Updates**: Weekly check for outdated dependencies

## 📦 Deployment

The agent can be deployed in several ways:

### Local Development

```bash
python -m src.main
```

### Docker

```bash
# Build the image
docker build -t windsurf-agent .

# Run the container
docker run -p 8080:8080 -v $(pwd)/.windsurf:/app/.windsurf windsurf-agent
```

### Kubernetes

Example deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: windsurf-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: windsurf-agent
  template:
    metadata:
      labels:
        app: windsurf-agent
    spec:
      containers:
      - name: windsurf-agent
        image: your-registry/windsurf-agent:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: windsurf-config
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
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
- [Pydantic](https://pydantic-docs.helpmanual.io/) for awesome data validation
- [aiohttp](https://docs.aiohttp.org/) for async HTTP server
- [pytest](https://docs.pytest.org/) for testing
- [GitHub Actions](https://github.com/features/actions) for CI/CD
- All contributors who have helped improve this template

## Changelog

### [0.1.0] - 2025-06-20
#### Added
- Initial project setup
- Basic agent implementation
- Example tool with tests
- CI/CD pipeline
- Documentation structure

#### Changed
- Updated README to follow new documentation standards

#### Removed
- N/A
