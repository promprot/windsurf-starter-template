"""Pytest configuration and fixtures for integration tests."""

import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from aiohttp import web, test_utils
from aiohttp.test_utils import TestClient, TestServer

# Configure logging for tests
if os.getenv("DEBUG_TESTS"):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("asyncio").setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    # Use a more precise event loop policy for Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    yield loop
    
    # Cleanup
    if not loop.is_closed():
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


@pytest.fixture
def unused_port() -> int:
    """Return an unused port number."""
    return test_utils.unused_port()


@pytest_asyncio.fixture
async def aiohttp_client(loop, aiohttp_client, unused_port):
    """Create a test client for aiohttp applications."""
    # This fixture is provided by pytest-aiohttp, but we customize it here
    # to ensure it uses our event loop and port settings
    async def create_client(app, *args, **kwargs):
        # Ensure the app is configured with our test settings
        if 'port' not in kwargs:
            kwargs['port'] = unused_port()
        
        # Create and return the test client
        client = await aiohttp_client(app, *args, **kwargs)
        return client
    
    return create_client


@pytest.fixture
def test_config() -> dict:
    """Return a test configuration dictionary."""
    return {
        "name": "test_agent",
        "version": "1.0.0",
        "http": {
            "host": "127.0.0.1",
            "port": 0,  # Let the OS assign a port
            "cors_enabled": True
        },
        "monitoring": {
            "enabled": True,
            "metrics_endpoint": "/metrics",
            "health_check_endpoint": "/health"
        },
        "logging": {
            "level": "INFO",
            "file_path": None
        },
        "tools": [
            {
                "name": "example_tool",
                "enabled": True,
                "config": {
                    "default_name": "Test User"
                }
            }
        ]
    }
