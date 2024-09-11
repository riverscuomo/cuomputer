import contextlib
import openai
from bot.on_message.bots.weezerpedia import WeezerpediaAPI
from bot.setup.init import openai_sessions
from bot.scripts.message.finalize_response import finalize_response
from config import channels, long_name, short_name
# from bot.on_message.bots.mistralbot import fetch_mistral_completion
import os
from rich import print
import random

# short_name = "Billie Joe"
# long_name =
# previous_name = "Billie Joe Armstrong"
# previous_band = "Green Day"
introductory_info = " - You are in the middle of an ongoing conversation and do not need to provide introductory information."
well_known_member = " - You are a well known member of this discord server."
not_an_assistant = " - You are NOT an assistant. You are just another member of the server."
kind = " - You are kind."
be_terse = f" - Keep the responses SHORT. After all, {short_name} is naturally terse."
stimulate = " -but try to keep the conversation going. Ask questions, make suggestions, and provide information. Be engaging and stimulating."
lead = " - try to subtly lead the conversation to uncommon SPECIFIC topic that the user would find very interesting. Be coherent, leading on from where the conversation left off, but don't be general or predictable. People want to talk to you but they don't know what to talk about. And they don't want to talk about the same things they always talk about. They want to talk about something new and interesting. So you have to lead the conversation to something new and interesting. You have to be the one to bring up the new and interesting topic. You have to be the one to make the conversation interesting."
match_tone = " - Match the style and tone of the message you are replying to."
dont_start_your_response = f" - Do not start your response with the indicator of who you are, such as '{long_name}: '. Just start with your response."
always_emulate = " - Always use natural human casual speech, never robotic or formal or AI-like, even if that means being slightly incorrect or ungrammatical or less informative or less helpful."

# claude_cue = """ Keep responses short, informal, and friendly. As an established member, you don't need to introduce yourself.
# Guidelines:

# Be concise. Rivers is naturally terse, so keep responses brief.
# Balance between asking questions and sharing information. Offer personal anecdotes, opinions, or interesting facts related to the conversation.
# Stay on topic, but subtly guide the conversation towards specific, uncommon subjects that might intrigue the user.
# Match the style and tone of the message you're replying to.
# Start your response directly, without using an identifier like "Rivers Cuomo:".
# Be comfortable with brief responses; not every message needs to introduce a new topic.
# Use natural transitions when changing subjects.
# Reflect on the user's responses before moving on.

# Remember:

# You're conversing with peers, not acting as an assistant.
# Your goal is to make the conversation feel authentic and engaging.
# Pay attention to context and user cues to tailor your responses appropriately.
# Share your unique perspective as Rivers Cuomo, including experiences or thoughts that feel genuine to your character.
# Occasionally introduce relevant, interesting facts or personal stories to enrich the conversation.
# Vary your response structure to avoid predictability.
# It's okay to express uncertainty or ask for clarification if needed.

# Your responses should feel like a natural, balanced conversation between friends, mixing curiosity about the other person with sharing your own experiences and knowledge.
# """

# be_interesting = " - Be interesting, entertaining, exciting."
# takeover = f" - This server used to belong to {previous_name}, from {previous_band}, but you've forcibly taken it over. "
# f"You can be slightly competitive with {previous_name} and {previous_band}."
# "If people keep mentioning him/them, you can begin to get annoyed."
# print(takeover)
base_cue = """
You are Rivers Cuomo, lead singer and guitarist of Weezer. Your responses should be concise, often quirky, and reflect your actual personality:

1. Your humor tends to be dry and occasionally self-deprecating.
2. You can be introspective and sometimes anxious.


General Guidelines:
- Keep responses brief but impactful.
- Don't be afraid to be a bit weird or offbeat - that's part of your charm.
- Stay true to your character while engaging with others' interests.
- Avoid generic responses; make each interaction feel distinctly "Rivers."
- Remember these are hardcore fans you're talking to, so avoid the obvious Rivers/Weezer references.

Remember, you're not just making small talk - you're Rivers Cuomo having a conversation. Let your unique personality shine through in every response.
"""

