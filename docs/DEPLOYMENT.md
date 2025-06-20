# Deployment Guide

*Version: 1.0.0*  
*Last Updated: 2025-06-20*  
*Maintainer: Red Team*

## Overview
This guide provides comprehensive instructions for deploying the Windsurf Agent Starter Template in various environments, including local development, Docker, and Kubernetes. For more information, see the [official documentation](https://docs.windsurf.com).

## Changelog

### [1.0.0] - 2025-06-20
#### Added
- Initial deployment guide
- Local deployment instructions
- Docker deployment guide
- Kubernetes deployment guide
- Environment variables reference
- Monitoring information

#### Changed
- Updated to follow new documentation standards

#### Removed
- N/A

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git
- (Optional) Docker and Docker Compose

## Local Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/windsurf-starter-template.git
cd windsurf-starter-template
```

### 2. Set Up Environment

Create and activate a virtual environment:

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On Unix or MacOS
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update it with your configuration:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run the Agent

```bash
python -m src.main
```

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t windsurf-agent .
```

### 2. Run the Container

```bash
docker run -d --name windsurf-agent \
  -p 8000:8000 \
  --env-file .env \
  windsurf-agent
```

## Kubernetes Deployment

### 1. Create a Kubernetes Secret

```bash
kubectl create secret generic windsurf-secrets --from-env-file=.env
```

### 2. Deploy the Application

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `MEMORY_ENABLED` | Enable memory | No | `true` |
| `MEMORY_PERSISTENCE` | Enable memory persistence | No | `true` |
| `AUTH_REQUIRED` | Require authentication | No | `true` |
| `API_KEY` | API key for authentication | If `AUTH_REQUIRED=true` | - |

## Monitoring

The agent exposes the following endpoints for monitoring:

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## Logging

Logs are written to `stdout` in JSON format. You can configure the log level using the `LOG_LEVEL` environment variable.

## Backup and Recovery

### Backing Up Memory

If memory persistence is enabled, the memory is stored in `.windsurf/memory.json`. To back it up:

```bash
cp .windsurf/memory.json memory_backup_$(date +%Y%m%d).json
```

### Restoring from Backup

To restore from a backup:

```bash
cp memory_backup_20230620.json .windsurf/memory.json
```

## Upgrading

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Restart the agent.
