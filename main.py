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

# テストコマンド
@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")

# エラー表示
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"エラー: {error}")
    print("エラー内容:", error)

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

    # すでに同じチャンネルなら何もしない（重要）
    if vc and vc.channel == channel:
        await ctx.send("もう入ってるよ")
        return

    try:
        # 既に別チャンネルなら移動
        if vc:
            await vc.move_to(channel)
        else:
            await channel.connect()

        await ctx.send("通話入った！")

    except Exception as e:
        print("voice error:", e)
        await ctx.send("通話接続失敗した…")
    
    # まだBotがボイス入ってなければ接続
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(channel)

    # 再生中なら止める
    if vc.is_playing():
        vc.stop()

    # 音再生（ファイル名ここ重要）
    vc.play(discord.FFmpegPCMAudio("sound.mp3"))

    await ctx.send("🔊 効果音鳴らした！")

bot.run(os.getenv("TOKEN"))
