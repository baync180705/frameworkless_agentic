import json
from llm import DeepSeekLLMClient
from schema import TOOLS_SCHEMA
from tools import TOOLS

llm: DeepSeekLLMClient = DeepSeekLLMClient()

SYSTEM_PROMPT: str = """
You are an autonomous agent.
You can think step by step and use tools when needed.
Stop when the task is complete.
"""

def run_agent(messages: list, MAX_STEPS: int = 10):

    for _ in range(MAX_STEPS):
        response = llm.call(messages, tools=TOOLS_SCHEMA)

        message = response.choices[0].message

        if message.tool_calls:
            call = message.tool_calls[0]
            tool_name = call.function.name
            tool_args = json.loads(call.function.arguments)

            if tool_name not in TOOLS:
                raise RuntimeError(f"Unknown tool: {tool_name}")

            result = TOOLS[tool_name](**tool_args)

            print(f"\nTool `{tool_name}` output:\n{result}\n")

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

        elif message.content:
            print(message.content)

            messages.append({
                "role": "assistant",
                "content": message.content
            })
            break

        else:
            raise RuntimeError("Unhandled response type")
        

def repl():
    messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]

    print("🔹 AI Agent started. Type 'exit' or press Ctrl+C to quit.\n")

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("\nSession ended.")
                break

            if not user_input:
                continue

            messages.append({
                "role": "user",
                "content": user_input
            })

            run_agent(messages)

    except KeyboardInterrupt:
        print("\n\nSession terminated (Ctrl+C).")