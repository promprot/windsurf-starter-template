"""Integration tests for the Windsurf Agent.

These tests verify the end-to-end functionality of the agent, including
configuration loading, tool execution, and health check endpoints.
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch

import pytest
from aiohttp import web, ClientSession, ClientResponse

from src.main import Agent, main
from src.config import AgentConfig

# Test configuration
TEST_CONFIG = {
    "name": "test_agent",
    "version": "1.0.0",
    "description": "Test agent configuration",
    "memory": {
        "enabled": True,
        "max_history": 100
    },
    "logging": {
        "level": "DEBUG",
        "file_path": None,
        "max_size_mb": 10,
        "backup_count": 5
    },
    "security": {
        "require_auth": False,
        "allowed_origins": ["*"],
        "rate_limit": {
            "enabled": False,
            "requests_per_minute": 60
        }
    },
    "monitoring": {
        "enabled": True,
        "metrics_endpoint": "/metrics",
        "health_check_endpoint": "/health"
    },
    "http": {
        "host": "127.0.0.1",
        "port": 8080,
        "cors_enabled": True
    },
    "tools": [
        {
            "name": "example_tool",
            "enabled": True,
            "config": {
                "default_name": "Test User",
                "max_add_value": 1000
            }
        }
    ]
}


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        json.dump(TEST_CONFIG, f)
        f.flush()
        yield f.name
        
    # Cleanup
    try:
        os.unlink(f.name)
    except OSError:
        pass


@pytest.fixture
def agent_config(temp_config_file: str) -> AgentConfig:
    """Create an agent configuration from the test config file."""
    return AgentConfig.from_json_file(temp_config_file)


@pytest.fixture
async def test_agent(agent_config: AgentConfig):
    """Create a test agent instance."""
    agent = Agent(config=agent_config)
    await agent.start()
    yield agent
    await agent.stop()


@pytest.fixture
def test_client(loop, aiohttp_client, test_agent: Agent):
    """Create a test client for the agent's HTTP server."""
    # The agent's app is already running, so we'll just use its server
    return loop.run_until_complete(aiohttp_client(test_agent.app))


class TestAgentIntegration:
    """Integration tests for the Agent class."""
    
    async def test_agent_initialization(self, agent_config: AgentConfig):
        """Test that the agent initializes with the correct configuration."""
        agent = Agent(config=agent_config)
        assert agent.config == agent_config
        assert agent.name == agent_config.name
        assert agent.version == agent_config.version
        
    async def test_agent_start_stop(self, agent_config: AgentConfig):
        """Test starting and stopping the agent."""
        agent = Agent(config=agent_config)
        
        # Start the agent
        await agent.start()
        assert agent.is_running
        
        # Stop the agent
        await agent.stop()
        assert not agent.is_running
        
    async def test_health_check_endpoint(self, test_client):
        """Test the health check endpoint."""
        # Test live health check
        resp = await test_client.get("/health/live")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "ok"
        
        # Test ready health check
        resp = await test_client.get("/health/ready")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "ok"
        
        # Test combined health check
        resp = await test_client.get("/health")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "ok"
        assert "live" in data
        assert "ready" in data
    
    async def test_tool_execution(self, test_agent: Agent):
        """Test executing a tool through the agent."""
        # Test greet operation
        result = await test_agent.process({
            "tool": "example_tool",
            "operation": "greet",
            "name": "Tester"
        })
        assert result["status"] == "success"
        assert result["result"] == "Hello, Tester!"
        
        # Test add operation
        result = await test_agent.process({
            "tool": "example_tool",
            "operation": "add",
            "a": 5,
            "b": 3
        })
        assert result["status"] == "success"
        assert result["result"] == 8.0
    
    async def test_invalid_tool_operation(self, test_agent: Agent):
        """Test handling of invalid tool operations."""
        # Invalid tool
        result = await test_agent.process({
            "tool": "nonexistent_tool",
            "operation": "greet"
        })
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()
        
        # Invalid operation
        result = await test_agent.process({
            "tool": "example_tool",
            "operation": "invalid_operation"
        })
        assert result["status"] == "error"
        assert "unsupported operation" in result["error"].lower()


class TestMainFunction:
    """Tests for the main() function."""
    
    async def test_main_function(self, temp_config_file: str, aiohttp_client):
        """Test the main() function with a test config file."""
        # Patch sys.argv to include our test config file
        with patch("sys.argv", ["main.py", "--config", temp_config_file]):
            # Start the agent in a background task
            agent_task = asyncio.create_task(main())
            
            # Give the agent time to start
            await asyncio.sleep(0.1)
            
            try:
                # Create a client to test the agent
                client = await aiohttp_client("http://127.0.0.1:8080")
                
                # Test the health check endpoint
                resp = await client.get("/health")
                assert resp.status == 200
                data = await resp.json()
                assert data["status"] == "ok"
                
            finally:
                # Stop the agent
                await Agent.get_instance().stop()
                agent_task.cancel()
                try:
                    await agent_task
                except asyncio.CancelledError:
                    pass
