import discord
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# 🔒 通話接続ロック（ループ防止）
connecting = {}

# =========================
# ランダム返信データ
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
    "おやすみ": ["おやすみなさい", "今日もお疲れ様", "一緒に寝るか？😎"],
    "きも": ["そうか、ごめん", "えへ//そういうこと言っちゃうんだ//♡♡", "なんで人にきもとか言えるの？鏡見てこいよ"],
    "そうだよ": ["そうだよ（便乗）", "おっ、そうだな（便乗）", "そうですよ（便乗）"],
    "死ね": ["じゃあ死んでくる", "お前が死ね", "だってさお前死ねよ"],
    "ペニス": ["野獣先輩呼んでこようか？", "ヤるか？", "ｱｱｱｱｱｱｱｱｱｱｱｱｱｱｱ///////////"],
    "ちんこ": ["きも死ね", "俺のしゃぶれよ、あっ付いてなかった", "野獣先輩呼びます"],
    "gay": ["お前俺とヤる？", "Oh Shit...", "こいつがヤりたいってよ"],
    "そうですよ": ["そうだよ（便乗）", "おっ、そうだな（便乗）", "そうですよ（便乗）"],
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
# メッセージ反応
# =========================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    text = message.content

    # うお優先
    if "うお" in text:
        await message.channel.send("冷笑まじか草wwww")
        return

    # ランダム返信
    for key in RESPONSES:
        if key in text:
            await message.channel.send(random.choice(RESPONSES[key]))
            break

# =========================
# /join（完全安定版）
# =========================
@tree.command(name="join", description="ボイスチャンネルに参加")
async def join(interaction: discord.Interaction):

    guild_id = interaction.guild.id

    # 🔒 接続中なら拒否（ループ防止）
    if connecting.get(guild_id):
        await interaction.response.send_message("接続中だからちょっと待って", ephemeral=True)
        return

    connecting[guild_id] = True

    try:
        if not interaction.user.voice:
            await interaction.response.send_message("先に通話入って！", ephemeral=True)
            return

        channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client

        # 同じVCなら何もしない
        if vc and vc.is_connected() and vc.channel == channel:
            await interaction.response.send_message("もう入ってるよ", ephemeral=True)
            return

        # 接続処理
        if vc and vc.is_connected():
            await vc.move_to(channel)
        else:
            await channel.connect(timeout=10, reconnect=False)

        await interaction.response.send_message("通話入った！")

    except Exception as e:
        print("VOICE ERROR:", e)
        await interaction.response.send_message("接続失敗")

    finally:
        connecting[guild_id] = False

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
