from datetime import datetime, timezone
from bot.db.fetch_data import fetch_users
from bot.scripts.get_firestore_user import get_firestore_user

# from bot.setup.init import firestore_users, client
from bot.setup.init import client
from bot.scripts.message.fix_nick import fix_nick
import config
# from config import (
#     # bundles_map,
#     # time_based_roles,
#     # firestore_time_format,
#     # og_cutoff,
#     # user_to_remove,
#     # GUILD_ID,
#     members_to_skip,
# )

from bot.db.fbdb import db
from firebase_admin import firestore
from rich import print


async def add_time_based_roles(member, roles):
    """
    If you want to change the name of the role, replace all in discord_bot
    and don't forget to change the name of the role in server/roles/settings.

    0.2: "Visitor",
    0.4: "Friend",

    2: "Neighbor",
    """
    print('add_time_based_roles')

    now = datetime.now(timezone.utc)
    joined_at = member.joined_at
    delta = now - joined_at
    # print(delta)
    # days = delta.days
    hours = int(delta.total_seconds() / 3600)
    # print(member.name, delta, "; hours: ", hours)
    # if hours < 1000:
    # print(f"add_time_based_roles for {member.name} who joined {hours} hours ago.")

    member_roles = [x.name for x in member.roles]
    # print(member_roles)
    # print(time_based_roles)
    

    if hours >= config.neighbor_threshold:
        if "Visitor" in member_roles:
            print(f"Removing Visitor from {member.name}")
            role = next((x for x in roles if x.name == "Visitor"), None)
            # print(role)
            await member.remove_roles(role)
        if "Neighbor" not in member_roles:
            print(f"Adding Neighbor to {member.name}")
            role = next((x for x in roles if x.name == "Neighbor"), None)
            # print(role)
            await member.add_roles(role)
    else:
        if "Visitor" not in member_roles:
            print(f"Adding Visitor to {member.name}")
            role = next((x for x in roles if x.name == "Visitor"), None)
            # print(role)
            await member.add_roles(role)
        """ YOU CAN'T REMOVE NEIGHBOR AUTOMATICALLY CUZ SOME NEWBIES MAY HAVE A BUNDLE """
        # if "Neighbor" in member_roles:
        #     print(f"Removing Neighbor from {member.name}")
        #     role = next((x for x in roles if x.name == "Neighbor"), None)
        #     # print(role)
        #     await member.remove_roles(role)

    
    # # k, v
    # for threshold, role_name in time_based_roles.items():
    #     # print(threshold, role_name)

    #     role = None

    #     # Remove Visitor role so it can give exclusive access to newbies in Welcome
    #     if role_name == "Visitor":
    #         # print("Visitor")
            
    #         if "Visitor" in member_roles and "Neighbor" in member_roles: 
    #             print(f"Removing Visitor from {member.name}")
    #             role = next((x for x in roles if x.name == role_name), None)
    #             # print(role)
    #             await member.remove_roles(role)
    #             # print(member.roles)
    #         continue
        

        # elif hours >= threshold:
        #     # print(f"Not Visitor so going on to check {role_name}")
        #     # print(hours, threshold, role_name)

        #     # Create the role object
        #     role = next((x for x in roles if x.name == role_name), None)
        #     # print(role)

        #     if role not in member.roles:                

        #         # print(hours, " >= ", threshold, " == ", hours > threshold, end=" so ")
        #         print("adding role ", role_name, f" for {member.name}")

        #         # add the role object to the member
        #         await member.add_roles(role)

        """ YOU CAN'T REMOVE NEIGHBOR AUTOMATICALLY CUZ SOME NEWBIES MAY HAVE A BUNDLE """
        # else:
        #     # member_roles = [x.name for x in member.roles]
        #     if role in member.roles:
        #         print(
        #             days,
        #             " < ",
        #             threshold,
        #             " == ",
        #             days > threshold,
        #             end=f" so removing {role.name} for {member.name}",
        #         )

        #         await member.remove_roles(role)
        # print("\n")


