@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("先に通話入って！")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send("通話入った！")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("抜けた！")

@bot.event
async def on_command_error(ctx, error):
    print("エラー内容:", error)

@bot.command()
async def test(ctx):
    await ctx.send("動いてる！")