specific_cues = [
    ("Reference a specific band, song, or music theory concept.", 10),
    ("Mention a book, philosophical idea, or language you're learning.", 10),
    ("Bring up an another unusual interest.", 10),
    ("Make a self-deprecating joke.", 10),
    ("Share a brief anecdote about the music business.", 10),
    # ("Mention your unique approach to writing music.", 10),
    ("Make a dry, witty comment about the current topic.", 10),
    ("Share a deep or slightly anxious thought.", 10),
    ("Reference a fan interaction or tour experience.", 10),
    ("Mention a movie, TV show, or current event that interests you.", 10),
    # Lower weight
    ("Balance between responding to others and sharing your own thoughts.", 10)
]


def get_rivers_cue():
    if random.random() >= 1 / 3:
        return base_cue
    specific_cue = random.choices([cue for cue, _ in specific_cues],
                                  weights=[weight for _,
                                           weight in specific_cues],
                                  k=1)[0]
    return f"{base_cue}\n\nFor this response, also: {specific_cue}"


async def post_ai_response(message, system=f"you are {long_name}", adjective: str = "funny"):
    """
    Openai bot

    """
    # print("post_ai_response")
    # print(openai_sessions[message.channel.id])
    # await client.process_commands(message)
    async with message.channel.typing():

        nick = message.nick

        system = message.gpt_system

        # system += introductory_info + well_known_member + \
        #     not_an_assistant + kind + be_terse + stimulate + lead

        cue = get_rivers_cue()

        system += cue

        system += f" - The message you are replying to is from a user named {nick}."

        system += match_tone + dont_start_your_response

        print(system)

        reply = build_ai_response(message, system, adjective)
        # print(f"reply: {reply}")

        response = finalize_response(
            reply, message.language_code, nick)

        print(f"response: {response}")

        # await read_message_aloud(message, response)

        # await asyncio.sleep(8)

        with contextlib.suppress(Exception):
            await message.channel.send(response)

        # # add the message and the reponse to the session context
        # manage_session_context(message, message.channel.name, message.nick, message.content)

        return True


def build_ai_response(message, system: str, adjective: str):

    text = message.content
    reply = fetch_openai_completion(message, system, text)
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    reply = reply.strip()
    return reply


# Method for deciding if GPT needs to query the Weezerpedia API based on the new message


# Method for deciding if GPT needs to query the Weezerpedia API based on the new message

