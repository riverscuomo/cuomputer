import openai
import requests
import sys
from io import BytesIO

from config import OPENAI_API_KEY

sys.path.append("...")  # Adds higher directory to python modules path.
openai_client = openai.Client(api_key=OPENAI_API_KEY)

async def process_image_and_respond(attachment, channel):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {"url": attachment.url}},
                    ],
                }
            ],
            max_tokens=300,
        )

        description = response.choices[0].message.content
        await channel.send(description)

    except Exception as e:
        await channel.send("Sorry, I couldn't analyze the image.")
        print(f"Error: {e}")