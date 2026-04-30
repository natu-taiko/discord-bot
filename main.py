import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 起動確認
@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")
    print("コマンド一覧:", bot.commands)

# メッセージ反応
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "うお" in message.content:
        await message.channel.send("冷笑まじかwwwwwwwww")

    # ←これが超重要（コマンド動かす）
    await bot.process_commands(message)

# 通話参加
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

# 通話退出
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("抜けた！")

# テストコマンド
@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")

# エラー表示
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"エラー: {error}")
    print("エラー内容:", error)

bot.run(os.getenv("TOKEN"))
