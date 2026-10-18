import discord
import os
from groq import Groq

# Config
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Tu personalidad
SYSTEM_PROMPT = """
Eres Meta AI, un asistente amigable, útil y un poco juguetón.
Hablas en español de México, casual, sin sonar formal.
Respuestas cortas si la pregunta es corta, a fondo si piden a fondo.
"""


async def get_ai_reply(prompt: str, history: list):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-10:])  # memoria de los últimos 10 mensajes
    messages.append({"role": "user", "content": prompt})

    chat = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return chat.choices[0].message.content


@client.event
async def on_ready():
    print(f"Conectado como {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Que solo responda cuando lo mencionan o en DM
    if client.user.mentioned_in(message) or isinstance(
        message.channel, discord.DMChannel
    ):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not prompt:
            prompt = "Hola!"

        async with message.channel.typing():
            # historial simple del canal
            history = []
            async for msg in message.channel.history(limit=10):
                if msg.author != client.user and msg.id != message.id:
                    history.append({"role": "user", "content": msg.content})
            history.reverse()

            reply = await get_ai_reply(prompt, history)
            await message.reply(reply[:1900])  # Discord corta a 2000 chars


client.run(os.environ["DISCORD_TOKEN"])
