"""
Example usage of the Agent Framework
"""

import logging
from src.agentcore.factory import AgentFactory
from src.agentcore.config import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_agent():
    """Example: Create and use a basic agent"""
    print("\n=== Basic Agent Example ===")
    
    # Create factory
    factory = AgentFactory()
    
    # Create an agent
    agent = factory.create_agent(
        agent_id="agent_001",
        name="BasicAgent",
        description="A basic example agent"
    )
    
    # Start the agent
    agent.start()
    print(f"Agent status: {agent.get_status()}")
    
    # Add task
    task_id = agent.add_task({
        'name': 'Example Task',
        'action': lambda: "Task executed successfully",
        'parameters': {}
    })
    print(f"Task added with ID: {task_id}")
    
    # Stop the agent
    agent.stop()
    factory.shutdown()


def example_agent_with_tools():
    """Example: Agent using built-in tools"""
    print("\n=== Agent with Tools Example ===")
    
    factory = AgentFactory()
    
    agent = factory.create_agent(
        agent_id="agent_002",
        name="ToolAgent",
        description="Agent that uses built-in tools"
    )
    
    agent.start()
    
    # Execute built-in tools
    try:
        # Use logging tool
        result = agent.execute_tool(
            'log_message',
            message="Agent is working with tools",
            level="info"
        )
        print(f"Log result: {result}")
        
        # Use environment tool
        result = agent.execute_tool(
            'get_environment',
            key='PATH'
        )
        print(f"Environment result: {result['value'][:50]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    agent.stop()
    factory.shutdown()


def example_multiple_agents():
    """Example: Create and manage multiple agents"""
    print("\n=== Multiple Agents Example ===")
    
    factory = AgentFactory()
    
    # Create multiple agents
    agents_config = [
        {"id": "worker_1", "name": "WorkerAgent1"},
        {"id": "worker_2", "name": "WorkerAgent2"},
        {"id": "coordinator", "name": "CoordinatorAgent"}
    ]
    
    agents = []
    for config in agents_config:
        agent = factory.create_agent(
            agent_id=config["id"],
            name=config["name"]
        )
        agents.append(agent)
        agent.start()
    
    # Get all agents status
    print("\nAll agents status:")
    for status in factory.get_all_agents_status():
        print(f"  - {status['name']}: {status['state']}")
    
    # Stop all agents
    for agent in agents:
        agent.stop()
    
    factory.shutdown()


def example_agent_memory():
    """Example: Using agent memory"""
    print("\n=== Agent Memory Example ===")
    
    factory = AgentFactory()
    
    agent = factory.create_agent(
        agent_id="agent_003",
        name="MemoryAgent",
        description="Agent with memory management"
    )
    
    agent.start()
    
    # Store data in memory
    agent.set_memory("user_name", "John Doe")
    agent.set_memory("conversation_count", 42)
    agent.set_memory("preferences", {"theme": "dark", "language": "en"})
    
    # Retrieve from memory
    print(f"User: {agent.get_memory('user_name')}")
    print(f"Conversations: {agent.get_memory('conversation_count')}")
    print(f"Preferences: {agent.get_memory('preferences')}")
    
    # Clear specific memory
    agent.clear_memory("conversation_count")
    print(f"After clear: {agent.get_memory('conversation_count', 'Not found')}")
    
    agent.stop()
    factory.shutdown()


def example_agent_configuration():
    """Example: Agent configuration management"""
    print("\n=== Agent Configuration Example ===")
    
    config_manager = ConfigManager()
    
    # Create configuration
    config = config_manager.create_config(
        agent_id="agent_004",
        name="ConfigAgent",
        description="Agent with custom configuration",
        max_workers=10,
        timeout=600,
        max_tasks=500
    )
    
    print(f"Created config: {config}")
    
    # Save configuration
    config_manager.save_config("agent_004", config)
    print("Configuration saved")
    
    # Load configuration
    loaded_config = config_manager.load_config("agent_004")
    print(f"Loaded config: {loaded_config}")
    
    # Update configuration
    updated_config = config_manager.update_config(
        "agent_004",
        timeout=900,
        max_workers=15
    )
    print(f"Updated config timeout: {updated_config.timeout}")


if __name__ == "__main__":
    print("Agent Framework Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_agent()
    example_agent_with_tools()
    example_multiple_agents()
    example_agent_memory()
    example_agent_configuration()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
