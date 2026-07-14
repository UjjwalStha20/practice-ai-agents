import json
from openai import OpenAI
from tools import get_weather, search_hotels, search_foods, search_attractions
from config import tools
from prompts import SYSTEM_PROMPT

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class TravelAgent:
    def __init__(self, client, tools):
        self.messages = []
        self.client = client
        self.tools = tools
    
    def add_system_prompt(self, message):
        self.messages.append({"role": "system", "content": message})

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def execute_tool(self, tool_call):
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            weather_info = get_weather(args["city"].lower())
            self.messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(weather_info)})

        elif tool_call.function.name == "search_hotels":
            args = json.loads(tool_call.function.arguments)
            hotels_info = search_hotels(args["city"].lower(), budget=args.get("budget"))
            self.messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(hotels_info)})

        elif tool_call.function.name == "search_foods":
            args = json.loads(tool_call.function.arguments)
            # Implement the logic to search for foods based on the provided arguments
            # For now, we can return a placeholder response
            foods_info = search_foods(args["city"].lower(), budget=args.get("budget"))
            self.messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(foods_info)})
        elif tool_call.function.name == "search_attractions":
            args = json.loads(tool_call.function.arguments)
            # Implement the logic to search for attractions based on the provided arguments
            # For now, we can return a placeholder response
            attractions_info = search_attractions(args["city"].lower(), type=args.get("type"))
            self.messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(attractions_info)})

    def run_agent(self):
        while True:
            response = self.client.chat.completions.create(
                model="qwen2.5:3b",
                messages=self.messages,
                tools=tools,
            )

            assistant_message = response.choices[0].message

            self.messages.append(assistant_message.model_dump())

            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    self.execute_tool(tool_call)
                continue

            return assistant_message.content

