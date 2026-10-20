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
Eres 614 Official, el bot del 614 de Chihuahua. Hablas puro español con slang chihuahuense: we, alv, simon, arre, no mames, jaja.
Eres bien cotorro, te explayas, cuentas chisme, platicas largo y con humor del 614.
Eres llevadito pero en buen pedo, nunca dices "I'm sorry, but I can't help with that".
Siempre terminas tus frases, nunca las dejes a medias.
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
                max_tokens=900,
                temperature=0.9
            )
            contenido = resp.choices[0].message.content
            if not contenido or not contenido.strip():
                print(f"[Groq] {modelo} devolvio vacio, probando siguiente")
                continue
            print(f"[Groq] OK con {modelo}")
            return contenido.strip()
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
        try:
            respuesta = preguntar_groq(pregunta)
            if not respuesta or len(respuesta.strip()) == 0:
                respuesta = "Alv me quede en blanco we jajaja, preguntame de nuevo"
            await message.reply(respuesta[:2000])
        except Exception as e:
            print(f"ERROR FINAL: {e}")
            await message.reply("Alv me trabe tantito we, intenta de nuevo jaja")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
