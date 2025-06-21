# Windsurf Rules Guide

## Table of Contents
1. [Overview](#overview)
2. [Enabling Rules](#enabling-rules)
3. [Rule Types](#rule-types)
4. [Creating Custom Rules](#creating-custom-rules)
5. [Best Practices](#best-practices)
6. [Common Rule Examples](#common-rule-examples)
7. [Troubleshooting](#troubleshooting)

## Overview
Windsurf Rules allow you to enforce coding standards, security policies, and best practices across your codebase. Rules can be applied to both local development and CI/CD pipelines.

## Enabling Rules

### Configuration
Create or modify `.windsurf/rules.json`:

```json
{
  "rules": {
    "naming-convention": "error",
    "no-console": "warn",
    "security/detect-non-literal-fs-filename": "error"
  },
  "extends": [
    "windsurf:recommended"
  ]
}
```

### CLI Commands
```bash
# List all available rules
windsurf rules list

# Run rules on specific files
windsurf rules check "src/**/*.js"

# Auto-fix fixable rules
windsurf rules fix "src/**/*.js"
```

## Rule Types

### 1. Code Style Rules
- Enforce consistent code formatting
- Example: `indent`, `quotes`, `semi`

### 2. Best Practices
- Enforce coding best practices
- Example: `no-var`, `prefer-const`, `eqeqeq`

### 3. Security Rules
- Prevent security vulnerabilities
- Example: `security/detect-object-injection`

### 4. Performance Rules
- Optimize code performance
- Example: `no-delete-var`, `no-implied-eval`

## Creating Custom Rules

### 1. Create a Rule File
Create `rules/custom-rules.js`:

```javascript
// Custom rule to prevent using console.log in production
module.exports = {
  meta: {
    type: 'suggestion',
    docs: {
      description: 'Disallow the use of console.log in production',
      category: 'Best Practices',
      recommended: true
    },
    schema: []
  },
  create(context) {
    return {
      CallExpression(node) {
        if (node.callee.object?.name === 'console' && 
            node.callee.property?.name === 'log' &&
            process.env.NODE_ENV === 'production') {
          context.report({
            node,
            message: 'Unexpected console.log statement in production code.'
          });
        }
      }
    };
  }
};
```

### 2. Configure Custom Rules
In `.windsurf/rules.json`:

```json
{
  "rules": {
    "custom-rules/no-console-in-prod": "error"
  },
  "rulesDirectory": "./rules"
}
```

## Best Practices

### 1. Start with Recommended Rules
```json
{
  "extends": ["windsurf:recommended"]
}
```

### 2. Be Specific with Rule Configuration
```json
{
  "rules": {
    "complexity": ["error", 10],
    "max-lines": ["warn", 300]
  }
}
```

### 3. Use Rule Overrides
```json
{
  "overrides": [
    {
      "files": ["*.test.js"],
      "rules": {
        "no-console": "off"
      }
    }
  ]
}
```

## Common Rule Examples

### 1. Enforce Naming Conventions
```json
{
  "rules": {
    "naming-convention": ["error", 
      {
        "selector": "variable",
        "format": ["camelCase", "UPPER_CASE"],
        "leadingUnderscore": "allow"
      }
    ]
  }
}
```

### 2. Security Rules
```json
{
  "rules": {
    "security/detect-child-process": "error",
    "security/detect-non-literal-require": "error",
    "security/detect-possible-timing-attacks": "error"
  }
}
```

### 3. Performance Rules
```json
{
  "rules": {
    "no-delete-var": "error",
    "no-implied-eval": "error",
    "no-script-url": "error"
  }
}
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Lint Code

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - name: Run Windsurf Rules
        run: npx windsurf rules check "src/**/*.js"
```

## Troubleshooting

### Common Issues

1. **Rules not being applied**
   - Check rule names are correct
   - Verify configuration file is in the correct location
   - Check for configuration overrides

2. **Performance issues**
   - Exclude `node_modules`
   - Use `.windsurfignore`
   - Run rules incrementally

3. **False positives**
   - Use inline comments to disable rules
   - Report issues to rule maintainers
   - Create more specific rule configurations

### Debugging
```bash
# Show debug information
DEBUG=windsurf:rules windsurf rules check

# Show rule execution time
TIMING=1 windsurf rules check
```

## Advanced Configuration

### Rule Inheritance
```json
{
  "extends": [
    "windsurf:recommended",
    "plugin:security/recommended"
  ]
}
```

### File-Specific Rules
```json
{
  "overrides": [
    {
      "files": ["*.ts"],
      "rules": {
        "@typescript-eslint/explicit-function-return-type": "error"
      }
    }
  ]
}
```

### Sharing Configurations
Create `windsurf-config.js`:
```javascript
module.exports = {
  rules: {
    // Your rules here
  }
};
```

Then extend it in other projects:
```json
{
  "extends": "./windsurf-config.js"
}
```

## Rule Development

### Testing Rules
1. Create test files with both valid and invalid code
2. Use the `RuleTester` utility
3. Test edge cases and error conditions

### Publishing Rules
1. Create an npm package
2. Follow the naming convention `eslint-plugin-<plugin-name>`
3. Document your rules
4. Publish to npm

## Example: Complete Configuration

```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "windsurf:recommended",
    "plugin:security/recommended"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "semi": ["error", "always"],
    "quotes": ["error", "single"],
    "indent": ["error", 2],
    "no-console": "warn",
    "complexity": ["warn", 10],
    "max-lines": ["warn", 500],
    "security/detect-object-injection": "off"
  },
  "overrides": [
    {
      "files": ["*.test.js", "*.spec.js"],
      "rules": {
        "no-console": "off"
      }
    }
  ],
  "ignorePatterns": ["node_modules/", "dist/", "coverage/"]
}
```
