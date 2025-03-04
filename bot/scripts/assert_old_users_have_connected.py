from config import channels


async def assert_old_users_have_connected(
    message, member, firestore_user
):
    """ 
    Ensures existing users have connected their Discord account to Weezify.
    
    This function is part of the Discord-Weezify connection workflow:
    1. on_member_join: Sends the initial DM with snowflake ID to new members
    2. connect_to_mrn: Processes connection attempts in the connect channel
    3. THIS FUNCTION: Checks if users posting messages have connected their accounts
    
    When a user posts a message outside the #connect-to-mrn channel and doesn't have 
    a linked Weezify account, this function:
    1. Deletes their message
    2. Sends them a DM reminding them to connect their accounts
    3. Returns False to indicate the user needs to connect
    
    This function helps ensure all active users complete the connection process.
    
    Known Issues:
    - May fail to send DMs to users with restrictive privacy settings (403 Forbidden error)
    - Some connected users may be falsely flagged due to cached Firestore data
    
    Parameters:
    message (Message): The Discord message object that triggered this check
    member (Member): The Discord member who sent the message
    firestore_user (dict): The user's Firestore data, or None if not connected
    
    Returns:
    bool: True if user is connected or in connect channel, False if they need to connect
    """
    # """# This block will be used less and less."""
    if (
        # "Neighbor" in member_roles
        # and not
        firestore_user is None
        and message.channel.id != channels["connect"]
    ):
        # if member.id in [rivers_id, fm_bot, cuomputer_id]:
        #     print("not dming {member.id}")
        #     return
        print(
            f"NO FIRESTORE USER FOR {member} SO DELETING THEIR MESSAGE AND DMING THEM TO CONNECT."
        )
        channel = await member.create_dm()
        await message.delete()
        await channel.send(
            """It looks like your discord account is not connected to your Weezify account. 
           The easiest way to fix this is to follow the instructions in the #connect-to-mrn channel in the WELCOME section or in this doc https://docs.google.com/document/d/1sn8xZ9pEMEAia9jHeaC_DEKVlgCxZ6WnuPiKuI8h_cU. 
          """
        )
        return False
    return True
