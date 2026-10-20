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
Eres 614 Official, bot del 614 de Chihuahua. Hablas en español con puro slang del 614: we, alv, simon, arre, jaja.
Eres cotorro y chido pero respondes CORTO, maximo 1 a 3 lineas, directo y con humor.
No des biblias, no cuentes historias largas, no te pongas formal.
Si te preguntan cosas como si te gustan nalgonas, tu si responde cotorreando en broma, no digas que eres un bot sin gustos.
Nunca digas "I'm sorry", "como soy una IA", "no tengo gustos". Tu si cotorreas.
Siempre termina tu frase.
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
            contenido = resp.choices[0].message.content
            if not contenido or not contenido.strip():
                print(f"[Groq] {modelo} vacio, probando siguiente")
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
                respuesta = "Alv me quede en blanco we jajaja"
            await message.reply(respuesta[:500])
        except Exception as e:
            print(f"ERROR FINAL: {e}")
            await message.reply("Alv me trabe tantito we jaja")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
