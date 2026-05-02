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
# ランダム返信
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
    user_id = message.author.id

    # XP
    xp[user_id] = xp.get(user_id, 0) + 1
    new_level = get_level(xp[user_id])

    if user_id not in level or new_level > level[user_id]:
        level[user_id] = new_level
        await message.channel.send(f"{message.author.mention} レベル{new_level}になった！🎉")

    # うおカウント
    if "うお" in text:
        uou_count[user_id] = uou_count.get(user_id, 0) + 1
        count = uou_count[user_id]

        msg = f"{message.author.mention} が「うお」を言った！\n回数: {count}回"

        if count % 10 == 0:
            msg += f"\n🎉 {count}回達成！"

        await message.channel.send(msg)
        return

    # カスタム返信
    for key, value in custom_responses.items():
        if key in text:
            await message.channel.send(value)
            return

    # ランダム返信
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
# コマンド
# =========================

@tree.command(name="help", description="コマンド一覧を見る")
async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(title="📖 コマンド一覧", color=0x00ffcc)

    embed.add_field(name="🎮 遊び系", value="""
/dice - サイコロ
/uou_rank - うおランキング
/level - レベル確認
""", inline=False)

    embed.add_field(name="🧠 便利系", value="""
/memo - メモ保存
/mymemo - メモ確認
/remind - リマインダー
/learn - 言葉を覚える
""", inline=False)

    embed.add_field(name="🛠 管理系", value="""
/announce - お知らせ
/clear - メッセージ削除
/serverinfo - サーバー情報
""", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================
# サーバー情報
# =========================
@tree.command(name="serverinfo", description="サーバー情報を見る")
async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(title="📊 サーバー情報", color=0x3399ff)
    embed.add_field(name="名前", value=guild.name)
    embed.add_field(name="人数", value=guild.member_count)
    embed.add_field(name="作成日", value=guild.created_at.strftime("%Y/%m/%d"))

    await interaction.response.send_message(embed=embed)

# =========================
# メッセージ削除
# =========================
@tree.command(name="clear", description="メッセージを削除")
async def clear(interaction: discord.Interaction, amount: int):

    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("権限ない", ephemeral=True)
        return

    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{amount}件削除した", ephemeral=True)

# =========================
# 既存コマンド
# =========================

@tree.command(name="learn", description="言葉を覚えさせる")
async def learn(interaction: discord.Interaction, word: str, reply: str):
    custom_responses[word] = reply
    await interaction.response.send_message(f"{word} を覚えた！")

@tree.command(name="remind", description="指定秒後に通知する")
async def remind(interaction: discord.Interaction, sec: int, msg: str):
    await interaction.response.send_message(f"{sec}秒後に通知するよ！")
    await asyncio.sleep(sec)
    await interaction.followup.send(msg)

@tree.command(name="dice", description="サイコロを振る")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 {random.randint(1,6)}")

@tree.command(name="memo", description="メモを保存する")
async def memo(interaction: discord.Interaction, text: str):
    memos[interaction.user.id] = text
    await interaction.response.send_message("保存した！")

@tree.command(name="mymemo", description="自分のメモを見る")
async def mymemo(interaction: discord.Interaction):
    text = memos.get(interaction.user.id, "メモないよ")
    await interaction.response.send_message(text)

@tree.command(name="level", description="自分のレベルを見る")
async def level_cmd(interaction: discord.Interaction):
    lv = level.get(interaction.user.id, 0)
    await interaction.response.send_message(f"あなたのレベル: {lv}")

@tree.command(name="uou_rank", description="うおの回数ランキングを見る")
async def uou_rank(interaction: discord.Interaction):

    if not uou_count:
        await interaction.response.send_message("まだ誰も言ってない")
        return

    sorted_users = sorted(uou_count.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 うおランキング\n"
    for i, (uid, cnt) in enumerate(sorted_users[:5], 1):
        text += f"{i}位 <@{uid}> : {cnt}回\n"

    await interaction.response.send_message(text)

@tree.command(name="announce", description="お知らせを送信（管理者）")
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("管理者だけ", ephemeral=True)
        return

    embed = discord.Embed(title="📣 お知らせ", description=message, color=0xff5555)
    await channel.send(embed=embed)

    await interaction.response.send_message("送信した", ephemeral=True)

@tree.command(name="test", description="動作確認")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("動いてる！")

# =========================
# 起動
# =========================
bot.run(os.getenv("TOKEN"))
