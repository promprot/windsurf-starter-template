# Sequential Thinking MCP Guide

## Table of Contents
1. [Overview](#overview)
2. [Setup and Configuration](#setup-and-configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Patterns](#advanced-patterns)
5. [Best Practices](#best-practices)
6. [Performance Considerations](#performance-considerations)
7. [Troubleshooting](#troubleshooting)

## Overview
The Sequential Thinking MCP enables complex reasoning and multi-step problem solving by breaking down tasks into manageable steps.

### Key Features
- Step-by-step reasoning
- State management
- Backtracking support
- Parallel execution
- Progress tracking

## Setup and Configuration

### Installation
```bash
npm install @modelcontextprotocol/server-sequential-thinking
```

### Configuration
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking@latest"],
      "env": {
        "MAX_STEPS": "50",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

## Basic Usage

### Creating a Simple Plan
```python
# Define a plan
plan = {
    "goal": "Generate a report on user activity",
    "steps": [
        "Fetch user data from the database",
        "Calculate daily active users",
        "Generate visualization",
        "Write summary"
    ]
}

# Execute the plan
result = await sequential_thinking.execute_plan(plan)
```

### Handling Step Results
```python
async def process_step(step, context):
    if step == "Fetch user data":
        return await fetch_from_database()
    elif step == "Calculate metrics":
        return calculate_metrics(context["user_data"])
    # ...

result = await sequential_thinking.execute_plan(plan, process_step)
```

## Advanced Patterns

### Conditional Execution
```python
plan = {
    "goal": "Process user upload",
    "steps": [
        "Validate file format",
        {
            "if": "is_valid_format",
            "then": ["Process file", "Generate report"],
            "else": ["Log error", "Notify user"]
        }
    ]
}
```

### Parallel Execution
```python
plan = {
    "goal": "Gather system metrics",
    "parallel": [
        "Get CPU usage",
        "Get memory usage",
        "Get disk space"
    ],
    "then": "Aggregate results"
}
```

### Error Handling
```python
plan = {
    "goal": "Data pipeline",
    "steps": [
        "Extract data",
        "Transform data",
        "Load data"
    ],
    "on_error": {
        "retry": 3,
        "fallback": "Use cached data"
    }
}
```

## Best Practices

### Planning
1. Define clear, atomic steps
2. Keep steps focused on a single task
3. Consider error cases and edge cases
4. Plan for retries and fallbacks

### Error Handling
- Use try/except blocks in step handlers
- Implement proper logging
- Consider idempotency

### Performance
- Use parallel execution when possible
- Cache expensive operations
- Monitor step durations

## Performance Considerations

### Memory Usage
- Break large plans into smaller sub-plans
- Clean up resources after each step
- Monitor memory usage

### Timeouts
- Set reasonable timeouts for steps
- Implement progress tracking
- Handle long-running steps appropriately

## Troubleshooting

### Common Issues

1. **Plan not progressing**
   - Check for infinite loops
   - Verify step completion
   - Review logs for errors

2. **Memory leaks**
   - Monitor memory usage
   - Clean up resources
   - Consider pagination for large datasets

3. **Performance issues**
   - Profile slow steps
   - Consider parallel execution
   - Optimize expensive operations

### Monitoring
```python
# Get plan status
status = await sequential_thinking.get_plan_status(plan_id)

# Get execution metrics
metrics = await sequential_thinking.get_metrics()
```

## Integration with Windsurf

### Configuration
```json
{
  "windsurf": {
    "sequential_thinking": {
      "enabled": true,
      "max_steps": 100,
      "timeout": 300000
    }
  }
}
```

### Usage with Windsurf
```python
# Create a plan for code analysis
plan = {
    "goal": "Analyze code quality",
    "steps": [
        "Run linter",
        "Run tests",
        "Generate coverage report",
        "Check for security issues"
    ]
}

# Execute and track progress
async def on_progress(step, result):
    await memory.set(f"analysis:step:{step}", result)

result = await sequential_thinking.execute_plan(
    plan,
    progress_callback=on_progress
)
```

## Example: Code Review Workflow

```python
async def code_review(pr_id):
    plan = {
        "goal": f"Review PR #{pr_id}",
        "steps": [
            "Fetch PR details",
            "Run static analysis",
            "Check test coverage",
            "Review documentation",
            "Check for security issues",
            "Generate review comments"
        ]
    }
    
    async def execute_step(step, context):
        if step == "Fetch PR details":
            return await github.get_pr(pr_id)
        elif step == "Run static analysis":
            return await run_analysis(context["pr"]["files"])
        # ... other steps ...
    
    return await sequential_thinking.execute_plan(plan, execute_step)
```

## Example: Data Processing Pipeline

```python
async def process_data_pipeline(dataset_id):
    plan = {
        "goal": f"Process dataset {dataset_id}",
        "steps": [
            "Validate input data",
            "Clean data",
            "Transform features",
            "Train model",
            "Evaluate performance",
            "Generate report"
        ],
        "on_error": {
            "retry": 2,
            "fallback": "Use previous model"
        }
    }
    
    return await sequential_thinking.execute_plan(plan)
```
