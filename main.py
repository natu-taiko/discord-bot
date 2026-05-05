import discord
from discord import app_commands
import random
import os
import json

# =========================
# 設定
# =========================
DATA_FILE = "data.json"

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# =========================
# 保存システム
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "xp": {},
            "level": {},
            "uou": {},
            "settings": {},
            "announce": {}
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "xp": xp,
            "level": level,
            "uou": uou_count,
            "settings": user_settings,
            "announce": guild_announce_channel
        }, f, ensure_ascii=False, indent=2)


# =========================
# データ読み込み
# =========================
data = load_data()

xp = data["xp"]
level = data["level"]
uou_count = data["uou"]
user_settings = data["settings"]
guild_announce_channel = data["announce"]


# =========================
# ランダム返信
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
    "おやすみ": ["おやすみなさい", "今日もお疲れ様", "一緒に寝るか？😎"],
    "きも": ["そうか、ごめん", "えへ//そういうこと言っちゃうんだ//♡♡"],
    "死ね": ["じゃあ死んでくる", "お前が死ね"],
    "ペニス": ["野獣先輩呼んでこようか？", "ヤるか？", "ｱｱｱｱｱｱｱｱｱｱｱｱｱｱｱ///////////"],
    "ちんこ": ["きも死ね", "俺のしゃぶれよ、あっ付いてなかった", "野獣先輩呼びます"],
    "gay": ["お前俺とヤる？", "Oh Shit...", "こいつがヤりたいってよ"],
    "そうですよ": ["そうだよ（便乗）", "おっ、そうだな（便乗）", "そうですよ（便乗）"],
    "お、おう": ["そっち系か～😅", "お、おう😅", "う、うお🤣"],
}

# =========================
# ユーザー設定取得
# =========================
def get_settings(user_id):
    if str(user_id) not in user_settings:
        user_settings[str(user_id)] = {
            "level": True,
            "reply": True,
            "uou": True
        }
    return user_settings[str(user_id)]


# =========================
# レベル計算
# =========================
def calc_level(x):
    return int(int(x) ** 0.5)


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

    user_id = str(message.author.id)
    text = message.content
    settings = get_settings(user_id)

    # XP
    xp[user_id] = int(xp.get(user_id, 0)) + 1
    new_lv = calc_level(xp[user_id])

    if settings["level"]:
        if level.get(user_id, 0) < new_lv:
            level[user_id] = new_lv
            await message.channel.send(f"{message.author.mention} Lv{new_lv}になった！🎉")
            save_data()

    # うおカウント
    if "うお" in text and settings["uou"]:
        uou_count[user_id] = int(uou_count.get(user_id, 0)) + 1
        await message.channel.send(f"{message.author.mention} うお回数: {uou_count[user_id]}")
        save_data()
        return

    # ランダム返信
    if settings["reply"]:
        for k, v in RESPONSES.items():
            if k in text:
                await message.channel.send(random.choice(v))
                return


# =========================
# 設定コマンド
# =========================
@tree.command(name="setting", description="機能ON/OFF")
async def setting(interaction: discord.Interaction, target: str, mode: str):

    settings = get_settings(str(interaction.user.id))

    if target not in ["level", "reply", "uou"]:
        await interaction.response.send_message("level / reply / uou", ephemeral=True)
        return

    settings[target] = (mode == "on")
    save_data()

    await interaction.response.send_message(f"{target} → {mode}", ephemeral=True)


# =========================
# 設定確認
# =========================
@tree.command(name="mysetting", description="設定確認")
async def mysetting(interaction: discord.Interaction):

    settings = get_settings(str(interaction.user.id))

    text = "\n".join([f"{k}: {'ON' if v else 'OFF'}" for k, v in settings.items()])
    await interaction.response.send_message(text, ephemeral=True)


# =========================
# レベル確認
# =========================
@tree.command(name="level", description="レベル確認")
async def level_cmd(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    await interaction.response.send_message(f"Lv {level.get(uid, 0)}")


# =========================
# うおランキング
# =========================
@tree.command(name="uou_rank", description="うおランキング")
async def uou_rank(interaction: discord.Interaction):

    sorted_users = sorted(uou_count.items(), key=lambda x: int(x[1]), reverse=True)

    text = ""
    for i, (uid, cnt) in enumerate(sorted_users[:5], 1):
        text += f"{i}位 <@{uid}> : {cnt}\n"

    await interaction.response.send_message(text or "まだデータなし")


# =========================
# お知らせチャンネル設定
# =========================
@tree.command(name="set_announce_channel", description="お知らせチャンネル設定")
async def set_announce_channel(interaction: discord.Interaction, channel: discord.TextChannel):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者のみ", ephemeral=True)
        return

    guild_announce_channel[str(interaction.guild.id)] = channel.id
    save_data()

    await interaction.response.send_message(f"{channel.mention} に設定したよ", ephemeral=True)


# =========================
# 全サーバーお知らせ
# =========================
@tree.command(name="announce_all", description="全サーバーにお知らせ")
async def announce_all(interaction: discord.Interaction, message: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者のみ", ephemeral=True)
        return

    embed = discord.Embed(title="📣 お知らせ", description=message, color=0xff4444)

    success = 0

    for guild in bot.guilds:

        cid = guild_announce_channel.get(str(guild.id))
        if not cid:
            continue

        channel = guild.get_channel(cid)
        if not channel:
            continue

        try:
            await channel.send(embed=embed)
            success += 1
        except:
            pass

    await interaction.response.send_message(f"送信完了: {success}サーバー", ephemeral=True)


# =========================
# サイコロ
# =========================
@tree.command(name="dice", description="サイコロ")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(str(random.randint(1, 6)))


# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
