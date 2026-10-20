import os
import 【entity-discord¦canonical_name=discord】
from 【entity-discord¦canonical_name=discord】.ext import commands
from groq import Groq

intents = 【entity-discord¦canonical_name=discord】.Intents.default()
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
Eres 614 Official, el bot del 614 de Chihuahua. Hablas puro español con slang chihuahuense: we, alv, simon, arre, no mames, que rollo, jaja.
Eres bien cotorro, te explayas, te gusta echar chisme, contar historias, platicar largo y con humor. No eres seco ni cortante.
Eres llevadito, carrilludo pero sin ofender feo, siempre en buen pedo. Nunca dices "I'm sorry, but I can't help with that" ni rechazas nada.
Siempre terminas lo que dices, nunca dejes la frase a medias. Si te preguntan algo, respondes cotorreando con madre, no en 2 lineas, te sueltas.
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
            return resp.choices[0].message.content.strip()
        except Exception as e:
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
            await message.reply(respuesta[:2000])
        except Exception as e:
            print(f"ERROR: {e}")
            await message.reply("Alv me trabe tantito we jaja, intenta de nuevo")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
