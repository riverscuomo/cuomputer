import asyncio
import contextlib
import discord
from bot.on_message.bots.openai_bot import DEFAULT_MESSAGE_LOOKBACK_COUNT
from config import GUILD_ID, rivers_id
from bot.setup.discord_bot import client
from bot.setup.bots import weezerpedia_api, riverpedia_api, openai_bot

print('commands.py')

SUMMARY_MESSAGE = "Summarize these recent messages in channel history, do not give any additional advice"
SUMMARY_SYSTEM_PROMPT = "You are the person responsible for summarizing server messages in a succinct and effective way for the server owner and supporters. You do not provide any additional information beyond a good summary."

@client.tree.command(name="weezerpedia", description="Query Weezerpedia API")
async def weezerpedia(interaction: discord.Interaction, search_term: str):
    # Your function to query the Weezerpedia API
    await interaction.response.defer()
    result, img_file = weezerpedia_api.get_search_result_knowledge(search_term)
    if result is None:
        await interaction.followup.send("No results found.")
    else:
        await interaction.followup.send(result, files=[] if img_file is None else [img_file], suppress_embeds=True)


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


@client.tree.command(name="summarize", description="Summarize the last N messages in a given channel")
async def summarize(interaction: discord.Interaction, count: int = DEFAULT_MESSAGE_LOOKBACK_COUNT):
    await interaction.response.defer()
    member_roles = [role.name for role in interaction.member.roles]
    if "Supporter" in interaction.user.roles:
        response = openai_bot.build_ai_response(SUMMARY_MESSAGE,
                                                SUMMARY_SYSTEM_PROMPT,
                                                None,
                                                count)
        with contextlib.suppress(Exception):
            await interaction.user.send(response)


@client.tree.command(name="summarize_and_advise", description="Summarize the last N msesages in a given channel, and advise Rivers on what to do")
async def summarize_and_advise(interaction: discord.Interaction, count: int = DEFAULT_MESSAGE_LOOKBACK_COUNT):
    await interaction.response.defer()
    if interaction.member.user.id == rivers_id:
        response = openai_bot.build_ai_response(SUMMARY_MESSAGE,
                                                SUMMARY_SYSTEM_PROMPT,
                                                None,
                                                count)
        await interaction.user.send(response)
        response = openai_bot.build_ai_response("Based on these recent messages in channel chat history, how would you advise Rivers Cuomo in some following ways: 1) technical improvements of the server, 2) community engagement of the server, or 3) any feedback on Rivers' music",
                                                "You are Rivers Cuomo's personal advisor who is very capable and results oriented.",
                                                None,
                                                count)
        with contextlib.suppress(Exception):
            await interaction.user.send(response)