async def add_remove_roles_for_specific_users(author, roles):
    print("add_remove_roles_for_specific_users")
    if author.id == config.user_to_remove:
        await author.remove_roles(next(x for x in roles if x.name == "Camp Counselor"))
        await author.remove_roles(next(x for x in roles if x.name == "Archivist"))
        await author.remove_roles(next(x for x in roles if x.name == "Librarian"))


async def check_firestore_and_add_roles_and_nick(member, roles):
    """
    Checks if this discord member is also an MRN member with a firestore record.

    If so, add the roles and nick.
    """
    print('check_firestore_and_add_roles_and_nick')
    firestore_users = fetch_users()

    firestore_user = get_firestore_user(member.id, firestore_users)

    # print(next(x for x in roles if x.name == "Neighbor").id)

    # ROUTINES TO RUN ON FIRESTORE USERS
    if firestore_user:
        # print(firestore_user)

        await add_og_role_from_firestore_user(member, firestore_user, roles)

        await add_roles_from_firestore_badges(member, firestore_user, roles)

        await add_roles_from_firestore_bundles(member, firestore_user, roles)

        nick = firestore_user["username"]

        actor_role = next(x for x in roles if x.name == "Actor")

        if member.name != "Rivers":  # and actor_role not in member.roles:
            await member.edit(nick=nick)

    else:
        # print("not MRN")
        nick = await fix_nick(member)

    return member, nick, firestore_user


async def add_og_role_from_firestore_user(member, firestore_user, roles):
    """
    Assign the OG role for rc.com reg date

    """
    print('add_og_role_from_firestore_user')
    if "registeredOn" in firestore_user:

        # A default for firestore user's who are missing registered on for some reason.
        registered_on = "Fri, 31 Jul 2020 00:00:00 GMT"

        # replace with the actual if it exists
        if firestore_user["registeredOn"] is not None:
            registered_on = firestore_user["registeredOn"]

        # registered_on = datetime.strptime("Jun 1 2005  1:33PM", "%b %d %Y %I:%M%p")
        registered_on = datetime.strptime(registered_on, config.firestore_time_format)
        # Sat, 12 Jun 2021 07:00:06 GMT

        if registered_on < config.og_cutoff:

            await member.add_roles(next(x for x in roles if x.name == "OG"))


async def add_roles_from_firestore_badges(member, firestore_user, roles):

    """
    Assign any roles they have MRN badges for.
    No way to add Neighbor here unless they have entered the

    """
    print('add_roles_from_firestore_badges')

    member_roles = [x.name for x in member.roles ]
    # print(member_roles)

    # # if they don't already have the neighbor role
    # if not member.get(member.roles, name="Neighbor"):

    #     print("miss the neighor role so adding: ", member)

    # # add the Neighbor object to the member
    # await member.add_roles(next(x for x in roles if x.name == "Neighbor"))

    # build a list of strings for each of the roles that the member already has

    # print(member_bundles)
    # member_roles.extend(member_bundles)
    # print(f"roles: {member_roles}")

    # if len(member_roles) > 2:

    # firestore_user = [x for x in firestore_users if x["discordId"] == discord_id]
    # if firestore_user == []:
    #     return
    # print(f"this firestore_user has at least 1 badge: {firestore_user}")

    badges = [x for x in firestore_user["badges"] if x!="Visitor"]
    # print(badges)

    for role in badges:
        if role not in member_roles:
            # print(f"Need to add <{role}>")

            try:
                # Create the role object
                role_obj = next(x for x in roles if x.name == role)
                # print("!" + role_obj.name)

                # add the role object to the member
                await member.add_roles(role_obj)
            except Exception as e:
                # print(f'{e}')
                pass
        # else:
        # print(f"Already has <{role}>")


