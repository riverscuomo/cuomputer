import random
from bot.setup.bots import openai_bot
from bot.scripts.message.finalize_response import finalize_response
from bot.setup.bots import resource_manager
import random


async def post_flirty_response(nick, message, language):
    """ pickup_lines, sweet_things, or openai (if in budget) """

    reply = get_flirty_response(message).replace(" ;)", "")
    # print(reply)

    if reply is None:
        return False

    response = finalize_response(reply, language, nick, replace_names=True)

    await message.channel.send(response)

    return True


def get_flirty_response(message: str):

    # """ If OPENAI is not overbudget """
    # reply =
    # return reply

    # """ If OPENAI is overbudget, turn this on instead """
    t = random.randint(1, 5)
    # print("t2=", t)
    if t == 1:
        return random.choice(resource_manager.pickup_lines)
    elif t == 2:
        return random.choice(resource_manager.sweet_things)
    elif t == 3:
        return random.choice(resource_manager.flirty_florida)
    else:
        return openai_bot.build_openai_response(message, "flirtatious")

    # print(message.content)
