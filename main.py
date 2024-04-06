import os
import discord
import asyncio
from discord.ext import commands

# Initialize the Discord bot
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# Define paid scripts for different games
paid_scripts = {
    "blox fruits": ["Blox fruit jude script", "loadstring(script_for_blox_fruits)"],
    "doors": ["Script for Doors game", "loadstring(script_for_doors)"],
    # Add more games and their scripts as needed
}

# Owner information
owner_info = {
    "name": "name",
    "age": age,
    "location": "country",
}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Server"), status=discord.Status.online)
    print(f'Logged in as {bot.user.name}!')

@bot.command(name='paid')
async def paid_scripts(ctx, game=None, *, query=None):
    if game is None:
        await ctx.send(help_messages["paid"])
        return

    game = game.lower()
    if game not in paid_scripts:
        embed = discord.Embed(title="Error", description=help_messages["error_game_not_found"], color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if query is None:
        script_list = "\n".join(paid_scripts[game])
        embed = discord.Embed(title=f"Paid Scripts for {game}", description=script_list, color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        filtered_scripts = [script for script in paid_scripts[game] if query.lower() in script.lower()]
        if filtered_scripts:
            script_list = "\n".join(filtered_scripts)
            embed = discord.Embed(title=f"Matching Paid Scripts for {game} '{query}'", description=script_list, color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="No Matching Scripts", description=help_messages["no_matching_scripts"].format(game=game), color=discord.Color.red())
            await ctx.send(embed=embed)

@bot.command(name='bhelp')
async def bot_help(ctx):
    help_messages = {
        "paid": "To get a list of paid scripts for a specific game, use `?paid <game>` or `?paid <game> <query>` to filter by query.",
        "bhelp": "This is the help command. Use `?bhelp` to display this message.",
        "error_game_not_found": "Sorry, that game has not been added to this bot yet.",
        "no_matching_scripts": "No matching paid scripts found for {game}.",
        "add_game": "To add a new game and its scripts, use `?add_game <game_name> <script1> <script2> ...`",
        "owner_info": "To get information about the owner, use `?owner_info`.",
        "see_games": "To see available game commands, use `?see_games`."
    }

    # Send help message to the server
    embed = discord.Embed(title="Bot Help", description=help_messages["bhelp"], color=discord.Color.blue())
    embed.add_field(name="Command Usage", value="To see available paid scripts for a game: `?paid <game>`\nTo filter scripts by a query: `?paid <game> <query>`\nTo add a new game: `?add_game <game_name> <script1> <script2> ...`\nTo get owner information: `?owner_info`\nTo see available game commands: `?see_games`")
    await ctx.send(embed=embed)

    # Delayed DM sending after 5 seconds
    await asyncio.sleep(5)
    await ctx.author.send("Current games are: Blox fruits and Doors. Please check your direct messages.")
    await ctx.send(embed=discord.Embed(description="Please check your direct messages. Thank you for choosing us!", color=discord.Color.green()))

@bot.command(name='see_games')
async def see_games(ctx):
    embed = discord.Embed(title="Available Games", color=discord.Color.blue())
    for game, scripts in paid_scripts.items():
        script_list = "\n".join(scripts)
        embed.add_field(name=game.capitalize(), value=script_list, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "check dms pls":
        available_games = "\n".join(paid_scripts.keys())
        embed = discord.Embed(title="Available Games", description=available_games, color=discord.Color.blue())
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.command(name='add_game')
async def add_game(ctx, game_name, *scripts):
    game_name = game_name.lower()

    if game_name in paid_scripts:
        await ctx.send(f"Game '{game_name}' already exists.")
        return

    paid_scripts[game_name] = list(scripts)
    await ctx.send(f"Game '{game_name}' and its scripts have been added successfully.")

@bot.command(name='owner_info')
async def owner_info_command(ctx):
    embed = discord.Embed(title="Owner Information", color=discord.Color.gold())
    embed.add_field(name="Name", value=owner_info["name"], inline=False)
    embed.add_field(name="Age", value=owner_info["age"], inline=False)
    embed.add_field(name="Location", value=owner_info["location"], inline=False)
    await ctx.send(embed=embed)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
