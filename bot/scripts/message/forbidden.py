import discord
from bot.on_message.classes.message import CustomMessage
from bot.setup.services.demoji_setup import demoji
from config import channels, rivers_id, cuomputer_id
from bot.scripts.message.sentiment import get_polarity
from data.lists import strings_to_delete  # , forbidden_words
from better_profanity import profanity

import re
import sys

sys.path.append("...")  # Adds higher directory to python modules path.


profanity.add_censor_words(
    ["cock", "arse", "whore",
     #  "lesbian",
     #  "slept with",
     #  "sleep with"
     ]
)


class Forbidden:
    def __init__(self, is_forbidden, reason):
        self.is_forbidden = is_forbidden
        self.reason = reason


def forbidden_message(message: discord.Message, role_names: list):
    """ punctuation and emoji http """

    based_role_in_based_channel = (
        message.channel.id == channels["based"] and "Based" in role_names)

    # # print(channel)
    # if channel_name == "questions-and-help":
    #     # await post_newbie_help(author_name, message)
    #     # print("asldkfjasdlkfj")
    #     if not message.endswith(".") and not message.endswith("?"):
    #         return Forbidden(is_forbidden=True, reason=
    #         )
    # if content.contains("!"):
    #     # print("alskdjf")
    #     await message.channel.send(
    #         "Please don't use '!'. I like it when you're calm."
    #     )

    if (
        "http" in message.content.lower()
        and "Neighbor" not in role_names
        and not "Cryptographer" in role_names
    ):
        return Forbidden(
            is_forbidden=True,
            reason="Please don't use http. Just tell me about what's at the link. I want to hear it from you.",
        )

    if "!" in message.content and "<@!" not in message.content and not based_role_in_based_channel:
        # print(" '!' in message.content: ", message.content)
        return Forbidden(
            is_forbidden=True,
            reason="Please don't use exclamation points. I like it when you're calm.",
        )

    elif demoji.findall(message.content) and not based_role_in_based_channel:
        # print("demoji.findall(message.content)")
        # socketio.emit("flash", [session["anonymous_user_id"],
        # ])
        return Forbidden(
            is_forbidden=True,
            reason="Can you say that with words? I really want to understand you.",
        )

    # print("message.attachments= ", message.attachments)

    if message.attachments == []:
        if len(message.content) == 0:
            print("len(message.content) == 0")
            return Forbidden(
                is_forbidden=True, reason=f"Your message.content was too short."
            )
        # if len(message.content) == 0:
        #     # print("len(message.content) < 2")
        #     return Forbidden(is_forbidden=True, reason=f".")

        # REQUIRE PUNCTUATION in all chann
        elif (message.channel.name != "fm-bot" and not based_role_in_based_channel) and re.match(
            r"[a-zA-Z0-9]+$", message.content.strip()[-1]
        ):
            print("doesnt end with punctuation")

            return Forbidden(
                is_forbidden=True,
                reason=f"Please end your message.contents with punctuation. It makes it easier for me to read",
            )

    elif message.content.endswith("**"):
        # print("message.content.endswith **")
        return Forbidden(is_forbidden=True, reason="ends with **")

    for x in strings_to_delete:
        if x in message.content.lower():
            # print("strings_to_delete: ", x)

            return Forbidden(is_forbidden=True, reason=f"message contains {x}")

    tiktokForbidden = ["you should", "weezer should", "rivers should"]

    if message.channel.id == channels["tiktok"]:
        for f in tiktokForbidden:
            if f in message.content.lower():
                return Forbidden(
                    is_forbidden=True, reason=f"Replace {f} with 'I should'"
                )
            
    if message.channel.id == channels["shrine"]:
        if message.reference:
            return Forbidden(is_forbidden=True, reason="Replies are not allowed in the Shrine. Please read the channel description at the top of the page.")

    # for x in forbidden_words:
    #     if x in message.lower():
    #         print("forbidden_words: ", x)

    #         return Forbidden(
    #             is_forbidden=True, reason=f"Message contains forbidden_words"
    #         )

    return Forbidden(is_forbidden=False, reason="")


# def clean_member_name(member_name):
#     # clean up the member name
#     member_name = demoji.replace(member_name)
#     member_name = profanity.censor(member_name)
#     return member_name


async def message_is_forbidden(message: discord.Message, role_names):
    """ punctuation and emoji http among others """

    allowed_ids = [rivers_id, cuomputer_id]

    if message.author.id in allowed_ids:
        return False

    # DELETE FORBIDDEN MESSAGES
    # put this first so it doesn't take too long
    forbidden = forbidden_message(message, role_names)

    if forbidden.is_forbidden:
        # print("forbidden:", forbidden.reason)
        try:
            channel = await message.author.create_dm()
            await message.delete()
            await channel.send(forbidden.reason + "\n\n" + message.content)
        except:
            # print(
            #     "Couldn't delete message because it doesn't exist. or another server? Maybe Dyno already got it for another reason?"
            # )
            return
        # await message.channel.send(forbidden.reason)

        return True
    return False


async def message_is_too_negative(message: CustomMessage, role_names):
    """ if polarity < negativity_threshold """

    from config import negativity_threshold

    test_message = message.content.lower().replace("rivers,", "").strip()[:-1]

    if len(test_message) > 8:

        polarity = get_polarity(test_message)
        # print(polarity)

        # negativity_threshold=negativity_threshold

        if message.channel.name == "shrine":
            negativity_threshold = 0.1

        if polarity < negativity_threshold:
            # print(f"\t!!!!TOO NEGATIVE!!!!! {polarity}")

            channel = await message.author.create_dm()

            try:

                await message.delete()

                await channel.send(
                    f"Your message was deleted because the sentiment was too negative [{polarity}]. The negativity threshold for this channel is {negativity_threshold}.\n\n"
                    + message.content
                )
            except:
                pass

            return True
    return False


async def name_contains_profanity(name, message: CustomMessage = None, member=None):
    """
    The 2 kwargs are when this function is called from on member join.
    """
    if (
        profanity.contains_profanity(name)
        or "everyone" in name.lower()
        or "arse" in name.lower()
        or "racist" in name.lower()
        or "whore" in name.lower()
    ):
        print(
            f"{name} will not be able to post here because failed profanity check."
        )
        if message:
            channel = await message.author.create_dm()
            await message.delete()
        elif member:
            channel = await member.create_dm()

        try:
            await channel.send(
                f"{name}, you won't be able to post here because your username contains un-neighborly language."
            )
        except Exception as e:
            pass
            # print(e)
            # print(member_name, channel)
        return True
    return False
