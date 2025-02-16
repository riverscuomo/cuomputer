from config import channels


async def assert_old_users_have_connected(
    message, member, firestore_user
):
    """ If they're not connected to RC.COM (no firestore user) and they're not in the connect channel, 
    delete their message and DM them to connect.
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
            """It looks like your discord account is not connected to your riverscuomo.com account. 
           The easiest way to fix this is to follow the instructions in the #connect-to-mrn channel description or in this doc https://docs.google.com/document/d/1sn8xZ9pEMEAia9jHeaC_DEKVlgCxZ6WnuPiKuI8h_cU. 
          """
        )
        return False
    return True
