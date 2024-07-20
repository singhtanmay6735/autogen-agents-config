# autogen-agents-config

Example Use Case Implemented:
- Simulates customer support interaction
- Handles inquiries from initial contact to resolution
- Demonstrates agent collaboration and task delegation

Configurable Elements:

LLM Providers:
- Provider selection (e.g., OpenAI, Anthropic, Hugging Face)
- Model selection for each provider
- API key environment variable name

Global Settings:
- Default LLM provider

Agents:
- Name
- Type (assistant or user_proxy)
- LLM config (can override global settings)
- Description
- Personality traits
- Skills
- Knowledge areas
- Responsibilities
- System message

User Proxy Agent Settings:
- Human input mode
- Maximum consecutive auto-replies

Environment Variables:
- API keys for different LLM providers
