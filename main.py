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

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("通話入った！")
    else:
        await ctx.send("先に通話入って！")
