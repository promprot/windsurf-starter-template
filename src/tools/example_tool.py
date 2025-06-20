"""
Example Tool for Windsurf Agent

This module provides an example implementation of a tool that can be used by the agent.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ExampleTool:
    """An example tool that demonstrates tool functionality.
    
    This tool provides basic example operations that can be extended for
    more complex functionality.
    """
    
    name = "example_tool"
    description = "An example tool that demonstrates tool functionality"
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the example tool with configuration.
        
        Args:
            config: Configuration dictionary for the tool
        """
        self.config = config or {}
        self._setup()
    
    def _setup(self) -> None:
        """Set up the tool with any required resources."""
        logger.debug("Setting up example tool")
        # Initialize any required resources here
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with the given input.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing the execution result
            
        Example:
            >>> tool = ExampleTool()
            >>> asyncio.run(tool.execute({"operation": "greet", "name": "World"}))
            {'status': 'success', 'result': 'Hello, World!'}
        """
        try:
            logger.info(f"Executing example tool with input: {input_data}")
            
            # Extract operation and parameters
            operation = input_data.get("operation", "greet")
            
            # Route to the appropriate operation
            if operation == "greet":
                name = input_data.get("name", "World")
                result = f"Hello, {name}!"
            elif operation == "add":
                a = float(input_data.get("a", 0))
                b = float(input_data.get("b", 0))
                result = a + b
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            return {
                "status": "success",
                "result": result,
                "metadata": {
                    "operation": operation,
                    "input": input_data
                }
            }
            
        except Exception as e:
            logger.error(f"Error in example tool: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "input": input_data
            }
    
    async def cleanup(self) -> None:
        """Clean up any resources used by the tool."""
        logger.debug("Cleaning up example tool")
        # Clean up any resources here


# Example usage
if __name__ == "__main__":
    import asyncio
    import json
    
    async def main():
        tool = ExampleTool()
        
        # Test greet operation
        result = await tool.execute({"operation": "greet", "name": "Windsurf"})
        print("Greet result:", json.dumps(result, indent=2))
        
        # Test add operation
        result = await tool.execute({"operation": "add", "a": 5, "b": 3})
        print("\nAdd result:", json.dumps(result, indent=2))
        
        # Test error case
        result = await tool.execute({"operation": "unknown"})
        print("\nError result:", json.dumps(result, indent=2))
        
        await tool.cleanup()
    
    asyncio.run(main())
