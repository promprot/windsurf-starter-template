"""
Unit tests for the ExampleTool class.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from src.tools.example_tool import ExampleTool

# Test data
TEST_CONFIG = {"test_config": "value"}

@pytest.fixture
def example_tool():
    """Fixture to provide an initialized ExampleTool instance for testing."""
    return ExampleTool(config=TEST_CONFIG)

@pytest.mark.asyncio
async def test_example_tool_initialization(example_tool):
    """Test that the tool initializes with the correct configuration."""
    assert example_tool.name == "example_tool"
    assert example_tool.description == "An example tool that demonstrates tool functionality"
    assert example_tool.config == TEST_CONFIG

@pytest.mark.parametrize("operation,params,expected_result", [
    ("greet", {"name": "Test"}, "Hello, Test!"),
    ("greet", {}, "Hello, World!"),
    ("add", {"a": 2, "b": 3}, 5),
    ("add", {"a": -1, "b": 1}, 0),
])
@pytest.mark.asyncio
async def test_example_tool_operations(example_tool, operation, params, expected_result):
    """Test the various operations of the example tool."""
    input_data = {"operation": operation, **params}
    result = await example_tool.execute(input_data)
    
    assert result["status"] == "success"
    assert result["result"] == expected_result
    assert result["metadata"]["operation"] == operation
    assert result["metadata"]["input"] == input_data

@pytest.mark.asyncio
async def test_example_tool_unknown_operation(example_tool):
    """Test that an unknown operation returns an error."""
    result = await example_tool.execute({"operation": "unknown_operation"})
    
    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]
    assert result["input"]["operation"] == "unknown_operation"

@pytest.mark.asyncio
async def test_example_tool_execution_error(example_tool):
    """Test error handling during tool execution."""
    # Test with invalid input for add operation
    result = await example_tool.execute({"operation": "add", "a": "not_a_number"})
    assert result["status"] == "error"
    
    # Test with missing operation
    result = await example_tool.execute({})
    assert result["status"] == "success"  # Default operation is greet

@pytest.mark.asyncio
async def test_example_tool_cleanup(example_tool):
    """Test that the cleanup method can be called without errors."""
    try:
        await example_tool.cleanup()
    except Exception as e:
        pytest.fail(f"cleanup() raised {type(e).__name__} unexpectedly!")

@pytest.mark.asyncio
async def test_example_tool_integration():
    """Test the tool's integration with the agent (example)."""
    # This is a placeholder for more complex integration tests
    tool = ExampleTool()
    result = await tool.execute({"operation": "greet", "name": "Integration"})
    assert result["status"] == "success"
    assert result["result"] == "Hello, Integration!"

# Test for error logging
@pytest.mark.asyncio
async def test_example_tool_error_logging(caplog, example_tool):
    """Test that errors are properly logged."""
    with caplog.at_level("ERROR"):
        await example_tool.execute({"operation": "invalid_operation"})
        
    assert "Error in example tool" in caplog.text

# Test for concurrent execution
@pytest.mark.asyncio
async def test_example_tool_concurrent_execution(example_tool):
    """Test that the tool can handle concurrent executions."""
    async def run_operation(i):
        return await example_tool.execute({"operation": "add", "a": i, "b": 1})
    
    # Run multiple operations concurrently
    results = await asyncio.gather(
        *(run_operation(i) for i in range(10)),
        return_exceptions=True
    )
    
    # Verify all operations completed successfully
    for i, result in enumerate(results):
        assert result["status"] == "success"
        assert result["result"] == i + 1
