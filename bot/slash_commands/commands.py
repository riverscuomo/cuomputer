import asyncio
import contextlib
import discord
from bot.on_message.bots.openai_bot import DEFAULT_MESSAGE_LOOKBACK_COUNT, PromptParams
from config import GUILD_ID, rivers_id
from bot.setup.discord_bot import client
from bot.setup.bots import weezerpedia_api, openai_bot # riverpedia_api,

print('commands.py')

SUMMARIZE_SYSTEM_PROMPT = "You are the person responsible for summarizing server messages in a succinct and effective way for the server owner and supporters. Always report the number of messages found."
SUMMARIZE_USER_PROMPT = "[INTERNAL] Summarize these recent messages in channel history if theres at least one message. Close by reporting the number of messages found."
ADVISE_SYSTEM_PROMPT = "You are Rivers Cuomo's personal advisor who is very capable and results oriented."
ADVISE_USER_PROMPT = "[INTERNAL] Rivers Cuomo runs this Discord server. Given there is at least one message in this channel, then based on these recent messages, how would you advise him?"


def is_supporter():
    async def predicate(interaction: discord.Interaction) -> bool:
        return "Supporter" in [role.name for role in interaction.user.roles] or interaction.user.id == rivers_id
    return discord.app_commands.check(predicate)


def is_rivers():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == rivers_id
    return discord.app_commands.check(predicate)


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
# @is_supporter()
async def summarize(interaction: discord.Interaction, count: int = DEFAULT_MESSAGE_LOOKBACK_COUNT):
    await interaction.response.send_message("Processing...", ephemeral=True)
    prompt_params = PromptParams(
        system_prompt=SUMMARIZE_SYSTEM_PROMPT,
        user_prompt=SUMMARIZE_USER_PROMPT,
        user_name=interaction.user.global_name,
        channel_id=interaction.channel_id,
        attachment_urls=[])
    response = openai_bot.fetch_openai_completion(prompt_params, count).strip()
    channel = interaction.channel
    with contextlib.suppress(Exception):
        await channel.send(f"**Summary of last {count} messages:**\n{response}")


@client.tree.command(name="summarize_and_advise", description="Summarize the last N messages in a given channel, and advise on what to do")
# @is_rivers()
async def summarize_and_advise(interaction: discord.Interaction, count: int = DEFAULT_MESSAGE_LOOKBACK_COUNT):
    await interaction.response.send_message("Processing...", ephemeral=True)
    prompt_params = PromptParams(system_prompt=SUMMARIZE_SYSTEM_PROMPT,
                                 user_prompt=SUMMARIZE_USER_PROMPT,
                                 user_name=interaction.user.global_name,
                                 channel_id=interaction.channel_id,
                                 attachment_urls=[])
    response = openai_bot.fetch_openai_completion(prompt_params, count).strip()

    # Get the channel to send messages to
    channel = interaction.channel
    with contextlib.suppress(Exception):
        await channel.send(f"**Summary of last {count} messages:**\n{response}")

    prompt_params = PromptParams(system_prompt=ADVISE_SYSTEM_PROMPT,
                                 user_prompt=ADVISE_USER_PROMPT,
                                 user_name=interaction.user.global_name,
                                 channel_id=interaction.channel_id,
                                 attachment_urls=[])
    response = openai_bot.fetch_openai_completion(prompt_params,
                                                  count).strip()
    with contextlib.suppress(Exception):
        await channel.send(f"**Summary of last {count} messages:**\n{response}")


@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CheckFailure):
        await interaction.response.send_message("This command is reserved for specified roles or users.", ephemeral=True)
    else:
        await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)