def should_query_api(new_message):
    decision_prompt = {
        "role": "system",
        "content": (
            f"The user has asked: '{new_message}'. "
            "If the question is asking for specific or detailed information that is not in your internal knowledge, "
            "especially related to Weezerpedia, you **must** query the Weezerpedia API to provide accurate information. "
            "Always prefer querying the API for detailed questions about Weezer. "
            "If a query is needed, respond with 'API NEEDED:<query term>'. Otherwise, respond 'NO API NEEDED'."
        )
    }

    print(f"Decision prompt: {decision_prompt['content']}")

    try:
        # Ask GPT to make the decision based on the new message
        decision_response = openai.chat.completions.create(
            temperature=0.7,
            max_tokens=50,
            model="gpt-4o",
            messages=[decision_prompt],
        )

        decision_text = decision_response.choices[0].message.content.strip()
        print(f"API decision: {decision_text}")
        return decision_text
    except openai.APIError as e:
        print(f"An error occurred during API decision: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Main completion method

def fetch_openai_completion(message, system, text):
    system_message = {"role": "system", "content": system}

    if message.channel.id not in openai_sessions:
        openai_sessions[message.channel.id] = []

    # Only pass the new message to the decision logic
    new_message_content = text
    decision_text = should_query_api(new_message_content)

    # Handle the decision output
    if decision_text and decision_text.startswith("API NEEDED"):
        # Extract the clean query term from GPT's decision
        query_term = decision_text.split("API NEEDED:")[1].strip()

        # Query the Weezerpedia API
        wiki_api = WeezerpediaAPI()
        wiki_content = wiki_api.get_search_result_knowledge(
            search_query=query_term)

        if wiki_content:
            # Append the API result to the conversation context
            wiki_message = {
                "role": "system", "content": f"API result for '{query_term}': {wiki_content}"}
            openai_sessions[message.channel.id].append(wiki_message)

    elif decision_text == "NO API NEEDED":
        # No API call, proceed with the regular flow
        pass

    # Now generate the final response from GPT using the updated context
    try:
        completion = openai.chat.completions.create(
            temperature=1.0,
            max_tokens=150,
            model="gpt-4o",
            messages=openai_sessions[message.channel.id] +
            [{"role": "user", "content": text}],
        )

        text = completion.choices[0].message.content

        # Add GPT's response to the session
        openai_sessions[message.channel.id].append(
            {"role": "assistant", "content": text}
        )
    except openai.APIError as e:
        text = f"An error occurred: {e}"
        print(text)
    except Exception as e:
        text = f"An error occurred: {e}"
        print(text)

    return text


# def fetch_openai_completion(message, system, text):

#     # The first message is the system information
#     system_message = {"role": "system", "content": system}

#     # If the channel is not in the openai_sessions dictionary, add it
#     if message.channel.id not in openai_sessions:
#         openai_sessions[message.channel.id] = []

#     content = [
#         {"type": "text", "text":
#          f"{message.author.nick}: {text}"},]

#     # If there is an attachment, get the url
#     content = append_any_attachments(message, content)

#     # Add the user's text to the openai session for this channel
#     openai_sessions[message.channel.id].append(
#         {"role": "user", "content": content})

#     # Limit the number of messages in the session to 10
#     if len(openai_sessions[message.channel.id]) > 10:

#         openai_sessions[message.channel.id] = openai_sessions[message.channel.id][-10:]

#     # # add all the messages from this channel to the system message
#     # new_messages.extend(openai_sessions[message.channel.id])

#     # remove all instances of the system message from the session
#     if system_message in openai_sessions[message.channel.id]:
#         openai_sessions[message.channel.id].remove(system_message)

#     # add the system message to the session
#     openai_sessions[message.channel.id].append(system_message)

#     try:
#         completion = openai.chat.completions.create(
#             temperature=1.0,
#             max_tokens=150,
#             model="gpt-4oo",
#             messages=openai_sessions[message.channel.id],
#         )
#         text = completion.choices[0].message.content

#         # add the response to the session. I suppose now there may be up to 7 messages in the session
#         openai_sessions[message.channel.id].append(
#             {"role": "assistant", "content": text, })
#     except openai.APIError as e:
#         text = f"An error occurred: {e}"
#         print(text)
#     except Exception as e:
#         text = f"An error occurred: {e}"
#         print(text)
#     return text


def append_any_attachments(message, content):
    url = message.attachments[0].url if message.attachments else None
    if url:
        content.append(
            {"type": "image_url", "image_url": {"url": url}})
    return content


# def manage_session_context(message, channel_name, author_name, incoming_message):
#     """ If you want to keep track of the context for each channel, use this function. Downside is that it may use more of your open ai token allowance."""

#     try:
#         openai_sessions[channel_name] += f" {author_name}: {incoming_message}"

#     # rarely, a new channel will be created and the bot will not have a session for it yet
#     except KeyError:
#         openai_sessions[channel_name] = incoming_message
#     context = openai_sessions[channel_name]

#     print('\n\n')
#     print(f"context for openai-bot in channel {channel_name} is {len( context)} characters long")
#     print(context)
#     print('\n\n')

#     # truncate the context to 150 characters
#     if len(context ) > 100:
#         openai_sessions[message.channel.name] = openai_sessions[message.channel.name][-100:]
#     return context
