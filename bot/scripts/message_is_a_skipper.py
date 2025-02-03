from config import (
    members_to_skip,
    channels,
)


def message_is_a_skipper(message, channel):
    """
    Returns true if the message is from a member or channel that should be skipped. such as:
    carlbot,
    rivers_id,
    cuomputer_id,
    another_rivers_server_id,
    dyno_id,
    server_publish_message_id,
    fm_bot,
    """
    # print("message_is_a_skipper")
    # Skip if message is in a DM Channel
    try:
        channel.name
    except:
        return True

    member = message.author

    # print(member.id)
    # print(members_to_skip)
    # print(member.id in members_to_skip)

    # if member.name == "Rivers#6979":
    #     return True

    if (
        not hasattr(channel, "name")
        or channel.name == "moderator-only"
        or channel.id == channels["welcome"]
        or member.id in members_to_skip
        or channel.id == channels["dan"]
        or channel.id == channels["sarah"]
        or channel.id == channels["vangie"]
        or channel.id == channels["geezerville"]
    ):
        return True
