import discord
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# =========================
# ランダム反応データ
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "やばい": ["それは草", "まじで？", "終わったなｗ"],
    "草": ["草ｗｗｗ", "わかる", "それな"]
}

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    await tree.sync()
    print(f"起動: {bot.user}")

# =========================
# ランダム反応
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content

    for key in RESPONSES:
        if key in text:
            await message.channel.send(random.choice(RESPONSES[key]))
            break

    await bot.process_commands(message)

# =========================
# /join（通話参加）
# =========================
@tree.command(name="join", description="ボイスチャンネルに参加")
async def join(interaction: discord.Interaction):

    if not interaction.user.voice:
        await interaction.response.send_message("先に通話入って！", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    try:
        if vc and vc.channel == channel:
            await interaction.response.send_message("もう入ってるよ", ephemeral=True)
            return

        if vc:
            await vc.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message("通話入った！")

    except Exception as e:
        print("voice error:", e)
        await interaction.response.send_message("接続失敗")

# =========================
# /leave（退出）
# =========================
@tree.command(name="leave", description="ボイスチャンネルから退出")
async def leave(interaction: discord.Interaction):

    vc = interaction.guild.voice_client

    if not vc:
        await interaction.response.send_message("まだ入ってないよ", ephemeral=True)
        return

    await vc.disconnect()
    await interaction.response.send_message("抜けた！")

# =========================
# /test
# =========================
@tree.command(name="test", description="動作確認")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("動いてる！")

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