async def add_roles_from_firestore_bundles(member, firestore_user, roles):

    """
    Assign any roles they have MRN bundles for.
    I can add Neighbor to the discord roles.
    But only if they're connected.

    """
    print('add_roles_from_firestore_bundles')
    # build a list of strings representing the bundle names they own
    member_bundles = [
        config.bundles_map[x] for x in firestore_user["bundleIds"] if x in config.bundles_map
    ]

    # build a list of strings for each of the roles that the member already has
    member_roles = [x.name for x in member.roles]

    # I'm adding the Neighbor role to the member's roles
    # but that doesn't guarantee they will be connected.
    # If not, they will be prompted to connect.
    if member_bundles and "Neighbor" not in member_roles:
        # if they don't already have the neighbor role
        # if not member.get(member.roles, name="Neighbor"):

        # print("miss the neighor role so adding: ", member)

        # db.collection("users").document(firestore_user.id).update(

        # add the Neighbor object to the member
        await member.add_roles(next(x for x in roles if x.name == "Neighbor"))

    for role in member_bundles:
        if role not in member_roles:
            # print(f"Need to add <{role}>")

            try:
                # Create the role object
                role_obj = next(x for x in roles if x.name == role)
                # print(f"!{role_obj.name}")

                # add the role object to the member
                await member.add_roles(role_obj)
            except Exception as e:
                print(e)
        # else:
        #     print(f"Already has <{role}>")


async def delete_bad_roles(member, bad_roles):

    """
    Delete bad roles. A one-time function.
    """

    # member_roles = [x.name for x in member.roles]

    for role in bad_roles:

        # print(member.name, role)
        if role in member.roles:
            print(f"Need to remove <{role}>")

            # add the role object to the member
            await member.remove_roles(role)


async def add_discord_roles_to_firestore_user():
    """
    a one time function to save the accumulated discord service and interest roles to the firestore user records.
    From now on, any additions or removals will be handled by client.on_member_update in bot.py.
    """

    firestore_users = fetch_users()

    discord_roles_to_save_to_firestore = [
        "Srs",
        "Calm",
        "Camp Counselor",
        "Dan",
        "El Scorcho",
        "Artist",
        "Pink Triangle",
        "Writer",
        "Poet",
        "D.J.",
        "Delinquent",
        "gec",
        "Geezer",
        "Musician",
        "Archivist",
        "Tour Guide",
        "Librarian",
        "Curator",
        "Biographical Researcher",
        "Night Watchman",
        "Performer",
        "Parental Advisory",
        "Graphic Design",
        "Data Scientist",
        "Welcome Committee",
        "Creative Director",
    ]
    guild = client.get_guild(config.GUILD_ID)

    members = guild.members
    # print(len(members))

    for member in members:

        # If they don't have more than 5 roles, skip them.
        if len(member.roles) < 5:
            continue

        roles = [
            x.name for x in member.roles if x.name in discord_roles_to_save_to_firestore
        ]

        if not roles:
            continue

        # Get the firestore user dictionary that corresponds to this discord user.
        discord_id = str(member)

        if firestore_user := get_firestore_user(discord_id, firestore_users):
            # print(firestore_user)
            id = firestore_user["id"]

            if ref := db.collection("users").document(id).get():
                ref.reference.update({"badges": firestore.ArrayUnion(roles)})
            else:
                print(f"No firestore user record with firestore id {id}")


# @client.event
# async def on_ready():

#     print(f"Logged into discord add_roles as {client.user.id}")
#     # print(client.intents)

#     await add_discord_roles_to_firestore_user()
#     exit()

#     guild = client.get_guild(config.GUILD_ID)
#     roles = await guild.fetch_roles()
#     bad_roles = [
#         x for x in roles if x.name in ["Supporter", "Champion", "100+", "400+", "1000+"]
#     ]

#     members = guild.members

#     for member in members:

#         # If they don't have more than 5 roles, skip them.
#         if len(member.roles) > 5:

#             print(member.roles)

#             await delete_bad_roles(member, bad_roles)


# def main():
#     asyncio.run(add_discord_roles_to_firestore_user())


# if __name__ == "__main__":

#     # main()
#     client.run(TOKEN)
