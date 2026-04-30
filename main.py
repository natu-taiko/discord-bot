import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "うお" in message.content:
        await message.channel.send("冷笑まじかwwwwwwww")

    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))

responses = {
    "死ね": "逆に殺してやろうか",
    "そうだよ": "便乗botと同じように便乗してやるよ！",
    "おはよう": "おはよー！",
    "こんにちわ": "こんにちわ"
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for word, reply in responses.items():
        if word in message.content:
            await message.channel.send(reply)
            break

    await bot.process_commands(message)

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send("通話入った！")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("抜けた！")

@bot.event
async def on_command_error(ctx, error):
    print("エラー内容:", error)
