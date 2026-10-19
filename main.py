import os
import discord
from discord.ext import commands
from groq import Groq

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELOS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "qwen/qwen3-32b"
]

def preguntar_groq(texto):
    last_err = None
    for modelo in MODELOS:
        try:
            resp = groq_client.chat.completions.create(
                model=modelo,
                messages=[{"role": "user", "content": texto}],
                max_tokens=500
            )
            print(f"[Groq] OK con {modelo}")
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[Groq] {modelo} fallo: {e}")
            last_err = e
            continue
    raise last_err

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user} - 24/7 activo!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        pregunta = message.content.replace(f'<@{bot.user.id}>','').replace('@614 Official','').strip()
        if not pregunta:
            pregunta = "Hola!"
        if len(pregunta) < 2:
            await message.reply("¿Mande? Escribe algo más 😅")
            return
        try:
            respuesta = preguntar_groq(pregunta)
            await message.reply(respuesta[:2000])
        except Exception as e:
            print(f"ERROR FINAL: {e}")
            await message.reply("Tuve un error con Groq, pero ya estoy conectado. Intenta de nuevo.")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
