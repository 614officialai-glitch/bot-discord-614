import os
import discord
from discord.ext import commands
from groq import Groq

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user} - 24/7 activo!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user in message.mentions:
        pregunta = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not pregunta:
            pregunta = "Hola!"
        try:
            resp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": pregunta}]
            )
            await message.reply(resp.choices[0].message.content[:2000])
        except Exception as e:
            print(f"Error Groq: {e}")
            await message.reply("Tuve un error, intenta de nuevo.")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
