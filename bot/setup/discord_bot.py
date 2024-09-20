from discord.ext import commands
import discord


# Set up the Discord bot's intents and permissions
intents = discord.Intents.all()

# Initialize the bot client
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("/"),
    intents=intents,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
)
