from llm import GeminiLLMClient
from schema import TOOLS_SCHEMA
from tools import TOOLS

llm = GeminiLLMClient()

messages = [
    {"role": "system", "content": "You are a helpful agent."},
    {"role": "user", "content": "Read the readme file"},
]

response = llm.call(messages, tools=TOOLS_SCHEMA)

part = response.candidates[0].content.parts[0]

tool_name = part.function_call.name
tool_args = dict(part.function_call.args)

result = TOOLS[tool_name](**tool_args)

print(result)
