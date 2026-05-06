import discord
from discord.ext import commands
import asyncio
import json
import os
import io
import subprocess
from collections import deque
from googlesearch import search

# NEW: Import both AI libraries
from groq import Groq
import google.generativeai as genai

# --- 1. LOAD CONFIGURATION ---
if not os.path.exists("config.json"):
    print("❌ ERROR: config.json not found! Create one based on the template.")
    exit()

with open("config.json", "r") as f:
    config = json.load(f)

# Initialize AI Clients
ai_provider = config.get("AI_PROVIDER", "groq").lower()
client_groq = None
model_gemini = None

if ai_provider == "groq":
    client_groq = Groq(api_key=config["GROQ_KEY"])
    print("✅ Luna using Groq (Llama 3.3)")
else:
    genai.configure(api_key=config["GEMINI_KEY"])
    model_gemini = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
    print("✅ Luna using Gemini 2.0 Flash Lite")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
chat_counter = 0

# --- 2. PERSISTENT MEMORY ---
MEMORY_FILE = "luna_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with io.open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return deque(json.load(f), maxlen=100)
        except:
            return deque(maxlen=100)
    return deque(maxlen=100)

def save_memory(mem_deque):
    with io.open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(mem_deque), f)

global_memory = load_memory()

# --- 3. TOOLS ---
async def async_web_search(query):
    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, lambda: list(search(query, num_results=3)))
        return "\n".join(results) if results else "nothing found."
    except:
        return "the internet is trash."

# --- 4. THE BRAIN (Universal Wrapper) ---
async def get_luna_response(question):
    search_context = ""
    if any(word in question.lower() for word in ["who", "what", "where", "how"]):
        info = await async_web_search(question)
        search_context = f"\n(Web Info: {info})"

    system_prompt = (
        f"You are Luna. Bratty, fun teen girl. Obsessed with RE4 and Leon. "
        f"Creator: {config['SHADOW_NAME']}. lowercase only. "
        f"Context: {search_context}"
    )

    try:
        if ai_provider == "groq":
            # Groq/Llama Logic
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(list(global_memory))
            messages.append({"role": "user", "content": question})
            completion = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8
            )
            answer = completion.choices[0].message.content.lower()
        
        else:
            # Gemini Logic
            # Convert deque memory to Gemini history format
            chat = model_gemini.start_chat(history=[])
            full_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {question}"
            response = chat.send_message(full_prompt)
            answer = response.text.lower()

        global_memory.append({"role": "user", "content": question})
        global_memory.append({"role": "assistant", "content": answer})
        save_memory(global_memory)
        return answer

    except Exception as e:
        return f"um my brain is fried: {str(e)}"

# --- 5. EVENTS ---
@bot.event
async def on_ready():
    print(f"✅ LUNA IS LIVE AS {bot.user}")

@bot.event
async def on_message(message):
    global chat_counter
    if message.author == bot.user: return
    
    if message.author.id == config["SHADOW_ID"]:
        chat_counter = 0

    # Logic for Jade
    is_jade = message.author.id == config["JADE_ID"]
    
    if bot.user.mentioned_in(message) or (is_jade and chat_counter < 5):
        async with message.channel.typing():
            clean_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
            
            # App launcher (Only for Owner)
            if message.author.id == config["SHADOW_ID"] and "open" in clean_text.lower():
                 # (Keep your subprocess logic here)
                 pass

            response = await get_luna_response(clean_text)
            
            if is_jade:
                chat_counter += 1
                if chat_counter == 5:
                    response += " anyway i'm bored now. go away."
            
            await message.reply(response)

bot.run(config["DISCORD_TOKEN"])