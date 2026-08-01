"""
Agent Tools - Predefined tools for agent operations
"""

import logging
import json
import os
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for managing agent tools"""
    
    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register(self, 
                 name: str, 
                 func: Callable,
                 description: str = "",
                 parameters: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a tool
        
        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            parameters: Tool parameters schema
        """
        self.tools[name] = {
            'function': func,
            'description': description,
            'parameters': parameters or {},
            'registered_at': datetime.now().isoformat()
        }
        logger.info(f"Tool '{name}' registered")
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get a registered tool
        
        Args:
            name: Tool name
            
        Returns:
            Tool function or None
        """
        tool = self.tools.get(name)
        return tool['function'] if tool else None
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all registered tools
        
        Returns:
            List of tool information
        """
        return [
            {
                'name': name,
                'description': info['description'],
                'parameters': info['parameters']
            }
            for name, info in self.tools.items()
        ]


class BuiltinTools:
    """Collection of built-in tools for agents"""
    
    @staticmethod
    def http_request(url: str, 
                    method: str = "GET",
                    headers: Optional[Dict[str, str]] = None,
                    data: Optional[Dict[str, Any]] = None,
                    timeout: int = 30) -> Dict[str, Any]:
        """
        Make HTTP request
        
        Args:
            url: Request URL
            method: HTTP method (GET, POST, etc.)
            headers: Request headers
            data: Request data
            timeout: Request timeout
            
        Returns:
            Response dictionary with status, headers, and body
        """
        try:
            logger.info(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'body': response.text,
                'success': response.status_code < 400
            }
        except Exception as e:
            logger.error(f"HTTP request failed: {str(e)}")
            return {
                'status': 0,
                'error': str(e),
                'success': False
            }
    
    @staticmethod
    def file_read(file_path: str) -> Dict[str, Any]:
        """
        Read file contents
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents or error
        """
        try:
            logger.info(f"Reading file: {file_path}")
            
            if not os.path.exists(file_path):
                return {'success': False, 'error': 'File not found'}
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'size': len(content)
            }
        except Exception as e:
            logger.error(f"File read failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def file_write(file_path: str, content: str) -> Dict[str, Any]:
        """
        Write to file
        
        Args:
            file_path: Path to file
            content: Content to write
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Writing to file: {file_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f'Written {len(content)} bytes',
                'file_path': file_path
            }
        except Exception as e:
            logger.error(f"File write failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def json_parse(data: str) -> Dict[str, Any]:
        """
        Parse JSON string
        
        Args:
            data: JSON string
            
        Returns:
            Parsed JSON or error
        """
        try:
            logger.info("Parsing JSON data")
            result = json.loads(data)
            return {
                'success': True,
                'data': result,
                'type': type(result).__name__
            }
        except Exception as e:
            logger.error(f"JSON parse failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def json_stringify(data: Any, indent: Optional[int] = 2) -> Dict[str, Any]:
        """
        Convert data to JSON string
        
        Args:
            data: Data to convert
            indent: JSON indentation
            
        Returns:
            JSON string or error
        """
        try:
            logger.info("Converting data to JSON string")
            result = json.dumps(data, indent=indent)
            return {
                'success': True,
                'json': result,
                'size': len(result)
            }
        except Exception as e:
            logger.error(f"JSON stringify failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_environment(key: str, default: Optional[str] = None) -> Dict[str, Any]:
        """
        Get environment variable
        
        Args:
            key: Environment variable key
            default: Default value
            
        Returns:
            Environment variable value or default
        """
        value = os.getenv(key, default)
        logger.info(f"Retrieved environment variable: {key}")
        return {
            'success': True,
            'key': key,
            'value': value
        }
    
    @staticmethod
    def execute_shell(command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute shell command
        
        Args:
            command: Command to execute
            timeout: Command timeout
            
        Returns:
            Command output or error
        """
        import subprocess
        
        try:
            logger.info(f"Executing shell command: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return {
                'success': False,
                'error': f'Command timeout after {timeout} seconds'
            }
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def log_message(message: str, level: str = "info") -> Dict[str, Any]:
        """
        Log a message
        
        Args:
            message: Message to log
            level: Log level (info, debug, warning, error)
            
        Returns:
            Logging status
        """
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(message)
        
        return {
            'success': True,
            'message': message,
            'level': level
        }


def create_default_tool_registry() -> ToolRegistry:
    """
    Create a tool registry with default tools
    
    Returns:
        ToolRegistry with built-in tools registered
    """
    registry = ToolRegistry()
    
    # Register built-in tools
    registry.register(
        'http_request',
        BuiltinTools.http_request,
        'Make HTTP requests',
        {'url': 'string', 'method': 'string', 'data': 'object'}
    )
    
    registry.register(
        'file_read',
        BuiltinTools.file_read,
        'Read file contents',
        {'file_path': 'string'}
    )
    
    registry.register(
        'file_write',
        BuiltinTools.file_write,
        'Write to file',
        {'file_path': 'string', 'content': 'string'}
    )
    
    registry.register(
        'json_parse',
        BuiltinTools.json_parse,
        'Parse JSON string',
        {'data': 'string'}
    )
    
    registry.register(
        'json_stringify',
        BuiltinTools.json_stringify,
        'Convert data to JSON',
        {'data': 'object'}
    )
    
    registry.register(
        'get_environment',
        BuiltinTools.get_environment,
        'Get environment variable',
        {'key': 'string'}
    )
    
    registry.register(
        'execute_shell',
        BuiltinTools.execute_shell,
        'Execute shell command',
        {'command': 'string', 'timeout': 'integer'}
    )
    
    registry.register(
        'log_message',
        BuiltinTools.log_message,
        'Log a message',
        {'message': 'string', 'level': 'string'}
    )
    
    return registry
