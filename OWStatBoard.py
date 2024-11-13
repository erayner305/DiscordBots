import discord
from discord.ext import commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import statlookup as stat

import asyncio
import json
import os
from datetime import datetime, timedelta, timezone

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	guildid = data["guildid"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

# Get firebase database
cred = credentials.Certificate("firebase_configuration.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

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
	embed.add_field(name='/stats BattleNetID#Num', value='Ensure you include your ID and Number! \nYour profile must be set to public for us to find your stats.')
	await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def stats(ctx, message):
	async with ctx.typing():
		doc_ref = db.collection('user_stats').document(message)
		doc = doc_ref.get()

		if doc.exists:
			data = doc.to_dict()
			last_updated = data.get("timestamp")
			if last_updated and datetime.now(timezone.utc) - last_updated < timedelta(hours=1):
				embed = discord.Embed(
					title="Overwatch Stats",
					description=f"Healing (avg/10 mins): {data['healing']} \nDamage (avg/10 mins): {data['damage']} \nWin Rate (%): {data['wins']}", 
					color=discord.Colour.from_rgb(249,158,26)
				)
				await ctx.reply(embed=embed, mention_author=False)
				return

		user = stat.player(message)
		if user.exists and not user.private:
			# Save data to firestore
			doc_ref.set({
				'healing': user.healing,
				'damage': user.damage,
				'wins': user.wins,
				'timestamp': datetime.now(timezone.utc)
			})

			embed = discord.Embed(title = "Overwatch Stats", description= f'Healing (avg/10 mins): {user.healing} \
				\nDamage (avg/10 mins): {user.damage} \nWin Rate (%): {user.wins}', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = "Good stuff gamer")
		elif user.exists and user.private:
			embed = discord.Embed(title = "Overwatch Stats", description= f'User {message} is private!', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = f'[Set your profile visibility to \'Public\' to display your stats]')
		else:
			embed = discord.Embed(title = "Overwatch Stats", description= f'User {message} does not exist.', color=discord.Colour.from_rgb(249,158,26))
			embed.set_footer(text = "Please ensure you enter your exact BattleID with format \"Name#Number\"")
		await asyncio.sleep(1)
	await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def damage(ctx):
    users_ref = db.collection('user_stats')
    # Get all users sorted by damage in descending order
    users = users_ref.order_by("damage", direction=firestore.Query.DESCENDING).limit(10).stream()

    embed = discord.Embed(title="Damage Leaderboard", color=discord.Colour.from_rgb(249,158,26))
    for i, user in enumerate(users, start=1):
        data = user.to_dict()
        embed.add_field(name=f"{i}. {user.id}", value=f"Damage (avg/10 mins): {data['damage']}", inline=False)

    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def healing(ctx):
    users_ref = db.collection('user_stats')
    # Get all users sorted by healing in descending order
    users = users_ref.order_by("healing", direction=firestore.Query.DESCENDING).limit(10).stream()

    embed = discord.Embed(title="Healing Leaderboard", color=discord.Colour.from_rgb(249,158,26))
    for i, user in enumerate(users, start=1):
        data = user.to_dict()
        embed.add_field(name=f"{i}. {user.id}", value=f"Healing (avg/10 mins): {data['healing']}", inline=False)

    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def winrate(ctx):
    users_ref = db.collection('user_stats')
    # Get all users sorted by win rate in descending order
    users = users_ref.order_by("wins", direction=firestore.Query.DESCENDING).limit(10).stream()

    embed = discord.Embed(title="Win rate Leaderboard", color=discord.Colour.from_rgb(249,158,26))
    for i, user in enumerate(users, start=1):
        data = user.to_dict()
        embed.add_field(name=f"{i}. {user.id}", value=f"Win rate: {data['wins']}", inline=False)

    await ctx.reply(embed=embed, mention_author=False)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}your stanky overwatch games"))

bot.run(token)