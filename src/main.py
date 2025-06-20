#!/usr/bin/env python3
"""
Windsurf Agent - Main Entry Point

This module serves as the main entry point for the Windsurf agent.
It initializes the agent, loads tools, and starts the processing loop.
"""

import asyncio
import json
import logging
import logging.handlers
import os
import signal
import sys
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional, Type, TypeVar, Union, cast

import aiohttp
from aiohttp import web

from .config import AgentConfig, load_config

# Configure initial logging (will be reconfigured after config is loaded)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

T = TypeVar('T')


class Agent:
    """Main agent class that coordinates tools and processing."""

    def __init__(self, config: Optional[Union[Dict[str, Any], AgentConfig]] = None):
        """Initialize the agent with configuration.
        
        Args:
            config: Configuration dictionary or AgentConfig instance
        """
        self._config: Optional[AgentConfig] = None
        self.tools: Dict[str, Any] = {}
        self.memory = None
        self._setup_complete = False
        self._http_session: Optional[aiohttp.ClientSession] = None
        self._web_app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        
        # Initialize with provided config or load default
        if config is not None:
            if isinstance(config, dict):
                self._config = AgentConfig(**config)
            elif isinstance(config, AgentConfig):
                self._config = config
        
        # Configure logging based on config
        self._configure_logging()
    
    async def __aenter__(self) -> 'Agent':
        """Async context manager entry."""
        await self.setup()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.cleanup()
    
    @property
    def config(self) -> AgentConfig:
        """Get the agent configuration.
        
        Returns:
            AgentConfig: The agent configuration.
            
        Raises:
            RuntimeError: If the agent is not configured.
        """
        if self._config is None:
            raise RuntimeError("Agent not configured. Call load_config() first.")
        return self._config
    
    @classmethod
    def from_config_file(cls, config_path: Union[str, Path, None] = None) -> 'Agent':
        """Create an agent instance from a configuration file.
        
        Args:
            config_path: Path to the configuration file. If None, uses default.
            
        Returns:
            Agent: Configured agent instance.
        """
        if config_path is None:
            config_path = Path(".windsurf/agent_settings.json")
            
        config = load_config(config_path)
        return cls(config)
    
    def _configure_logging(self) -> None:
        """Configure logging based on the agent configuration."""
        if self._config is None:
            return
            
        log_config = self.config.logging
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_config.level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_config.format))
        root_logger.addHandler(console_handler)
        
        # Configure file handler if file logging is enabled
        if log_config.file:
            log_file = Path(log_config.file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=log_config.max_size_mb * 1024 * 1024,  # Convert MB to bytes
                backupCount=log_config.backup_count,
                encoding='utf-8',
            )
            file_handler.setFormatter(logging.Formatter(log_config.format))
            root_logger.addHandler(file_handler)
            
        logger.info(f"Logging configured with level {log_config.level}")
    
    async def get_http_session(self) -> aiohttp.ClientSession:
        """Get or create an HTTP client session.
        
        Returns:
            aiohttp.ClientSession: The HTTP client session.
        """
        if self._http_session is None or self._http_session.closed:
            self._http_session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                json_serialize=lambda x: json.dumps(x, ensure_ascii=False)
            )
        return self._http_session

    async def setup(self) -> None:
        """Set up the agent components."""
        if self._setup_complete:
            return

        logger.info("Setting up agent...")
        
        # Initialize components
        await self._setup_memory()
        await self._load_tools()
        await self._setup_http_server()
        
        self._setup_complete = True
        logger.info("Agent setup complete")
    
    async def _setup_http_server(self) -> None:
        """Set up the HTTP server if monitoring is enabled."""
        if not self.config.monitoring.enabled:
            return
            
        self._web_app = web.Application()
        self._configure_routes()
        
        # Create an app runner
        self._runner = web.AppRunner(self._web_app)
        await self._runner.setup()
        
        # Start the server
        self._site = web.TCPSite(
            self._runner,
            host='0.0.0.0',
            port=self.config.monitoring.port
        )
        
        try:
            await self._site.start()
            logger.info(f"HTTP server started on port {self.config.monitoring.port}")
        except Exception as e:
            logger.error(f"Failed to start HTTP server: {e}")
    
    def _configure_routes(self) -> None:
        """Configure HTTP routes for the web application."""
        if self._web_app is None:
            return
            
        # Health check endpoints
        if self.config.monitoring.health_check.enabled:
            self._web_app.router.add_get(
                self.config.monitoring.health_check.endpoint,
                self.health_check_handler
            )
            self._web_app.router.add_get(
                self.config.monitoring.health_check.live_endpoint,
                self.liveness_handler
            )
            self._web_app.router.add_get(
                self.config.monitoring.health_check.ready_endpoint,
                self.readiness_handler
            )
        
        # Metrics endpoint
        if self.config.monitoring.enabled and hasattr(self, 'metrics_handler'):
            self._web_app.router.add_get(
                self.config.monitoring.endpoint,
                self.metrics_handler
            )
    
    async def health_check_handler(self, request: web.Request) -> web.Response:
        """Handle health check requests."""
        return web.json_response({
            'status': 'ok',
            'version': self.config.version,
            'name': self.config.name
        })
    
    async def liveness_handler(self, request: web.Request) -> web.Response:
        """Handle liveness probe requests."""
        return web.json_response({'status': 'alive'})
    
    async def readiness_handler(self, request: web.Request) -> web.Response:
        """Handle readiness probe requests."""
        if self._setup_complete and all(tool.is_ready() for tool in self.tools.values()):
            return web.json_response({'status': 'ready'})
        return web.json_response(
            {'status': 'not ready'},
            status=503  # Service Unavailable
        )

    async def _setup_memory(self) -> None:
        """Initialize memory component."""
        if not self.config.memory.enabled:
            logger.debug("Memory is disabled in configuration")
            return
            
        logger.debug("Initializing memory...")
        # Placeholder for memory setup
        self.memory = {}
        logger.info("Memory initialized")

    async def _load_tools(self) -> None:
        """Load available tools."""
        if not self.config.tools.auto_discover:
            logger.debug("Auto-discovery of tools is disabled")
            return
            
        logger.debug("Loading tools...")
        
        # Ensure tools directory exists
        tools_dir = Path(self.config.tools.directory)
        if not tools_dir.exists():
            logger.warning(f"Tools directory not found: {tools_dir}")
            return
        
        # Add tools directory to Python path
        if str(tools_dir.parent) not in sys.path:
            sys.path.insert(0, str(tools_dir.parent))
        
        # Example tool loading - in a real implementation, you would dynamically import tools
        try:
            from tools.example_tool import ExampleTool
            self.tools["example"] = ExampleTool()
            logger.info(f"Loaded tool: example")
        except ImportError as e:
            logger.warning(f"Failed to load example tool: {e}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return response.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            Dictionary containing the processing result
            
        Raises:
            ValueError: If the input data is invalid
        """
        if not self._setup_complete:
            await self.setup()

        logger.info(f"Processing input: {input_data}")
        
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        
        # Example processing logic
        response: Dict[str, Any] = {
            'status': 'success',
            'input': input_data,
            'result': None,
            'metadata': {
                'agent': self.config.name,
                'version': self.config.version,
                'timestamp': asyncio.get_event_loop().time()
            }
        }
        
        # Here you would add your actual processing logic
        # For example, routing to specific tools based on input
        
        return response
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up agent resources...")
        
        # Close HTTP session
        if self._http_session and not self._http_session.closed:
            await self._http_session.close()
        
        # Stop web server
        if self._site is not None:
            await self._site.stop()
        if self._runner is not None:
            await self._runner.cleanup()
        if self._web_app is not None:
            await self._web_app.cleanup()
        
        # Clean up tools
        for name, tool in list(self.tools.items()):
            if hasattr(tool, 'cleanup') and callable(tool.cleanup):
                await tool.cleanup()
            del self.tools[name]
        
        logger.info("Agent cleanup complete")
    
    async def run(self) -> None:
        """Run the agent in interactive mode."""
        await self.setup()
        
        print(f"{self.config.name} v{self.config.version}")
        print("Type 'exit' or press Ctrl+C to quit")
        
        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown(sig)))
        
        try:
            while True:
                try:
                    user_input = await loop.run_in_executor(
                        None, input, "\nEnter input (or 'exit' to quit): "
                    )
                    
                    if user_input.lower() in ('exit', 'quit'):
                        break
                        
                    # Process the input
                    response = await self.process({"input": user_input})
                    print("\nResponse:", json.dumps(response, indent=2))
                    
                except (EOFError, KeyboardInterrupt):
                    break
                except Exception as e:
                    logger.error(f"Error processing input: {e}", exc_info=True)
                    print(f"Error: {e}")
                    
        finally:
            await self.cleanup()
    
    async def shutdown(self, sig: signal.Signals) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {sig.name}, shutting down...")
        await self.cleanup()
        asyncio.get_running_loop().stop()


def main() -> None:
    """Main entry point for the agent."""
    try:
        agent = Agent.from_config_file()
        asyncio.run(agent.run())
    except Exception as e:
        logger.critical(f"Agent crashed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

        while True:
            try:
                user_input = input("\n> ")
                if user_input.lower() in ('exit', 'quit'):
                    break
                    
                # Process the input
                response = await self.process({"text": user_input})
                print("\nResponse:", response)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error processing input: {e}", exc_info=True)


async def main():
    """Main entry point for the agent."""
    agent = Agent()
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
