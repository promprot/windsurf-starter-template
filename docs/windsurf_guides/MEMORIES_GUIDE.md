# Windsurf Memories Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Memory Types](#memory-types)
4. [Advanced Usage](#advanced-usage)
5. [Best Practices](#best-practices)
6. [Common Use Cases](#common-use-cases)
7. [Troubleshooting](#troubleshooting)

## Overview
Windsurf Memories provide persistent storage and retrieval of information across sessions, enabling context-aware assistance and personalized experiences.

## Getting Started

### Enabling Memories
In your `.windsurf/config.json`:

```json
{
  "memories": {
    "enabled": true,
    "persist": true,
    "path": ".windsurf/memories"
  }
}
```

### Basic Usage
```javascript
// Save a memory
await memories.create({
  type: 'preference',
  key: 'theme',
  value: 'dark',
  tags: ['ui', 'preferences']
});

// Retrieve a memory
const theme = await memories.get('preference:theme');
```

## Memory Types

### 1. User Preferences
```javascript
await memories.setPreference('theme', 'dark');
const theme = await memories.getPreference('theme', 'light');
```

### 2. Context Memories
```javascript
// Save context from current conversation
await memories.saveContext({
  file: 'src/index.js',
  cursor: { line: 42, column: 10 },
  context: 'Working on authentication flow'
});

// Get relevant context
const context = await memories.getContext('src/index.js');
```

### 3. Code Snippets
```javascript
// Save a code snippet
await memories.createSnippet({
  name: 'api-client',
  code: 'class ApiClient { /* ... */ }',
  language: 'javascript',
  tags: ['http', 'client']
});

// Find snippets by tag
const httpSnippets = await memories.findSnippets({ tags: ['http'] });
```

## Advanced Usage

### Memory Search
```javascript
// Full-text search
const results = await memories.search({
  query: 'authentication',
  types: ['snippet', 'context'],
  limit: 5
});

// Vector similarity search
const similar = await memories.findSimilar(
  'How to handle auth tokens',
  { type: 'snippet' }
);
```

### Memory Expiration
```javascript
// Memory that expires in 24 hours
await memories.create({
  type: 'temporary',
  key: 'session:123',
  value: { /* session data */ },
  expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000)
});
```

### Memory Hooks
```javascript
// Add a hook before saving
memories.beforeCreate(async (memory) => {
  // Validate or transform memory
  if (memory.type === 'snippet') {
    memory.language = memory.language || 'javascript';
  }
  return memory;
});

// Add a hook after retrieval
memories.afterGet(async (memory) => {
  // Add additional context
  if (memory.type === 'preference') {
    memory.lastAccessed = new Date();
  }
  return memory;
});
```

## Best Practices

### 1. Memory Organization
- Use consistent naming conventions
- Group related memories with tags
- Use namespaces for different contexts
- Set appropriate expiration times

### 2. Performance
- Batch memory operations when possible
- Use pagination for large result sets
- Index frequently queried fields
- Clean up old memories

### 3. Security
- Encrypt sensitive data before storing
- Validate all inputs
- Implement proper access controls
- Audit memory access

## Common Use Cases

### 1. Code Context Persistence
```javascript
// Save editor state
async function saveEditorState(filePath, cursor, selections) {
  await memories.create({
    type: 'editor_state',
    key: `editor:${filePath}`,
    value: { cursor, selections },
    tags: ['editor', 'state']
  });
}

// Restore editor state
async function restoreEditorState(filePath) {
  const state = await memories.get(`editor:${filePath}`);
  return state?.value || { cursor: { line: 0, column: 0 }, selections: [] };
}
```

### 2. User Preferences
```javascript
// Save user preferences
async function saveUserPreferences(userId, prefs) {
  await memories.setPreference(`user:${userId}:prefs`, prefs);
}

// Get user preferences with defaults
async function getUserPreferences(userId) {
  return await memories.getPreference(
    `user:${userId}:prefs`,
    { theme: 'light', fontSize: 14 }
  );
}
```

### 3. Learning from Interactions
```javascript
// Save successful code completions
async function trackCompletion(prefix, suggestion, accepted) {
  await memories.create({
    type: 'completion',
    key: `completion:${hash(prefix)}`,
    value: { prefix, suggestion, accepted },
    tags: ['learning', 'completion']
  });
}

// Get relevant completions
async function getRelevantCompletions(prefix) {
  return await memories.search({
    query: prefix,
    types: ['completion'],
    filters: { 'value.accepted': true },
    limit: 5
  });
}
```

## Integration with Windsurf

### 1. Editor Integration
```javascript
// Save cursor position when file changes
document.addEventListener('cursorActivity', async (event) => {
  const { filePath, cursor } = event.detail;
  await memories.saveContext({
    file: filePath,
    cursor,
    context: 'User is editing this file'
  });
});
```

### 2. Command Palette
```javascript
// Remember frequently used commands
async function trackCommandUsage(commandId) {
  await memories.incr(`command:${commandId}:count`);
  await memories.zadd('command:popularity', 1, commandId);
}

// Get popular commands
async function getPopularCommands(limit = 5) {
  return await memories.zrevrange('command:popularity', 0, limit - 1);
}
```

## Performance Optimization

### 1. Caching
```javascript
// Memory cache layer
const memoryCache = new Map();

async function getWithCache(key) {
  if (memoryCache.has(key)) {
    return memoryCache.get(key);
  }
  const value = await memories.get(key);
  if (value) {
    memoryCache.set(key, value);
  }
  return value;
}
```

### 2. Batch Operations
```javascript
// Load multiple memories at once
async function getMultipleMemories(keys) {
  const pipeline = memories.pipeline();
  keys.forEach(key => pipeline.get(key));
  return await pipeline.exec();
}

// Batch save
async function saveMultipleMemories(items) {
  const pipeline = memories.pipeline();
  items.forEach(item => {
    pipeline.create(item);
  });
  return await pipeline.exec();
}
```

## Security Considerations

### 1. Data Validation
```javascript
function validateMemory(memory) {
  // Validate memory structure
  const schema = Joi.object({
    type: Joi.string().required(),
    key: Joi.string().required(),
    value: Joi.any().required(),
    tags: Joi.array().items(Joi.string())
  });
  
  return schema.validate(memory);
}
```

### 2. Access Control
```javascript
async function getUserMemories(userId, query) {
  // Ensure users can only access their own memories
  return await memories.search({
    ...query,
    filters: {
      ...query.filters,
      'value.userId': userId
    }
  });
}
```

## Troubleshooting

### Common Issues

1. **Memory not found**
   - Verify the key exists
   - Check for typos
   - Verify access permissions

2. **Performance issues**
   - Check for large memory items
   - Verify indexes exist
   - Monitor memory usage

3. **Inconsistent state**
   - Check for concurrent modifications
   - Verify transaction boundaries
   - Check for proper error handling

### Debugging
```javascript
// Enable debug logging
process.env.DEBUG = 'windsurf:memories*';

// Get memory statistics
const stats = await memories.stats();
console.log('Memory stats:', stats);
```

## Monitoring and Maintenance

### 1. Health Checks
```javascript
// Check if memories are working
async function checkHealth() {
  try {
    await memories.ping();
    return { status: 'healthy' };
  } catch (error) {
    return { status: 'unhealthy', error: error.message };
  }
}
```

### 2. Cleanup
```javascript
// Remove old memories
async function cleanupOldMemories(days = 30) {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  
  const oldMemories = await memories.search({
    filters: {
      createdAt: { $lt: cutoff }
    },
    types: ['temporary']
  });
  
  await memories.deleteMany(oldMemories.map(m => m.id));
  return oldMemories.length;
}
```

### 3. Backup and Restore
```javascript
// Export memories
async function exportMemories() {
  const allMemories = await memories.search({ limit: 10000 });
  return JSON.stringify(allMemories, null, 2);
}

// Import memories
async function importMemories(jsonData) {
  const items = JSON.parse(jsonData);
  return await saveMultipleMemories(items);
}
```

## Example: Complete Implementation

### User Settings Manager
```javascript
class UserSettings {
  constructor(userId) {
    this.userId = userId;
    this.namespace = `user:${userId}:settings`;
  }

  async get(key, defaultValue = null) {
    return await memories.get(`${this.namespace}:${key}`, defaultValue);
  }

  async set(key, value) {
    return await memories.set(`${this.namespace}:${key}`, value);
  }

  async getAll() {
    const keys = await memories.keys(`${this.namespace}:*`);
    const values = await Promise.all(keys.map(k => memories.get(k)));
    return keys.reduce((acc, key, i) => ({
      ...acc,
      [key.replace(`${this.namespace}:`, '')]: values[i]
    }), {});
  }

  async trackUsage(feature) {
    await memories.zincrby(`user:${this.userId}:features`, 1, feature);
  }

  async getFavoriteFeatures(limit = 5) {
    return await memories.zrevrange(
      `user:${this.userId}:features`,
      0,
      limit - 1
    );
  }
}
```

## Migration Guide

### From v1 to v2
1. Backup existing memories
2. Update configuration format
3. Run migration script
4. Verify data integrity

### Schema Changes
- Added `createdAt` and `updatedAt` timestamps
- Changed tag structure
- Added support for vector search

## API Reference

### Core Methods
- `memories.create(memory)`: Create a new memory
- `memories.get(key)`: Retrieve a memory by key
- `memories.update(key, updates)`: Update an existing memory
- `memories.delete(key)`: Delete a memory
- `memories.search(query)`: Search memories

### Utility Methods
- `memories.findSimilar(text, options)`: Find similar memories
- `memories.incr(key, amount)`: Increment a numeric value
- `memories.zadd(key, score, member)`: Add to a sorted set
- `memories.zrange(key, start, stop)`: Get range from a sorted set

## Contributing
1. Fork the repository
2. Create a feature branch
3. Write tests
4. Submit a pull request

## License
MIT
