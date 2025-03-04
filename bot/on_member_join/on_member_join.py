from bot.setup.discord_bot import client
from config import channels
from bot.scripts.message.forbidden import name_contains_profanity
from bot.db.fetch_data import fetch_roles
import random


@client.event
async def on_member_join(member):
    """
    Handles new members joining the Discord server.
    
    This function is triggered when a user joins the server. It performs several important tasks:
    
    1. Discord-Weezify Connection Flow (Step 1):
       - Assigns the "Visitor" role to new members
       - Sends a welcome message in the welcome channel
       - DMs the user with instructions and their Discord snowflake ID
    
    The Discord snowflake ID is critical for users to connect their Discord account to Weezify.
    Users will need this ID to enter on their Weezify profile at https://www.weezify.web.app.
    
    Connection Process Overview:
    1. THIS FUNCTION: User joins server, gets DM with snowflake ID
    2. User enters snowflake ID on Weezify profile page
    3. User goes to #connect-to-mrn channel and types their Weezify username
    4. Bot confirms connection (handled by connect_to_mrn function)
    
    Known Issues:
    - Users with restrictive DM privacy settings won't receive the welcome DM
      Solution: They need to temporarily enable "Allow direct messages from server members"
      or get their snowflake ID through other means
    
    Parameters:
    member (Member): The Discord member object representing the user who joined
    
    Returns:
    None
    """

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
            "How's it going?",
            "What's happening?",
            "What's the story?",
            "Yo!",
            "Hello!",
            "Hi there",
            "Good morning",
            "Good afternoon",
            "Good evening",
            "It's nice to meet you",
            "Hey, Heya or Hey there!",
            "It's a pleasure to meet you",
            "Morning!",
            "How are things?",
            "What's new?",
            "It's good to see you",
            "G'day!",
            "Howdy!",
            "What's up?",
        ]
    )

    await channel.send(f"{member.name}, {outgoing_message}")

    """ Compose and send a DM to the new member with instructions and their snowflake id."""

    INSTRUCTIONS_LINK = "https://docs.google.com/document/d/1sn8xZ9pEMEAia9jHeaC_DEKVlgCxZ6WnuPiKuI8h_cU"
    channel = await member.create_dm()
    snowflake = member.id
    snowflake = str(snowflake)

    await channel.send(
        f"Thanks for joining my server. To get started, please:\n\n"
        + f"1. Create an account at https://www.weezify.web.app if you don't already have one\n"
        + f"2. Go to your profile screen on Weezify\n" 
        + f"3. Enter your discord snowflake id: {snowflake}\n"
        + f"4. Come to the #connect-to-mrn channel in the Discord server\n"
        + f"5. Type your Weezify username (case-sensitive)\n\n"
        + f"For more detailed instructions: {INSTRUCTIONS_LINK}\n\n"
        + f"See you in the hood!"
    )
