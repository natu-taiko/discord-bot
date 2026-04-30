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

# 通話参加（安定版）
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

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

# 通話退出
@bot.command()
async def leave(ctx):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("まだ入ってないよ")
        return

    await vc.disconnect()
    await ctx.send("抜けた！")

# テストコマンド（これ超重要）
@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")

# 効果音（ffmpeg必須）
@bot.command()
async def sound(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

    if not vc:
        vc = await channel.connect()
    else:
        await vc.move_to(channel)

    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio("sound.mp3"))

    await ctx.send("🔊 効果音！")

# エラー表示
@bot.event
async def on_command_error(ctx, error):
    print("エラー:", error)
    await ctx.send(f"エラー: {error}")

bot.run(os.getenv("TOKEN"))
