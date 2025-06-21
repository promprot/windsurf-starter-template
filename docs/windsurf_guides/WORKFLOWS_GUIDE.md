# Windsurf Workflows Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Workflow Types](#workflow-types)
4. [Creating Custom Workflows](#creating-custom-workflows)
5. [Best Practices](#best-practices)
6. [Common Workflow Examples](#common-workflow-examples)
7. [Troubleshooting](#troubleshooting)

## Overview
Windsurf Workflows automate repetitive tasks in your development process, from code formatting to deployment. This guide covers how to create, manage, and optimize workflows in your Windsurf environment.

## Getting Started

### Prerequisites
- Windsurf CLI installed
- Node.js 16+ and npm/yarn
- Git repository initialized

### Basic Configuration
Create `.windsurf/workflows` directory:
```bash
mkdir -p .windsurf/workflows
```

### Your First Workflow
Create `.windsurf/workflows/hello-world.yml`:
```yaml
name: Hello World
on: [push, pull_request]

jobs:
  greet:
    name: Greet the user
    runs-on: ubuntu-latest
    steps:
      - name: Say hello
        run: echo "Hello, ${{ github.actor }}!"
```

## Workflow Types

### 1. Local Development Workflows
Run on your machine during development.

**Example**: Pre-commit hooks
```yaml
# .windsurf/workflows/pre-commit.yml
name: Pre-commit

on: pre-commit

jobs:
  lint:
    name: Lint and format
    runs-on: local
    steps:
      - name: Run linter
        run: npm run lint
      - name: Run formatter
        run: npm run format
```

### 2. CI/CD Workflows
Run on your CI/CD pipeline.

**Example**: Test and Build
```yaml
# .windsurf/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
```

### 3. Scheduled Workflows
Run on a schedule.

**Example**: Daily Dependency Updates
```yaml
# .windsurf/workflows/daily-update.yml
name: Daily Update

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update dependencies
        run: |
          npm update
          npm test
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add package*.json
          git commit -m 'chore(deps): update dependencies'
          git push
```

## Creating Custom Workflows

### 1. Workflow Structure
```yaml
name: Workflow Name

# When to run the workflow
on: [push, pull_request]

# Environment variables
env:
  NODE_ENV: test

# Jobs to run
jobs:
  job-name:
    name: Job Name
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "Running step 1"
      - name: Step 2
        run: echo "Running step 2"
```

### 2. Using Actions
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
```

### 3. Matrix Builds
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [14.x, 16.x, 18.x]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

## Best Practices

### 1. Workflow Organization
- Keep workflows small and focused
- Use descriptive names
- Group related jobs
- Reuse workflows when possible

### 2. Performance
- Cache dependencies
- Run jobs in parallel when possible
- Use matrix builds for multiple configurations
- Set appropriate timeouts

### 3. Security
- Use secrets for sensitive data
- Limit permissions
- Use official actions
- Pin action versions

## Common Workflow Examples

### 1. Node.js Project
```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    - run: npm ci
    - run: npm test
    - run: npm run build --if-present
```

### 2. Docker Build and Push
```yaml
name: Docker Build

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: user/app:latest,user/app:${{ github.sha }}
```

### 3. Deploy to AWS
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - name: Deploy to S3
        run: |
          aws s3 sync ./dist s3://my-bucket/ --delete
```

## Advanced Features

### 1. Reusable Workflows
Create `.github/workflows/reusable.yml`:
```yaml
name: Reusable Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm test
```

Use it in another workflow:
```yaml
name: Use Reusable Workflow

on: [push, pull_request]

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable.yml
    with:
      node-version: '18'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 2. Self-hosted Runners
```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test
```

### 3. Caching
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      - run: npm ci
      - run: npm test
```

## Troubleshooting

### Common Issues

1. **Workflow not running**
   - Check YAML syntax
   - Verify the `on` conditions
   - Check branch protection rules

2. **Permission errors**
   - Check workflow permissions
   - Verify token scopes
   - Check repository settings

3. **Dependency issues**
   - Clear cache
   - Update lockfiles
   - Check for version conflicts

### Debugging
```yaml
- name: Debug information
  run: |
    echo "Branch: ${{ github.ref }}"
    echo "Event: ${{ github.event_name }}"
    echo "SHA: ${{ github.sha }}"
    env
```

### Logs
- View workflow runs in the Actions tab
- Download logs for failed jobs
- Enable debug logging with `ACTIONS_STEP_DEBUG`

## Integration with Other Tools

### 1. Slack Notifications
```yaml
- name: Send Slack notification
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
    STATUS: ${{ job.status }}
```

### 2. Code Coverage
```yaml
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
```

### 3. Security Scanning
```yaml
- name: Run security scan
  uses: snyk/actions/node@master
  with:
    command: monitor
    args: --org=my-org --project-name=my-project
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Monitoring and Maintenance

### 1. Workflow Metrics
- Track workflow duration
- Monitor success rates
- Set up alerts for failures

### 2. Cost Optimization
- Use smaller runners when possible
- Cache dependencies
- Clean up old artifacts

### 3. Regular Updates
- Update actions to latest versions
- Review and optimize workflows
- Remove unused workflows
