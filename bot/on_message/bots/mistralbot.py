from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
import dotenv
from bot.setup.init import openai_sessions
dotenv.load_dotenv()


mistral_api_key = os.environ["MISTRAL_API_KEY"]
mistral_model = "mistral-tiny"

mistral_client = MistralClient(api_key=mistral_api_key)


def fetch_mistral_completion(message: str, system: str):
    # The first message is the system information
    messages = [
        ChatMessage(role="system", content=system)
    ]

    # Add the user's text to the openai session for this channel
    openai_sessions[message.channel.id].append(
        ChatMessage(role="user", content=f"{message.author.name}: {message.content}"))

    # Limit the number of messages in the session to 6
    if len(openai_sessions[message.channel.id]) > 6:

        openai_sessions[message.channel.id] = openai_sessions[message.channel.id][-3:]

    # add all the messages from this channel to the system message
    messages.extend(openai_sessions[message.channel.id])
    # print(f"messages: {messages}")
    for m in messages:
        print(m)

    # No streaming
    reply = mistral_client.chat(
        model=mistral_model,
        messages=messages,
    )

    text = reply.choices[0].message.content

    # add the response to the session. I suppose now there may be up to 7 messages in the session

    ChatMessage(role="assistant", content=text)

    return text
