import discord
import statlookup as stat
from discord.ext import commands
import asyncio
import json
import os


# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	guildid = data["guildid"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]


class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
intents.guild_messages = True
intents.message_content = True
intents.messages = True
# The bot and client
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)
# The connected servers
guild = bot.get_all_members()

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")
	
@bot.command()
async def owhelp(ctx):
	embed = discord.Embed(title = "Bot Help", description= "Some useful commands:", color=discord.Colour.from_rgb(249,158,26))
	embed.add_field(name='/stats BattleNetID-Num', value='Ensure you replace the \'#\' with \'-\'')
	await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def stats(ctx, message):
	async with ctx.typing():
		user = stat.player(message)
		if user.exists and not user.private:
			embed = discord.Embed(title = "Overwatch Stats", description= f'Healing (avg/10 mins): {user.healing} \
				\nDamage (avg/10 mins): {user.damage} \nWin Rate (%): {user.wins}', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = "Good stuff gamer")
		elif user.exists and user.private:
			embed = discord.Embed(title = "Overwatch Stats", description= f'User {message} is private!', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = f'[Set your profile visibility to \'Public\' to display your stats]')
		else:
			embed = discord.Embed(title = "Overwatch Stats", description= f'User {message} does not exist.', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = "Please ensure you enter your exact BattleID with format \"Name-Number\"")
		await asyncio.sleep(1)
	await ctx.reply(embed=embed, mention_author=False)
	
@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}your stanky overwatch games"))

bot.run(token)