import requests
import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands


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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say ?")
async def say(interaction: discord.Integration, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")


@bot.event
async def  on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "bad word" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} -  dont use that word")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role Doesn't Exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer a {secret_role}")
    else:
        await ctx.send("Role Doesn't Exist")


@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have persmission to do that!")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)

    poll_message = await ctx.sendd(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

    
bot.run(D_KEY,log_handler=handler, log_level=logging.DEBUG)



