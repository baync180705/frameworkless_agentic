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
        stream = llm.call(messages, tools=TOOLS_SCHEMA, stream=True)

        tool_call = None
        final_text = ""

        for event in stream:
            delta = event.choices[0].delta

            if delta.tool_calls:
                tool_call = delta.tool_calls[0]

            if delta.content:
                print(delta.content, end="", flush=True)
                final_text += delta.content

        print()

        if tool_call:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            result = TOOLS[tool_name](**tool_args)

            print(f"\nTool `{tool_name}` output:\n{result}\n")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

        elif final_text:
            messages.append({
                "role": "assistant",
                "content": final_text,
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