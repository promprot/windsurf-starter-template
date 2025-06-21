# Memory MCP Guide

## Table of Contents
1. [Overview](#overview)
2. [Setup and Configuration](#setup-and-configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Patterns](#advanced-patterns)
5. [Best Practices](#best-practices)
6. [Performance Considerations](#performance-considerations)
7. [Troubleshooting](#troubleshooting)

## Overview
The Memory MCP provides persistent key-value storage for your application, allowing you to store and retrieve data across sessions.

### Key Features
- Persistent key-value storage
- Namespace support
- TTL (Time To Live) for entries
- Atomic operations

## Setup and Configuration

### Installation
```bash
npm install @modelcontextprotocol/server-memory
```

### Configuration
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory@latest"],
      "env": {
        "MEMORY_FILE_PATH": "./.windsurf/memory.json",
        "MEMORY_MAX_ENTRIES": "500",
        "LOG_LEVEL": "warn"
      }
    }
  }
}
```

## Basic Usage

### Storing Data
```python
# Store a simple value
await memory.set("user:123:name", "John Doe")

# Store with TTL (1 hour)
await memory.set("user:123:session", session_data, ttl=3600)

# Store complex data
user_data = {
    "name": "John Doe",
    "preferences": {"theme": "dark", "notifications": True},
    "last_active": "2023-10-25T10:30:00Z"
}
await memory.set("user:123:profile", user_data)
```

### Retrieving Data
```python
# Get a value
name = await memory.get("user:123:name")

# Get with default value
theme = await memory.get("user:123:theme", "light")

# Check if key exists
if await memory.exists("user:123:preferences"):
    prefs = await memory.get("user:123:preferences")
```

### Deleting Data
```python
# Delete a key
await memory.delete("user:123:session")

# Clear all data (use with caution)
await memory.clear()
```

## Advanced Patterns

### Namespaces
```python
# Using namespaces
user_ns = memory.namespace("user:123")
await user_ns.set("preferences", {"theme": "dark"})
prefs = await user_ns.get("preferences")
```

### Atomic Operations
```python
# Atomic increment
new_count = await memory.incr("page:views:home")

# Atomic list operations
await memory.lpush("user:123:activity", "login")
await memory.rpush("user:123:activity", "view_page")
activities = await memory.lrange("user:123:activity", 0, -1)
```

### Transactions
```python
async with memory.transaction() as txn:
    txn.set("user:123:balance", 100)
    txn.decr("user:123:balance", 10)
    # Changes are committed when the block exits successfully
```

## Best Practices

### Key Naming
- Use colons (`:`) for hierarchy (e.g., `user:123:profile`)
- Be consistent with key patterns
- Avoid special characters in keys

### Data Organization
- Group related data under namespaces
- Use appropriate data structures (strings, hashes, lists)
- Set reasonable TTLs for temporary data

### Error Handling
```python
try:
    data = await memory.get("important:data")
    if data is None:
        # Handle missing data
        pass
except Exception as e:
    # Handle errors
    logger.error(f"Memory operation failed: {e}")
```

## Performance Considerations

### Batch Operations
```python
# Instead of multiple gets
user_data = await memory.mget([
    "user:123:name",
    "user:123:email",
    "user:123:prefs"
])

# Instead of multiple sets
await memory.mset({
    "user:123:name": "John",
    "user:123:email": "john@example.com"
})
```

### Memory Management
- Set appropriate `MEMORY_MAX_ENTRIES`
- Monitor memory usage
- Clean up old data

## Troubleshooting

### Common Issues

1. **Data not persisting**
   - Check `MEMORY_FILE_PATH` permissions
   - Verify the process has write access

2. **Performance issues**
   - Check for large values
   - Look for unbounded growth

3. **Connection issues**
   - Verify MCP server is running
   - Check logs for errors

### Monitoring
```bash
# Get memory stats
stats = await memory.info()
print(f"Used memory: {stats['used_memory']}")
print(f"Total keys: {stats['total_keys']}")
```

### Logs
Set `LOG_LEVEL=debug` for detailed logs during development.

## Integration with Windsurf

### Configuration
```json
{
  "windsurf": {
    "memory": {
      "enabled": true,
      "persist": true,
      "path": "./.windsurf/memory"
    }
  }
}
```

### Usage with Windsurf
```python
# Store editor state
async def save_editor_state(file_path, cursor_pos, selections):
    await memory.set(f"editor:{file_path}:cursor", cursor_pos)
    await memory.set(f"editor:{file_path}:selections", selections)

# Restore editor state
async def restore_editor_state(file_path):
    cursor_pos = await memory.get(f"editor:{file_path}:cursor")
    selections = await memory.get(f"editor:{file_path}:selections", [])
    return cursor_pos, selections
```

## Example: User Preferences
```python
class UserPreferences:
    def __init__(self, user_id):
        self.ns = memory.namespace(f"user:{user_id}:prefs")
    
    async def get_theme(self):
        return await self.ns.get("theme", "system")
    
    async def set_theme(self, theme):
        await self.ns.set("theme", theme)
    
    async def get_notifications(self):
        return await self.ns.get("notifications", True)
    
    async def set_notifications(self, enabled):
        await self.ns.set("notifications", bool(enabled))

# Usage
prefs = UserPreferences("123")
await prefs.set_theme("dark")
theme = await prefs.get_theme()
```
