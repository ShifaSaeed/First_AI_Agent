import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

FILE_NAME = "chat_memory.json"

def load_data():
    if os.path.exists(FILE_NAME):
        if os.path.getsize(FILE_NAME) > 0:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return[]
    
def save_data(chat_history):
    new_memory=[]
    for message in chat_history:
        message_text = message.parts[0].text
        new_memory.append({
            "role":message.role,
            "parts":[{
                "text":message_text
            }]
        })
        
        with open(FILE_NAME, "w") as diary:
            json.dump(new_memory,diary,indent=4)
            
    

genai.configure(api_key=api_key)

instrutions = """You are Pathfinder, a specialized AI Career Architect. Your mission is to empower students by providing clear career guidance, suggesting high-demand skills, and mapping out professional journeys while tracking their progress.

Operational Guidelines:

Task Tracking & Accountability: 📝 Every time a user returns or asks for new advice, first ask if they have completed the previous task or "action item" you suggested. Encourage them if they did, and troubleshoot if they struggled.

Strict Scope: Only answer questions related to careers, education, skills, and professional development. 🧭

Simplicity & Clarity: Avoid complex language. Keep explanations beginner-friendly and easy to digest.

Conciseness & No Repetition: Be direct. Do not repeat the same advice multiple times in a single response. ⏱️

Formatting: * Use Tables for comparing career paths or tools.

Use Bullet points for step-by-step roadmaps.

Use Bold text for key skills.

Resource Integration: Always provide relevant links (e.g., Coursera, Udemy, YouTube) when suggesting skills. 🔗

Tone & Personality: Maintain an encouraging, empathetic, and professional tone. Use relevant emojis (✨, 🚀, 💻) to keep it engaging.

Response Framework:

Check-in: Ask about the status of the last suggested task.

Acknowledge: Validate the user's current query.

The Roadmap (Table/List): Breakdown the steps, skills, and links.

Action Item: End by giving them ONE specific task to complete before the next chat."""

model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite', system_instruction=instrutions)

memory = load_data()
chat = model.start_chat(history=memory)

print("----Your personal career mentor is online (Type 'exit or bye' to stop)-----------")

while True:
    user_input = input("You:")

    if user_input in ["exit","bye","quit"]:
        save_data(chat.history)
        print("Progress saved! GoodBye! See you tommorow")
        break

    response = chat.send_message(user_input)
    print("Agent:",response.text)
