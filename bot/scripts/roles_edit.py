import discord
from rich import print
from bot.setup.discord_bot import client, GUILD_ID
from config import TOKEN, CLIENT_ID


"""
change the color of all roles
role properties?
"""


OAUTH2_URL = (
    "https://discord.com/api/oauth2/authorize?client_id="
    + CLIENT_ID
    + "&permissions=8&scope=bot"
)
OAUTH2_URL = (
    "https://discord.com/api/oauth2/authorize?client_id="
    + CLIENT_ID
    + "&permissions=8&redirect_uri=https%3A%2F%2Frcwebserver.herokuapp.com%2F&response_type=code&scope=bot%20activities.write%20activities.read%20relationships.read%20applications.entitlements%20applications.store.update%20applications.commands%20applications.builds.read%20rpc.voice.read%20rpc.voice.write%20rpc.activities.write%20webhook.incoming%20messages.read%20applications.builds.upload%20identify%20email%20connections%20guilds%20guilds.join%20gdm.join%20rpc%20rpc.notifications.read"
)
GUILD_ID = 890210072381247548
TOKEN = open("token.txt", "r").readline()

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():

    guild = client.get_guild(GUILD_ID)

    print("Logged in as {0.user}".format(client))
    roles = await guild.fetch_roles()

    for r in roles:

        color = "fafafa"

        # convert the hex value to an int value
        color = int(color, 16)

        try:

            if r.position > 3:

                await r.edit(color=discord.Color.from_rgb(250, 250, 250))

            else:
                await r.edit(color=discord.Color.from_rgb(180, 180, 180))
        except:
            print(f"couldn't change the color of {r.name}")


client.run(TOKEN)
