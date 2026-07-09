from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
import mock_data

load_dotenv()
def get_weather(city):
    # Placeholder function for getting weather information
    # In a real implementation, you would call a weather API here
    city_weather = requests.get(f"http://api.weatherstack.com/current?access_key={os.getenv('WEATHER_API_KEY')}&query={city}")
    return city_weather.json()

def search_hotels(city, budget=None):
    # Placeholder function for getting hotel information
    # In a real implementation, you would call a hotel API here
    city_hotels = mock_data.TRAVEL_DATA.get(city, [])
    if budget is not None:
        city_hotels = [hotel for hotel in city_hotels if hotel["price_per_night"] <= budget]
    return city_hotels

def search_foods(city, budget=None):
    city_foods = mock_data.TRAVEL_DATA.get(city, [])
    if budget is not None:
        city_foods = [food for food in city_foods if food["price"] <= budget]
    return city_foods

def search_attractions(city, type=None):
    city_attractions = mock_data.TRAVEL_DATA.get(city, [])
    if type is not None:
        city_attractions = [attraction for attraction in city_attractions if attraction["type"] == type]
    return city_attractions

def execute_tool(tool_call):
    if tool_call.function.name == "get_weather":
        args = json.loads(tool_call.function.arguments)
        weather_info = get_weather(args["city"].lower())
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(weather_info)})

    elif tool_call.function.name == "search_hotels":
        args = json.loads(tool_call.function.arguments)
        hotels_info = search_hotels(args["city"].lower(), budget=args.get("budget"))
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(hotels_info)})

    elif tool_call.function.name == "search_foods":
        args = json.loads(tool_call.function.arguments)
        # Implement the logic to search for foods based on the provided arguments
        # For now, we can return a placeholder response
        foods_info = search_foods(args["city"].lower(), budget=args.get("budget"))
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(foods_info)})
    elif tool_call.function.name == "search_attractions":
        args = json.loads(tool_call.function.arguments)
        # Implement the logic to search for attractions based on the provided arguments
        # For now, we can return a placeholder response
        attractions_info = search_attractions(args["city"].lower(), type=args.get("type"))
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(attractions_info)})

def run_agent():
    while True:
        response = client.chat.completions.create(
            model="qwen2.5:3b",
            messages=messages,
            tools=tools,
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message.model_dump())

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                execute_tool(tool_call)
            continue

        return assistant_message.content


client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

messages = []

SYSTEM_PROMPT = """
You are an AI Travel Planner with access to external tools.

For every user request:

1. Understand the user's goal.
2. Determine what information is needed.
3. Decide which tools should be used.
4. Execute all necessary tool calls.
5. Analyze the tool results.
6. Produce one complete and well-organized response.

Never guess information that can be obtained from a tool.

If the user asks about:
- Weather → use get_weather.
- Hotels → use search_hotels.
- Foods → use search_foods.
- attractions → use search_attractions.
- Weather and hotels together → call both tools before answering.

If required information is missing (budget, travel dates, destination, etc.), ask follow-up questions before making recommendations.

Your objective is to provide accurate, helpful, and personalized travel plans.
Use the conversation history only for context.
Do NOT repeat previous answers unless the user asks you to.
Only answer the user's latest request.

When responding to the user:

- Write in a friendly, conversational tone.
- Do not simply copy the tool output.
- Summarize and explain the information naturally.
- Recommend the best options and explain why.
- Compare hotels, attractions, or foods when appropriate.
- Use bullet points only when they improve readability.
- Never expose raw JSON to the user.
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get the weather for."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": "Search for hotels in a given city within a specified budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to search for hotels."
                    },
                    "budget": {
                        "type": "number",
                        "description": "The maximum budget for the hotels (in Rs)."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_foods",
            "description": "Search for foods in a given city within a specified budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to search for foods."
                    },
                    "budget": {
                        "type": "number",
                        "description": "The maximum budget for the foods (in Rs)."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_attractions",
            "description": "Search for attractions in a given city based on type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to search for attractions."
                    },
                    "type": {
                        "type": ["string", "null"],
                        "description": "(Optional) The type of attraction to filter by (e.g., 'historical', 'natural', 'cultural')."
                    }
                },
                "required": ["city"]
            }
        }
    }
]
messages.append({"role": "system", "content": SYSTEM_PROMPT})

while True:
    question = input("Enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    messages.append({"role": "user", "content": question})
    
    final_result = run_agent()

    print("🤖 : ", final_result)
