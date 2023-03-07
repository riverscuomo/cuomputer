import requests
from rich import print
from cachetools import cached, TTLCache
from dotenv import load_dotenv
import os

load_dotenv()

LIBRARY_API = os.getenv("LIBRARY_API")
USERS_API = os.getenv("USERS_API")
USERS_API_TOKEN= os.getenv("USERS_API_TOKEN")
USERS_API_USER_ID= os.getenv("USERS_API_USER_ID")

cache = TTLCache(maxsize=100000, ttl=60)
wikiCache = TTLCache(maxsize=100000, ttl=60 * 60)

@cached(wikiCache)
def fetch_entries():
    print("fetch_entries")
    response = requests.get(
        url=LIBRARY_API,
    )
    if response.status_code != 200:
        print("error getting entries from 1.0")
        return []

    try:
        json = response.json()
    except Exception as e:
        print(e)
        print(response)
        print("books r fun must be down")

    return json["entries"]


async def fetch_roles(guild):
    """ returns the list of roles and the list of role names for the server """
    roles = await guild.fetch_roles()
    role_names = [x.name for x in roles]
    return roles, role_names


@cached(cache)
def fetch_users():
    print("fetch_users from Api (every 60 seconds?)")
    response = requests.get(
        url=USERS_API,
        headers={
            "TOKEN": USERS_API_TOKEN,
            "userId": USERS_API_USER_ID,
        },
    )
    if response.status_code != 200:
        print("error getting bundles from 1.0")
        return []

    json = response.json()

    users = json["users"]
    lastUpdated = json["last_updated"]
    print(f"Users last updated at: {lastUpdated}")
    # print(users[-1])
    return users


def main():
    
    # TEST
    users = fetch_users()
    users = [x for x in users if x["username"] == "Olivia"]
    print(users)

    entries = fetch_entries()
    print(entries)


if __name__ == "__main__":
    main()
