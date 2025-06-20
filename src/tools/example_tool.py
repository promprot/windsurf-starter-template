"""
Example Tool for Windsurf Agent

This module provides an example implementation of a tool that can be used by the agent.
It demonstrates best practices for tool implementation including type hints, documentation,
error handling, and resource management.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union, cast

# Configure logging
logger = logging.getLogger(__name__)

# Type aliases
OperationType = Literal["greet", "add"]


class ToolError(Exception):
    """Base exception for tool-related errors."""
    pass


class OperationNotSupportedError(ToolError):
    """Raised when an unsupported operation is requested."""
    pass


class InputValidationError(ToolError):
    """Raised when input validation fails."""
    pass


@dataclass
class ToolConfig:
    """Configuration for the ExampleTool.
    
    Attributes:
        default_name: Default name to use for greeting if none provided
        max_add_value: Maximum allowed value for addition operation
    """
    default_name: str = "World"
    max_add_value: float = 1000.0


class ExecuteInput(TypedDict, total=False):
    """Type definition for execute method input."""
    operation: OperationType
    name: str
    a: Union[int, float, str]
    b: Union[int, float, str]


class ExecuteResult(TypedDict):
    """Type definition for execute method result."""
    status: Literal["success", "error"]
    result: Optional[Any]
    error: Optional[str]
    metadata: Dict[str, Any]


class ExampleTool:
    """An example tool that demonstrates tool functionality.
    
    This tool provides basic example operations that can be extended for
    more complex functionality. It demonstrates proper type hints, error
    handling, and documentation.
    
    Attributes:
        name: The name of the tool
        description: A brief description of the tool
        version: The version of the tool
    """
    
    name: str = "example_tool"
    description: str = "An example tool that demonstrates tool functionality"
    version: str = "1.0.0"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the example tool with configuration.
        
        Args:
            config: Optional configuration dictionary for the tool. Can include:
                - default_name: Default name for greeting operation
                - max_add_value: Maximum allowed value for addition
                
        Example:
            >>> tool = ExampleTool({"default_name": "User", "max_add_value": 500})
        """
        self.config = ToolConfig(**config) if config else ToolConfig()
        self._setup()
    
    def _setup(self) -> None:
        """Set up the tool with any required resources.
        
        This method is called during initialization to prepare the tool
        for use. Override in subclasses to add custom setup logic.
        """
        logger.debug("Setting up example tool")
        # Initialize any required resources here
    
    async def execute(self, input_data: ExecuteInput) -> ExecuteResult:
        """Execute the tool with the given input.
        
        This is the main entry point for the tool. It routes the input to the
        appropriate operation handler based on the 'operation' field.
        
        Args:
            input_data: Dictionary containing input parameters. Must include:
                - operation: The operation to perform ('greet' or 'add')
                Additional fields depend on the operation:
                  - greet: 'name' (optional)
                  - add: 'a' and 'b' (numbers to add)
                
        Returns:
            A dictionary containing:
                - status: 'success' or 'error'
                - result: The operation result (on success)
                - error: Error message (on error)
                - metadata: Additional information about the operation
                
        Raises:
            InputValidationError: If input validation fails
            OperationNotSupportedError: If an unsupported operation is requested
            
        Example:
            >>> tool = ExampleTool()
            >>> await tool.execute({"operation": "greet", "name": "World"})
            {
                'status': 'success',
                'result': 'Hello, World!',
                'error': None,
                'metadata': {'operation': 'greet', 'input': {...}}
            }
        """
        logger.info("Executing example tool", extra={"input": input_data})
        
        try:
            # Validate input
            if not isinstance(input_data, dict) or 'operation' not in input_data:
                raise InputValidationError("Input must be a dictionary with an 'operation' key")
            
            operation = input_data.get('operation', 'greet')
            
            # Route to the appropriate operation
            if operation == 'greet':
                result = await self._handle_greet(input_data)
            elif operation == 'add':
                result = await self._handle_add(input_data)
            else:
                raise OperationNotSupportedError(f"Unsupported operation: {operation}")
            
            return {
                'status': 'success',
                'result': result,
                'error': None,
                'metadata': {
                    'operation': operation,
                    'input': input_data
                }
            }
            
        except ToolError as e:
            logger.error(f"Tool error: {e}", exc_info=True)
            return self._create_error_result(str(e), input_data)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.exception(error_msg)
            return self._create_error_result(error_msg, input_data)
    
    async def _handle_greet(self, input_data: Dict[str, Any]) -> str:
        """Handle the 'greet' operation.
        
        Args:
            input_data: Input parameters including optional 'name'
            
        Returns:
            A greeting message
        """
        name = str(input_data.get('name', self.config.default_name))
        return f"Hello, {name}!"
    
    async def _handle_add(self, input_data: Dict[str, Any]) -> float:
        """Handle the 'add' operation.
        
        Args:
            input_data: Input parameters including 'a' and 'b' to add
            
        Returns:
            The sum of a and b
            
        Raises:
            InputValidationError: If a or b are not valid numbers or exceed max_add_value
        """
        try:
            a = float(input_data.get('a', 0))
            b = float(input_data.get('b', 0))
            
            # Validate input values
            max_val = self.config.max_add_value
            if abs(a) > max_val or abs(b) > max_val:
                raise InputValidationError(
                    f"Values must not exceed {max_val} in magnitude"
                )
                
            return a + b
            
        except (TypeError, ValueError) as e:
            raise InputValidationError("Both 'a' and 'b' must be numbers") from e
    
    def _create_error_result(
        self,
        error_msg: str,
        input_data: Dict[str, Any]
    ) -> ExecuteResult:
        """Create a standardized error response.
        
        Args:
            error_msg: The error message
            input_data: The input that caused the error
            
        Returns:
            A dictionary with error details
        """
        return {
            'status': 'error',
            'result': None,
            'error': error_msg,
            'metadata': {'input': input_data}
        }
    
    async def cleanup(self) -> None:
        """Clean up any resources used by the tool.
        
        This method should be called when the tool is no longer needed
        to properly release any acquired resources.
        """
        logger.debug("Cleaning up example tool")
        # Clean up any resources here
    
    def is_ready(self) -> bool:
        """Check if the tool is ready to process requests.
        
        Returns:
            bool: True if the tool is ready, False otherwise
        """
        # Add any readiness checks here
        return True


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
