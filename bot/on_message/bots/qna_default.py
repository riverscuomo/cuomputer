from bot.scripts.message.finalize_response import finalize_response


async def post_qna_default_response(message):

    response = "I'm sorry, I don't understand. This channel is for questions related to the operation of my server."
    response = finalize_response(response, message.nick)
    response += "\n\n"

    reply = [
        response,
        "To have a fun conversation with me: please use the #coach-cuomo channel--but make sure you have the Neighbor role first.\n",
        "To report a bug: please use the relevant channel in the Tech Support section.\n",
    ]
    await message.channel.send("".join(reply))
