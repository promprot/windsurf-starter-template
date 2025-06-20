# Architecture Overview

## System Components

### 1. Core Agent
- **Entry Point**: `src/main.py`
- **Responsibility**: Main execution flow and coordination
- **Dependencies**: Tools, Memory, MCP Servers

### 2. Tools
- **Location**: `src/tools/`
- **Purpose**: Extend agent capabilities
- **Auto-discovery**: Enabled via `agent_settings.json`

### 3. MCP Servers
- **Configuration**: `.windsurf/mcp_config.json`
- **Default Servers**:
  - Memory Server
  - Filesystem Server
  - GitHub MCP Server
  - Sequential Thinking Server

## Data Flow

```mermaid
graph TD
    A[User Request] --> B[Core Agent]
    B --> C[Tool Selection]
    C --> D[Execute Tool]
    D --> E[Memory Update]
    E --> F[Response Generation]
    F --> G[User Response]
```

## Security Considerations

- All sensitive data is stored in environment variables
- Tools run in isolated environments
- Memory persistence is configurable
- API authentication is required
