from config import channels

async def delete_based_images_in_general(message, member_roles,now):
    """Don't let Based post images in general """
    print("delete_based_images_in_general")
    # print(now.hour)
    # print(22 > now.hour > 18)
    # print(message.attachments)
    # print("Based" in member_roles)
    if (
        message.channel.id == channels["general"]
        # and len(message.content) > 2
        and message.attachments != []
        and "Based" in member_roles
        and 22 > now.hour > 18
    ):
        # print(message.attachments)
        response = "Try posting images in Based."
        # print(response)
        channel = await message.author.create_dm()
        await message.delete()
        await channel.send(
            response
            + "\n\n"
            + message.content
        )
        
        
async def reject_artist_text_in_gallery(message, member_roles):
    """Don't let Artists posts text messages in the gallery"""
    if (
        message.channel.name == "gallery"
        # and len(message.content) > 2
        and message.attachments == []
        and "Artist" in member_roles
    ):
        # print(message.attachments)
        print("Artists are not allowed to send text messages the gallery.")
        channel = await message.author.create_dm()
        await message.delete()
        await channel.send(
            "Artists are not allowed to send text messages the gallery."
            + "\n\n"
            + message.content
        )


async def reject_in_focus_channel(message, member_roles):
    """ """
    if message.channel.name == "focus":
        content = message.content
        if len(content) > 80 or " and " in content or "," in content or "/" in content:
            channel = await message.author.create_dm()
            await message.delete()
            await channel.send(
                "Please just pick the one most important thing to focus on."
                + "\n\n"
                + message.content
            )
