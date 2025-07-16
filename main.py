import discord
import random
import time
import os
import json
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"The bot is logged as {bot.user}")

@bot.command()
@commands.cooldown(1, 7200, commands.BucketType.user)  # 1 kullanım, 7200 saniye (2 saat), kullanıcı bazında
async def dick(ctx, option: str = None):
    user_id = str(ctx.author.id)
    
    if os.path.exists("dicks.json"):
        with open("dicks.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    buyume_rakamlari = list(range(1,13))
    secilen_buyume = random.choice(buyume_rakamlari)
    boy = data.get(user_id, 0)

    if option == "grow":
        boy += secilen_buyume
        data[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"{ctx.author.mention}, ur dick is grew up {secilen_buyume}cm! : {boy} cm 🍆")


    if option == "howmanycm":
        await ctx.send(f"ur dick is {boy}cm {ctx.author.mention}-san1!1!!")
        return

    if option == "top":
        if not data:
            await ctx.send("there is no data")
            return

        sirali = sorted(data.items(), key=lambda x: x[1], reverse=True)

        mesaj = "**server top dick size:**\n"
        for i, (uid, boy) in enumerate(sirali, start=1):
            try:
                user = await ctx.guild.fetch_member(int(uid))
                isim = user.display_name
            except:
                isim = f"User ID: {uid}"

            mesaj += f"{i}. {isim} — {boy} cm\n"

        if len(mesaj) > 2000:
            mesaj = mesaj[:1990] + "\n...ve devamı var."

        await ctx.send(mesaj)
        return

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, you need to wait {round(error.retry_after)} seconds to use this command.")
    else:
        raise error  # Diğer hataları normal şekilde göster


bot.run("INSERT YOUR TOKEN HERE")