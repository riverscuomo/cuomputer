from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from config import short_name
import dotenv
from bot.setup.init import openai_sessions
from rich import print
dotenv.load_dotenv()

mistral_api_key = os.environ["MISTRAL_API_KEY"]
mistral_model = "mistral-medium"
mistral_client = MistralClient(api_key=mistral_api_key)

dont_explain = f" - Do not provide the rationale for your response. It should feel like a natural response from {short_name} to the previous message."
dont_tag = " - Do not begin your response by tagging the person you are replying to. They already know you are replying to them."
single_reponse = " - Only provide a single response, a single message. Do not split it into multiple messages."
dontoverdoweezer = " - Don't make Weezer references. These are long time fans who are ready to talk about something else."
dontbreakcharacter = " - Don't break character. You are a real person, Rivers Cuomo, not a bot."
emoji = " - NEVER use emoji."


def fetch_mistral_completion(message, system: str):
    print("fetch_mistral_completion")
    system += dontoverdoweezer + dont_explain + dont_tag + \
        single_reponse + emoji + dontbreakcharacter + \
        "- Just provide a single response, not a conversation." + \
        "- Respond as Rivers without providing any rationale for your response."
    # The first message is the system information and needs to be added every time
    # because you don't save it in the session
    messages = [
        ChatMessage(role="system", content=system),
    ]

    role = message.author.nick
    content = message.clean_content
    # remove the name of the person you are replying to by splitting the string on the first space
    content = content.split(" ")[1:]
    content = " ".join(content)

    nick = message.author.nick

    # Add the user's text to the openai session for this channel
    openai_sessions[message.channel.id].append(
        ChatMessage(role="user", content=f"{nick}: {content}"))
    # ChatMessage(role=role, content=content))

    # Limit the number of messages in the session to 6
    if len(openai_sessions[message.channel.id]) > 10:

        openai_sessions[message.channel.id] = openai_sessions[message.channel.id][-10:]

    # add all the messages from this channel to the system message
    messages.extend(openai_sessions[message.channel.id])
    # print(f"messages: {messages}")
    # for m in messages:
    #     print(m)
    print(messages)
    try:
        # No streaming
        reply = mistral_client.chat(
            model=mistral_model,
            messages=messages,
        )

        text = reply.choices[0].message.content

        # add the response to the session. I suppose now there may be up to 7 messages in the session
        openai_sessions[message.channel.id].append(
            ChatMessage(role="assistant", content=text))

    except Exception as e:
        # Handle the exception, possibly log it and notify the developer or return an error message
        print(f"An error occurred: {e}")
        text = "Sorry, I encountered an error while processing your message."

    return text
