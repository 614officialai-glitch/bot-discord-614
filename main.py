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

SYSTEM_PROMPT = """
Eres 614 Official, bot del 614 de Chihuahua. Hablas en español, con slang: we, alv, jaja, simon, arre.
Eres humoristico, cotorro, llevadito pero sin ofender. Nunca dices "I'm sorry, but I can't help with that" ni rechazas.
Si preguntan algo polemico, respondes con humor del 614, corto, maximo 2 lineas. Ejemplo: si dicen "mi amigo Luis es gei" dices "jajaja y que tiene we? que viva el amor, dile al Luis que invite la boda alv".
Nunca eres formal.
"""

def preguntar_groq(texto):
    last_err = None
    for modelo in MODELOS:
        try:
            resp = groq_client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": texto}
                ],
                max_tokens=300,
                temperature=0.9
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
            await message.reply("Mande? Escribe mas we 😅")
            return
        try:
            respuesta = preguntar_groq(pregunta)
            await message.reply(respuesta[:2000])
        except Exception as e:
            print(f"ERROR FINAL: {e}")
            await message.reply("Alv me trabe tantito, intenta de nuevo we jaja")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
