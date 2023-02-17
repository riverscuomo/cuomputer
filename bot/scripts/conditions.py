from config import (
    q_and_a_channels,
    testing,
    library_response_channels,
    coach_response_channels,
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


def meets_conditions_for_flirty_response(
    t,
    message,
    is_question,
    mentions_rivers,
    user_score
):
    # never_respond = 194  # t has to be higher
    # no_river = 196  # if no 'river', t has to be higher
    # no_question = 197  # if no '?', t has to be higher
    # always_respond = 100  # will always respond if t is higher

    if (
        # t > never_respond
        (is_question and mentions_rivers and t > 110)
        or ((is_question or mentions_rivers) and t > 195)
    ):
        return True


def meets_conditions_for_googlebot_response(
    author_name: str, channel: str, newbie: bool
):
    if channel == "ask-rivers":
        # print("meets_conditions_for_googlebot_response! because channel == ask-rivers")
        return True

    elif channel in q_and_a_channels and (newbie or testing):
        # print("meets_conditions_for_googlebot_response!")
        return True

    # elif channel in japanese_channels or spanish_channels:
    #     print("meets_conditions_for_googlebot_response!")
    #     return True

    # print(
    #     f"Doesn't meets_conditions_for_googlebot_response because '{channel}' not in {q_and_a_channels} or newbie={newbie}"
    # )
    return False


def meets_conditions_for_library_response(channel_name):
    return channel_name in library_response_channels


def meets_conditions_for_riverbot_response(channel_name):
    return channel_name in rivers_response_channels
