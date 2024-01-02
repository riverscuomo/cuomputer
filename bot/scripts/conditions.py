from config import (
    library_response_channels,

    rivers_response_channels,
    standard_reponse_channels,
    always_respond_channels,
    members_to_skip,
    never_respond,
    threshold_for_non_questions,
    threshold_for_not_mentioning_rivers,
)


def meets_conditions_for_standard_response(t, message, newbie):
    """
    if message.channel.name in always_respond_channels [coach_cuomo]
    if message.channel.name in standard_reponse_channels [general + foreign]
    """

    if message.channel.name in always_respond_channels:
        return True

    if message.channel.name in standard_reponse_channels and (
        t > never_respond
        and ("?" in message.content or t > threshold_for_non_questions or newbie)
        and (
            "river" in message.content
            or t > threshold_for_not_mentioning_rivers
            or newbie
        )
        and message.author.id not in members_to_skip
    ):
        return True


def meets_conditions_for_oldbot_response(channel_name):
    if channel_name in ["coach-cuomo", "general"]:
        return True


def meets_conditions_for_library_response(channel_name):
    return channel_name in library_response_channels


def meets_conditions_for_riverbot_response(channel_name):
    return channel_name in rivers_response_channels
