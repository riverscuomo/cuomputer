import discord
import asyncio
from config import GUILD_ID
from bot.setup.discord_bot import client
from bot.setup.bots import weezerpedia_api, riverpedia_api

print('commands.py')


@client.tree.command(name="weezerpedia", description="Query Weezerpedia API")
async def weezerpedia(interaction: discord.Interaction, search_term: str):
    # Your function to query the Weezerpedia API
    result = weezerpedia_api.get_search_result_knowledge(search_term)
    await interaction.response.send_message(result)


@client.tree.command(name="riverpedia", description="Query Riverpedia API")
async def riverpedia(interaction: discord.Interaction, search_term: str):
    # Your function to query Riverpedia API
    result = riverpedia_api.get_wiki_response(search_term)
    await interaction.response.send_message(result)


@client.tree.command(name="servertime", description="Get the number of days since you joined the server")
async def servertime(interaction: discord.Interaction):
    today = discord.utils.utcnow()
    age = today - interaction.user.joined_at
    joined = max(age.days, 0)
    await interaction.response.send_message(
        f"{interaction.user.name}, you joined my server {joined} days ago."
    )
