import discord
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# 🔒 接続ロック
connecting = {}

# =========================
# ランダム返信データ
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
}

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    await tree.sync()
    print(f"起動: {bot.user}")

# =========================
# メッセージ反応
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content

    if "うお" in text:
        await message.channel.send("冷笑まじか草wwww")
        return

    for key in RESPONSES:
        if key in text:
            await message.channel.send(random.choice(RESPONSES[key]))
            break

# =========================
# /join（最終安定版）
# =========================
@tree.command(name="join")
async def join(interaction: discord.Interaction):

    guild = interaction.guild
    guild_id = guild.id

    if connecting.get(guild_id):
        await interaction.response.send_message("接続中…ちょい待って", ephemeral=True)
        return

    connecting[guild_id] = True

    try:
        if not interaction.user.voice:
            await interaction.response.send_message("先に通話入って！", ephemeral=True)
            return

        channel = interaction.user.voice.channel
        vc = guild.voice_client

        # 既に同じ場所
        if vc and vc.is_connected():
            if vc.channel == channel:
                await interaction.response.send_message("もう入ってる", ephemeral=True)
                return

            await vc.move_to(channel)
            await interaction.response.send_message("移動した！")
            return

        # 新規接続
        vc = await channel.connect(timeout=15)
        await interaction.response.send_message("通話入った！")

    except Exception as e:
        print("JOIN ERROR:", e)
        await interaction.response.send_message("接続失敗")

    finally:
        connecting[guild_id] = False

# =========================
# /leave（最終安定版）
# =========================
@tree.command(name="leave")
async def leave(interaction: discord.Interaction):

    vc = interaction.guild.voice_client

    if not vc or not vc.is_connected():
        await interaction.response.send_message("入ってないよ", ephemeral=True)
        return

    await vc.disconnect(force=True)
    await interaction.response.send_message("抜けた！")

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
