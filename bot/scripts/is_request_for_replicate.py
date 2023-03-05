from config import REPLICATE_API_TOKEN , channels
import replicate

# https://replicate.com/account
# I set a limit of $5 per month with google pay

model = replicate.models.get("stability-ai/stable-diffusion")

# regex formula to replace "show me " in a string, upper or lower case
import re


def generate_image(query):
    """ From Arthuremidio's model, returns an image based on the query."""
    print("Arthuremidio's model")

    # the line below is needed because it is a best practice to train the model where the "new content"
    # corresponds to an uncommon 3-character string (in our case, 'cjw'). thus, with the line below we're
    # replacing in the original prompt string any occurrence of  "Rivers" or "Rivers Cuomo" (case insensitive) with 'cjw'.
    query_adjusted = re.sub('Rivers Cuomo|Rivers', 'cjw', query, flags=re.IGNORECASE)

    model = replicate.models.get("arthuremidio/rivers")
    
    # # the line below is for us to specify a specific version of the model. I recommend having it as we plan to iterate on the model.
    # # then, you can switch to another version once we try it out
    # version = model.versions.get("af7728c2f0f70568ba57c52558a4b030c18f4cebbe44071df7442906df3c3cb3")

    image = model.predict(prompt=query_adjusted, api_token=REPLICATE_API_TOKEN)
    
    return image[0]




async def is_request_for_replicate_image(message, member_roles, firestore_user):
    """ Returns True if the message is a request for a replicate image, meets, conditions, and sends the image."""
    if message.content.lower().startswith("show me "):
        user_score = firestore_user["score"]
        print(f"is_request_for_replicate_image. user_score={user_score}")

        if user_score > 4:
            
            prompt = re.sub(r"show me\s", "", message.content, flags=re.IGNORECASE)
            # prompt = prompt.lower().replace("show me ", "")[:-1]
            print(prompt)
            # # print(message.author.name)
            
            if "rivers" in prompt.lower():
                image = generate_image(prompt)
            else:

                image = model.predict(
                    prompt=prompt,
                    api_token=REPLICATE_API_TOKEN,
                    )
            
                image = image[0]
            # print(image)
            # await message.channel.send("Replicate request")
            s = f"{message.author.name}, {prompt}."
            await message.channel.send(s)
            await message.channel.send(image)
            return True
    return False