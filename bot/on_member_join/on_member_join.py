from bot.setup.init import client
from config import channels
from bot.scripts.message.forbidden import name_contains_profanity
from bot.db.fetch_data import fetch_roles
import random


@client.event
async def on_member_join(member):

    channel = client.get_channel(channels["welcome"])

    if await name_contains_profanity(member.name, member):
        return

    roles, role_names = await fetch_roles(channel.guild)

    visitor_role = next((r for r in roles if r.name == "Visitor"), None)

    await member.add_roles(visitor_role)

    outgoing_message = random.choice(
        [
            "welcome to Señor Rios' Neighborhood.",
            "welcome to the hood, yo.",
            "wilkommen aus Herr Rivers Neighborhood.",
            "top of the mornin' to ya.",
            "Hi!",
            "How’s it going?",
            "What’s happening?",
            "What’s the story?",
            "Yo!",
            "Hello!",
            "Hi there",
            "Good morning",
            "Good afternoon",
            "Good evening",
            "It’s nice to meet you",
            "Hey, Heya or Hey there!",
            "It’s a pleasure to meet you",
            "Morning!",
            "How are things?",
            "What’s new?",
            "It’s good to see you",
            "G’day!",
            "Howdy!",
            "What’s up?",
        ]
    )

    await channel.send(f"{member.name}, {outgoing_message}")

    """ Compose and send a DM to the new member with instructions and their snowflake id."""

    INSTRUCTIONS_LINK = "https://docs.google.com/document/d/1sn8xZ9pEMEAia9jHeaC_DEKVlgCxZ6WnuPiKuI8h_cU"
    channel = await member.create_dm()
    snowflake = member.id
    snowflake = str(snowflake)

    await channel.send(
        f"Thanks for joining my server. Please follow the instructions in this doc to get started: {INSTRUCTIONS_LINK}"
        + "\n\n"
        + f"And here is your discord snowflake id: {snowflake}. You're going to need it to continue.\n\nSee you in the hood."
    )
