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
# データ
# =========================
custom_responses = {}
memos = {}
xp = {}
level = {}
uou_count = {}
user_settings = {}

def get_level(x):
    return int(x ** 0.5)

def get_settings(user_id):
    if user_id not in user_settings:
        user_settings[user_id] = {
            "level": True,
            "reply": True,
            "uou": True
        }
    return user_settings[user_id]

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
    user_id = message.author.id
    settings = get_settings(user_id)

    # XP
    xp[user_id] = xp.get(user_id, 0) + 1
    new_level = get_level(xp[user_id])

    if settings["level"]:
        if user_id not in level or new_level > level[user_id]:
            level[user_id] = new_level
            await message.channel.send(f"{message.author.mention} レベル{new_level}になった！🎉")
    else:
        level[user_id] = new_level

    # うお
    if "うお" in text and settings["uou"]:
        uou_count[user_id] = uou_count.get(user_id, 0) + 1
        count = uou_count[user_id]

        msg = f"{message.author.mention} が「うお」を言った！\n回数: {count}回"

        if count % 10 == 0:
            msg += f"\n🎉 {count}回達成！"

        await message.channel.send(msg)
        return

    # カスタム返信
    if settings["reply"]:
        for key, value in custom_responses.items():
            if key in text:
                await message.channel.send(value)
                return

    # ランダム返信
    if settings["reply"]:
        for key in RESPONSES:
            if key in text:
                await message.channel.send(random.choice(RESPONSES[key]))
                return

# =========================
# コマンド
# =========================

@tree.command(name="help", description="コマンド一覧")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="📖 コマンド一覧", color=0x00ffcc)

    embed.add_field(name="🎮 遊び", value="/dice\n/uou_rank\n/level", inline=False)
    embed.add_field(name="🧠 便利", value="/memo\n/mymemo\n/remind\n/learn", inline=False)
    embed.add_field(name="⚙️ 設定", value="/setting\n/mysetting\n/status", inline=False)
    embed.add_field(name="🛠 管理", value="/announce\n/clear\n/serverinfo", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================
# ステータス変更
# =========================
@tree.command(name="status", description="Botのステータス変更（管理者）")
async def status(interaction: discord.Interaction, type: str, text: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者のみ", ephemeral=True)
        return

    if type == "play":
        activity = discord.Game(name=text)

    elif type == "listen":
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)

    elif type == "watch":
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)

    elif type == "stream":
        activity = discord.Streaming(name=text, url="https://twitch.tv/discord")

    else:
        await interaction.response.send_message("play / listen / watch / stream", ephemeral=True)
        return

    await bot.change_presence(activity=activity)
    await interaction.response.send_message(f"変更: {text}")

# =========================
# 設定
# =========================
@tree.command(name="setting", description="機能ON/OFF")
async def setting(interaction: discord.Interaction, target: str, mode: str):

    settings = get_settings(interaction.user.id)

    if target not in ["level", "reply", "uou"]:
        await interaction.response.send_message("level / reply / uou", ephemeral=True)
        return

    if mode not in ["on", "off"]:
        await interaction.response.send_message("on / off", ephemeral=True)
        return

    settings[target] = (mode == "on")
    await interaction.response.send_message(f"{target} → {mode}", ephemeral=True)

@tree.command(name="mysetting", description="設定確認")
async def mysetting(interaction: discord.Interaction):

    settings = get_settings(interaction.user.id)

    text = ""
    for k, v in settings.items():
        text += f"{k}: {'ON' if v else 'OFF'}\n"

    await interaction.response.send_message(text, ephemeral=True)

# =========================
# 管理
# =========================
@tree.command(name="clear", description="メッセージ削除")
async def clear(interaction: discord.Interaction, amount: int):

    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("権限なし", ephemeral=True)
        return

    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message("削除した", ephemeral=True)

@tree.command(name="announce", description="お知らせ")
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者のみ", ephemeral=True)
        return

    embed = discord.Embed(title="📣 お知らせ", description=message)
    await channel.send(embed=embed)

    await interaction.response.send_message("送信した", ephemeral=True)

@tree.command(name="serverinfo", description="サーバー情報")
async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    await interaction.response.send_message(
        f"名前: {guild.name}\n人数: {guild.member_count}"
    )

# =========================
# 便利系
# =========================
@tree.command(name="memo", description="メモ保存")
async def memo(interaction: discord.Interaction, text: str):
    memos[interaction.user.id] = text
    await interaction.response.send_message("保存した")

@tree.command(name="mymemo", description="メモ確認")
async def mymemo(interaction: discord.Interaction):
    await interaction.response.send_message(memos.get(interaction.user.id, "なし"))

@tree.command(name="remind", description="リマインド")
async def remind(interaction: discord.Interaction, sec: int, msg: str):
    await interaction.response.send_message("OK")
    await asyncio.sleep(sec)
    await interaction.followup.send(msg)

# =========================
# 遊び
# =========================
@tree.command(name="dice", description="サイコロ")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(str(random.randint(1,6)))

@tree.command(name="level", description="レベル確認")
async def level_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(f"Lv {level.get(interaction.user.id, 0)}")

@tree.command(name="uou_rank", description="うおランキング")
async def uou_rank(interaction: discord.Interaction):

    if not uou_count:
        await interaction.response.send_message("まだない")
        return

    sorted_users = sorted(uou_count.items(), key=lambda x: x[1], reverse=True)

    text = ""
    for i, (uid, cnt) in enumerate(sorted_users[:5], 1):
        text += f"{i}位 <@{uid}> : {cnt}\n"

    await interaction.response.send_message(text)

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
