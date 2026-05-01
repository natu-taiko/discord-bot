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
# ランダム返信データ
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "やばい": ["それは草", "まじで？", "終わったなｗ"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
}

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    try:
        await tree.sync()
        print(f"起動: {bot.user}")
    except Exception as e:
        print("SYNC ERROR:", e)

# =========================
# メッセージ反応（うお＋ランダム）
# =========================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    text = message.content

    # ① うお優先（暴走防止）
    if "うお" in text:
        await message.channel.send("冷笑まじか草wwww")
        await bot.process_commands(message)
        return

    # ② ランダム返信
    for key in RESPONSES:
        if key in text:
            await message.channel.send(random.choice(RESPONSES[key]))
            break

    await bot.process_commands(message)

# =========================
# /join（通話安定版）
# =========================
@tree.command(name="join", description="ボイスチャンネルに参加")
async def join(interaction: discord.Interaction):

    if not interaction.user.voice:
        await interaction.response.send_message("先に通話入って！", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    try:
        # 同じチャンネルなら何もしない
        if vc and vc.is_connected() and vc.channel == channel:
            await interaction.response.send_message("もう入ってるよ", ephemeral=True)
            return

        # 別チャンネルなら移動
        if vc and vc.is_connected():
            await vc.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message("通話入った！")

    except Exception as e:
        print("VOICE ERROR:", e)

        # 壊れたVCだけ掃除（安全）
        try:
            vc = interaction.guild.voice_client
            if vc:
                await vc.disconnect()
        except:
            pass

        await interaction.response.send_message("接続失敗")

# =========================
# /leave
# =========================
@tree.command(name="leave", description="ボイスチャンネルから退出")
async def leave(interaction: discord.Interaction):

    vc = interaction.guild.voice_client

    if not vc or not vc.is_connected():
        await interaction.response.send_message("まだ通話入ってないよ", ephemeral=True)
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
