import discord
import random
import time
import os
import sys
import json
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

if os.path.exists("cooldowns.json"):
    with open("cooldowns.json", "r") as f:
        try:
            cooldowns = json.load(f)
        except json.JSONDecodeError:
            cooldowns = {}
else:
    cooldowns = {}


@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")

@bot.command()
@commands.is_owner()
async def reload(ctx):
    await ctx.send("🔁 reloading...")
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, miktar):
    sil = await ctx.channel.purge(limit=int(miktar))


@bot.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(f"pong! {latency}ms")


@bot.command()
async def dick(ctx, option: str = None):
    user_id = str(ctx.author.id)

    # Dosyadan veriyi oku, yoksa boş dict yap
    if os.path.exists("dicks.json"):
        with open("dicks.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Eğer option parametresi yoksa uyar
    if option is None:
        await ctx.send("these are the only options that you can use: grow / howmanycm / top")
        return

    # cooldown sadece 'buyut' seçeneğinde geçerli
    if option == "grow":
        now = time.time()
        cooldown_time = 7200  # 2 saat = 7200 saniye
        last_time = cooldowns.get(user_id, 0)

        if now - last_time < cooldown_time:
            kalan = int(cooldown_time - (now - last_time))
            saat = int(kalan/3600)
            dakika = int((kalan%3600) / 60)
            user = ctx.author.mention
            
            if saat >= 1:
                await ctx.send(f"{user}, you can grow your dick after {saat} hours {dakika} minutes")
                return

            if saat == 0:
                await ctx.send(f"{user}, you can grow your dick after {dakika} minutes")
                return

        else:
            cooldowns[user_id] = now
            with open("cooldowns.json", "w") as f:
                json.dump(cooldowns, f, indent=4)


        buyume_rakamlari = list(range(1, 13))
        secilen_buyume = random.choice(buyume_rakamlari)
        boy = data.get(user_id, 0)
        boy += secilen_buyume
        data[user_id] = boy

        with open("dicks.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(
            f"{ctx.author.mention}, your dick is grew up {secilen_buyume}cm, now its: {boy}cm!"
        )
        return

    # cooldown yok, diğer seçenekler:
    if option == "howmanycm":
        boy = data.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, your dick is {boy} cm!")
        return

    if option == "top":
        if not data:
            await ctx.send("no one has a dick lmao lol ts pmo mdr")
            return

        sirali = sorted(data.items(), key=lambda x: x[1], reverse=True)

        mesaj = "**leaderboard of dicks:**\n"
        for i, (uid, boy) in enumerate(sirali, start=1):
            try:
                user = await ctx.guild.fetch_member(int(uid))
                isim = user.display_name if user else f"User ID: {uid}"
            except:
                isim = f"User ID: {uid}"

            mesaj += f"{i}. {isim} — {boy} cm\n"

            if len(mesaj) > 1900:
                mesaj += "\n...ve devamı var."
                break

        await ctx.send(mesaj)
        return

    # Bilinmeyen seçenek
    await ctx.send(
        "these are the only options that you can use: grow / howmanycm / top"
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, you should wait {round(error.retry_after)/60} to use this command"
        )
    else:
        raise error  # Diğer hataları normal şekilde göster

bot.run("INSERT YOUR TOKEN HERE")
