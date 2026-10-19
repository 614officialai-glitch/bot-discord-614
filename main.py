import os
from flask import Flask
from threading import Thread
import 【entity-discord¦canonical_name=discord】
from 【entity-discord¦canonical_name=discord】.ext import commands
from groq import Groq

# --- WEB para que Render no lo apague ---
app = Flask('')
@app.route('/')
def home():
    return "Bot 614 activo!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    Thread(target=run_web).start()

# --- BOT ---
intents = 【entity-discord¦canonical_name=discord】.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Si te mencionan, responde con Groq
    if bot.user in message.mentions:
        pregunta = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not pregunta:
            pregunta = "Hola"
        try:
            resp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": pregunta}]
            )
            await message.reply(resp.choices[0].message.content[:2000])
        except Exception as e:
            await message.reply(f"Error: {e}")
    
    await bot.process_commands(message)

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
