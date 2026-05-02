import discord
from discord import app_commands
import random
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# =========================
# ランダム返信（完全版）
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
# カスタム返信
# =========================
custom_responses = {}

# =========================
# メモ機能
# =========================
memos = {}

# =========================
# レベルシステム
# =========================
xp = {}
level = {}

def get_level(x):
    return int(x ** 0.5)

# =========================
# 起動
# =========================
@bot.event
async def on_ready():
    await tree.sync()
    print(f"起動: {bot.user}")

# =========================
# メッセージ処理
# =========================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    text = message.content

    # XP
    user_id = message.author.id
    xp[user_id] = xp.get(user_id, 0) + 1

    new_level = get_level(xp[user_id])
    if user_id not in level or new_level > level[user_id]:
        level[user_id] = new_level
        await message.channel.send(f"{message.author.mention} レベル{new_level}になった！🎉")

    # うお優先
    if "うお" in text:
        await message.channel.send("冷笑まじか草wwww")
        return

    # カスタム返信
    for key, value in custom_responses.items():
        if key in text:
            await message.channel.send(value)
            return

    # 元のランダム返信（完全復活）
    for key in RESPONSES:
        if key in text:
            await message.channel.send(random.choice(RESPONSES[key]))
            return

    # AI風
    if random.random() < 0.03:
        await message.channel.send(random.choice([
            "それちょっと分かる",
            "深いなそれ…",
            "急にどうしたｗ",
            "まあそういう日もある"
        ]))

# =========================
# /learn
# =========================
@tree.command(name="learn")
async def learn(interaction: discord.Interaction, word: str, reply: str):
    custom_responses[word] = reply
    await interaction.response.send_message(f"{word} を覚えた！")

# =========================
# /remind
# =========================
@tree.command(name="remind")
async def remind(interaction: discord.Interaction, sec: int, msg: str):
    await interaction.response.send_message(f"{sec}秒後に通知するよ！")
    await asyncio.sleep(sec)
    await interaction.followup.send(msg)

# =========================
# /dice
# =========================
@tree.command(name="dice")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 {random.randint(1,6)}")

# =========================
# /memo
# =========================
@tree.command(name="memo")
async def memo(interaction: discord.Interaction, text: str):
    memos[interaction.user.id] = text
    await interaction.response.send_message("保存した！")

# =========================
# /mymemo
# =========================
@tree.command(name="mymemo")
async def mymemo(interaction: discord.Interaction):
    text = memos.get(interaction.user.id, "メモないよ")
    await interaction.response.send_message(text)

# =========================
# /level
# =========================
@tree.command(name="level")
async def level_cmd(interaction: discord.Interaction):
    lv = level.get(interaction.user.id, 0)
    await interaction.response.send_message(f"あなたのレベル: {lv}")

# =========================
# /test
# =========================
@tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("動いてる！")

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
