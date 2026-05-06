🌙 Luna AI | Discord Bot
Luna is a high-energy, "bratty teen" Discord bot inspired by Resident Evil 4 (and her obsession with Leon). She isn't your typical polite assistant—she’s fun, opinionated, and uses either Groq (Llama 3.3) or Gemini 2.0 Flash Lite to power her brain.

✨ Features
Dual-Brain Support: Choose between Groq or Google Gemini via a simple config.

Persistent Memory: She remembers your conversations (even after a restart).

Web-Aware: She can search the internet to answer your questions.

Dynamic Moods: Her personality shifts based on how you treat her.

Owner Commands: Can launch apps like Steam, Discord, or RE4 directly from your PC.

Bookwork Memory: Integrated logic for handling school-specific logging (SparkAI compatible).

🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.8+ installed. You will also need the following libraries:

Bash
pip install discord.py groq google-generativeai googlesearch-python


2. Configuration
Create a config.json file in the main folder:

JSON
{
  "DISCORD_TOKEN": "YOUR_TOKEN",
  "AI_PROVIDER": "gemini", 
  "GROQ_KEY": "YOUR_GROQ_KEY",
  "GEMINI_KEY": "YOUR_GEMINI_KEY",
  "SHADOW_ID": 1167246675828551791,
  "SHADOW_NAME": "Shadow",
  "JADE_ID": 0
}
Set AI_PROVIDER to either "groq" or "gemini".

3. Run Luna
Bash
python luna.py
🛠️ Commands
@Luna [question] — Chat with her.

!open [app name] — (Owner only) Launch PC apps like Steam or Chrome.

talk to jade — Triggers a specific conversation loop between bot personas.

📂 Project Structure
luna.py — The main bot logic.

config.json — Your private keys (DO NOT share this).

luna_memory.json — Where Luna stores her chat history.

.gitignore — Prevents your keys from being leaked to GitHub.

🤝 Contributing
Luna is open source! Feel free to fork the repo, add more "bratty" prompts, or improve the search tools.

Created by Archive_Software
