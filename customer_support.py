import os
from dotenv import load_dotenv
import yaml
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

with open("agents.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_config_list(llm_config):
    provider = llm_config['provider']
    model = llm_config['model']
    api_key_env_var = llm_config['api_key_env_var']
    
    assert api_key_env_var in os.environ, f"{api_key_env_var} environment variable is missing from .env"
    api_key = os.environ[api_key_env_var]

    return [{'model': model, 'api_key': api_key}]

def resolve_variable(value, config):
    if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
        key = value[2:-1]
        return config.get(key, value)
    return value

def create_agent(agent_config, global_config):
    if agent_config['type'] == 'assistant':
        llm_config = agent_config.get('llm_config', {})
        provider = resolve_variable(llm_config.get('provider'), global_config)
        if provider.startswith('${'):
            provider = global_config['default_provider']
        config_list = get_config_list(global_config['llm_configs'][provider])
        
        return AssistantAgent(
            name=agent_config['name'],
            llm_config={"config_list": config_list},
            system_message=agent_config['system_message']
        )
    elif agent_config['type'] == 'user_proxy':
        return UserProxyAgent(
            name=agent_config['name'],
            human_input_mode=agent_config['settings']['human_input_mode'],
            max_consecutive_auto_reply=agent_config['settings']['max_consecutive_auto_reply']
        )
    else:
        raise ValueError(f"Unknown agent type: {agent_config['type']}")

agents = {agent['name']: create_agent(agent, config) for agent in config['agents']}

def handle_customer_inquiry(inquiry: str):
    agents['Human'].initiate_chat(
        agents['SupportManager'],
        message=f"New customer inquiry: {inquiry}"
    )

    responses = []
    for agent_name, messages in agents['Human'].chat_messages.items():
        for message in messages:
            if "content" in message and isinstance(message["content"], str):
                responses.append(f"{agent_name}: {message['content']}")

    return "\n\n".join(responses)

if __name__ == "__main__":
    customer_inquiry = "I'm having trouble logging into my account. Can you help?"
    support_conversation = handle_customer_inquiry(customer_inquiry)
    print("Customer Support Conversation:")
    print(support_conversation)