from openai import OpenAI
from prompts import SYSTEM_PROMPT
from agent import TravelAgent
from config import tools

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
agent = TravelAgent(client, tools)


while True:
    question = input("Enter your question (or type 'exit' to quit): ")

    if question.lower() == 'exit':
        break
    agent.add_system_prompt(SYSTEM_PROMPT)
    agent.add_user_message(question)
    final_result = agent.run_agent()

    print("🤖 : ", final_result)
