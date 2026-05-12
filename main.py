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
# データ保存（安全版）
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "xp": {},
            "level": {},
            "uou": {},
            "settings": {},
            "announce": {},
            "afk": {}
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 型ズレ防止
    data["xp"] = {str(k): v for k, v in data.get("xp", {}).items()}
    data["level"] = {str(k): v for k, v in data.get("level", {}).items()}
    data["uou"] = {str(k): v for k, v in data.get("uou", {}).items()}
    data["settings"] = {str(k): v for k, v in data.get("settings", {}).items()}
    data["announce"] = {str(k): v for k, v in data.get("announce", {}).items()}
    data["afk"] = {str(k): v for k, v in data.get("afk", {}).items()}

    return data


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "xp": {str(k): v for k, v in xp.items()},
            "level": {str(k): v for k, v in level.items()},
            "uou": {str(k): v for k, v in uou_count.items()},
            "settings": user_settings,
            "announce": guild_announce_channel,
            "afk": afk_data
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
afk_data = data["afk"]


# =========================
# 返信データ
# =========================
RESPONSES = {
    "おはよう": ["おはよ〜！", "今日もがんばろ🔥", "起きた？"],
    "こんにちは": ["こんにちは！", "いい感じだね👍", "元気？"],
    "草": ["草ｗｗｗ", "わかる", "それな"],
    "おやすみ": ["おやすみなさい", "今日もお疲れ様"],
    "死ね": ["じゃあ死んでくる", "お前が死ね"],
    "きも": ["そうか、ごめん", "えへ//"],
    "ペニス": ["野獣先輩呼んでこようか？", "ヤるか？"],
    "ちんこ": ["きも死ね", "俺のしゃぶれよ"],
    "gay": ["お前俺とヤる？", "Oh Shit..."],
    "そうですよ": ["そうだよ（便乗）"],
    "お、おう": ["そっち系か～😅", "お、おう😅", "う、うお🤣"],
    "そうだよ": ["そうだよ（便乗）", "そうっすね～（便乗）", "そうですよ（便乗）"],
}


# =========================
# 設定取得
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

    # =========================
    # AFK解除
    # =========================
    if user_id in afk_data:

        del afk_data[user_id]
        save_data()

        await message.channel.send(
            f"{message.author.mention} AFK解除！おかえり〜"
        )

    # =========================
    # AFK通知
    # =========================
    for user in message.mentions:

        uid = str(user.id)

        if uid in afk_data:
            await message.channel.send(
                f"{user.display_name} はAFK中\n理由: {afk_data[uid]}"
            )

    # XP
    xp[user_id] = int(xp.get(user_id, 0)) + 1
    new_lv = calc_level(xp[user_id])

    if settings["level"]:
        if level.get(user_id, 0) < new_lv:
            level[user_id] = new_lv
            await message.channel.send(
                f"{message.author.mention} Lv{new_lv}になった！🎉"
            )
            save_data()

    # うお
    if "うお" in text and settings["uou"]:
        uou_count[user_id] = int(uou_count.get(user_id, 0)) + 1

        await message.channel.send(
            f"{message.author.mention} うお回数: {uou_count[user_id]}"
        )

        save_data()
        return

    # ランダム返信
    if settings["reply"]:
        for k, v in RESPONSES.items():
            if k in text:
                await message.channel.send(random.choice(v))
                return


# =========================
# 設定ON/OFF
# =========================
@tree.command(name="setting", description="機能ON/OFF")
async def setting(interaction: discord.Interaction, target: str, mode: str):

    settings = get_settings(str(interaction.user.id))

    if target not in ["level", "reply", "uou"]:
        await interaction.response.send_message(
            "level / reply / uou",
            ephemeral=True
        )
        return

    settings[target] = (mode == "on")
    save_data()

    await interaction.response.send_message(
        f"{target} → {mode}",
        ephemeral=True
    )


# =========================
# 設定確認
# =========================
@tree.command(name="mysetting", description="設定確認")
async def mysetting(interaction: discord.Interaction):

    settings = get_settings(str(interaction.user.id))

    text = "\n".join([
        f"{k}: {'ON' if v else 'OFF'}"
        for k, v in settings.items()
    ])

    await interaction.response.send_message(
        text,
        ephemeral=True
    )


# =========================
# レベル確認
# =========================
@tree.command(name="level", description="レベル確認")
async def level_cmd(interaction: discord.Interaction):

    uid = str(interaction.user.id)

    await interaction.response.send_message(
        f"Lv {level.get(uid, 0)}"
    )


# =========================
# うおランキング
# =========================
@tree.command(name="uou_rank", description="うおランキング")
async def uou_rank(interaction: discord.Interaction):

    sorted_users = sorted(
        uou_count.items(),
        key=lambda x: int(x[1]),
        reverse=True
    )

    text = ""

    for i, (uid, cnt) in enumerate(sorted_users[:5], 1):
        text += f"{i}位 <@{uid}> : {cnt}\n"

    await interaction.response.send_message(
        text or "まだデータなし"
    )


# =========================
# お知らせ設定
# =========================
@tree.command(name="set_announce_channel", description="お知らせチャンネル設定")
async def set_announce_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "管理者のみ",
            ephemeral=True
        )
        return

    guild_announce_channel[str(interaction.guild.id)] = channel.id
    save_data()

    await interaction.response.send_message(
        f"{channel.mention} に設定したよ",
        ephemeral=True
    )


# =========================
# お知らせ解除
# =========================
@tree.command(name="unset_announce_channel", description="お知らせ解除")
async def unset_announce_channel(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "管理者のみ",
            ephemeral=True
        )
        return

    gid = str(interaction.guild.id)

    if gid in guild_announce_channel:

        del guild_announce_channel[gid]
        save_data()

        await interaction.response.send_message(
            "解除したよ",
            ephemeral=True
        )

    else:
        await interaction.response.send_message(
            "未設定だよ",
            ephemeral=True
        )


# =========================
# 一斉お知らせ
# =========================
@tree.command(name="announce_all", description="全サーバー通知")
async def announce_all(
    interaction: discord.Interaction,
    message: str
):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "管理者のみ",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📣 お知らせ",
        description=message,
        color=0xff4444
    )

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

    await interaction.response.send_message(
        f"送信完了: {success}",
        ephemeral=True
    )


# =========================
# サイコロ
# =========================
@tree.command(name="dice", description="サイコロ")
async def dice(interaction: discord.Interaction):

    await interaction.response.send_message(
        str(random.randint(1, 6))
    )


# =========================
# AFK
# =========================
@tree.command(name="afk", description="AFK設定")
async def afk(
    interaction: discord.Interaction,
    reason: str = "離席中"
):

    uid = str(interaction.user.id)

    afk_data[uid] = reason
    save_data()

    await interaction.response.send_message(
        f"AFK設定したよ: {reason}"
    )


# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
