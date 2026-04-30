import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 起動確認
@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")
    print("コマンド一覧:", [c.name for c in bot.commands])

# メッセージ反応
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "うお" in message.content:
        await message.channel.send("うおおおお！")

    await bot.process_commands(message)

# 🔥 通話参加（ループ対策済み）
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

    # すでに同じチャンネルなら何もしない
    if vc and vc.channel == channel:
        await ctx.send("もう入ってるよ")
        return

    try:
        if vc:
            await vc.move_to(channel)
        else:
            await channel.connect()

        await ctx.send("通話入った！")

    except Exception as e:
        print("voice error:", e)
        await ctx.send("通話接続失敗")

# 🔥 通話退出
@bot.command()
async def leave(ctx):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("まだ通話入ってないよ")
        return

    await vc.disconnect()
    await ctx.send("抜けた！")

# 🔥 テスト
@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")

# 🔥 お知らせ機能（追加）
@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, text):
    await ctx.send(f"📢 お知らせ：{text}")

# 🔥 エラー表示
@bot.event
async def on_command_error(ctx, error):
    print("エラー:", error)
    await ctx.send(f"エラー: {error}")

bot.run(os.getenv("TOKEN"))
