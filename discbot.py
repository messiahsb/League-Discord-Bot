import requests
import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import random
import league

load_dotenv()
D_KEY = os.getenv("D_API")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

secret_role = "Leaguer"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="League of Legends"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="rammus")
async def rammus(interaction: discord.Interaction):
    await interaction.response.send_message("Okay 👍")


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say ?")
async def say(interaction: discord.Integration, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")


@bot.tree.command(name="change_status")
async def change_status(interaction: discord.Interaction):
    try:
        status:list[str] = ["Leg of Leggings", "Woog of Woggings", "Leech of Lemons", "Dota 2"] 
        await bot.change_presence(activity=discord.Game(name=(f"{random.choice(status)}")))
        await interaction.response.send_message("Status Changed", ephemeral=True)
    except Exception as e:
        print(e)


@bot.tree.command(name="sona")
async def rammus(interaction: discord.Interaction):
    await interaction.response.send_message("Only you can here me Summoner", ephemeral=True)

# @bot.tree.command(name="get_match_winner")
# async def get_match_winner(interaction: discord.Interaction):
#     y = league.get_match_data(league.get_match_history(league.get_puuid("Wold5182", "NA1"), "0", "1")[0])
#     print(y)
#     x = "win" if league.get_match_winner(y) else "lose"
#     print(x)
#     try:   
#         await interaction.response.send_message(f"{x}", ephemeral=True)
#     except Exception as e:
#         await interaction.response.send_message("could not get match data")


@bot.event
async def  on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "okay" in message.content.lower():
        await message.add_reaction("👍")

    await bot.process_commands(message)



# @bot.command()
# async def assign(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role:
#         await ctx.author.add_roles(role)
#         await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
#     else:
#         await ctx.send("Role Doesn't Exist")

# @bot.command()
# async def remove(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role:
#         await ctx.author.remove_roles(role)
#         await ctx.send(f"{ctx.author.mention} is no longer a {secret_role}")
#     else:
#         await ctx.send("Role Doesn't Exist")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have persmission to do that!")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)

    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

    
bot.run(D_KEY,log_handler=handler, log_level=logging.DEBUG)


