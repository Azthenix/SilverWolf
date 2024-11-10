import discord
import os # default module
from dotenv import load_dotenv
import requests
import json

users_path = "users.json"

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

#####################################################################################################
#####################################################################################################
#####################################################################################################

@bot.slash_command(name="reload", description="Reloads modules", guild_ids=[742405919249268767])
async def reload_modules(ctx):
    bot.reload_extension('redeem_for_all')
    bot.reload_extension('redeem')
    await ctx.respond("Reloaded all modules")

#####################################################################################################
#####################################################################################################
#####################################################################################################

bot.load_extension('redeem_for_all')
bot.load_extension('redeem')

bot.run(os.getenv('SilverWolf')) # run the bot with the token
