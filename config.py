from prompts import SYSTEM_PROMPT


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
],
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