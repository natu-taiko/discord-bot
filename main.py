import discord
from discord.ext import commands, tasks
from datetime import datetime
import os

# =========================
# 初期設定
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# お知らせ送信先チャンネルID
CHANNEL_ID = 1473243172288069743  # ←ここ変更

# =========================
# 起動時
# =========================
@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")
    print("コマンド一覧:", [c.name for c in bot.commands])
    daily_announce.start()

# =========================
# メッセージ反応
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "うお" in message.content:
        await message.channel.send("冷笑まじか草wwwwwwwww")

    await bot.process_commands(message)

# =========================
# 通話参加（安定版）
# =========================
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

# =========================
# 通話退出
# =========================
@bot.command()
async def leave(ctx):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("まだ通話入ってないよ")
        return

    await vc.disconnect()
    await ctx.send("抜けた！")

# =========================
# テスト
# =========================
@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")

# =========================
# 手動お知らせ（管理者のみ）
# =========================
@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, *, text):
    await ctx.send(f"📢 お知らせ：{text}")

# =========================
# 自動お知らせ（例：20時）
# =========================
sent_today = False

@tasks.loop(minutes=1)
async def daily_announce():
    global sent_today

    now = datetime.now()

    # 例：20:00に1回だけ送信
    if now.hour == 0 and now.minute == 10:
        if not sent_today:
            channel = bot.get_channel(1473243172288069743)
            if channel:
                await channel.send("📢 定期メンテナンスのお知らせ")
            sent_today = True
    else:
        sent_today = False

# =========================
# エラー処理
# =========================
@bot.event
async def on_command_error(ctx, error):
    print("エラー:", error)
    await ctx.send(f"エラー: {error}")

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
