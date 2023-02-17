import sys  # For relative imports to work in Python 3.6


sys.path.append("...")  # Adds higher directory to python modules path.

# from time import sleep
import discord
from rich import print
from gspreader import update_range
from bot.setup.init import (
    sheet,
    client,
    roles_sheet_headers as headers,
)

from config import TOKEN, GUILD_ID, skipper_role_ids, default_color


async def print_role_ids_to_sheet():
    """
    Run whenever you add a role.

    Actually, next time try just adding to discord and NOT the sheet. See what happens when you run this function.
    Make sure role names in discord match role names in ROLES.

    It didn't work when I tried to pass in guild from init.

    A common failure is if the spelling isn't exactly the same in the sheet and discord.
    Then the failed run has added the item to the sheet. Oh so maybe you don't have to do it manually.
    """
    guild = client.get_guild(GUILD_ID)

    roles = await guild.fetch_roles()
    # print(roles)

    data = sheet.get_all_records()

    for role in roles:
        try:
            row = next(x for x in data if x["role"] == role.name)
            row["id"] = str(role.id)

        except:
            print(f"No record for {role.name} so adding it to the sheet.")
            row = {x: "" for x in headers}
            row["role"] = role.name
            row["id"] = str(role.id)[:-3]
            data.append(row)

    update_range(sheet, data)


async def set_color(role, color: str):

    color = color.replace("#", "")

    # convert the hex value to an int value
    color = int(color, 16)

    try:

        if role.position > 1:
            print(f"Setting {role.name} to {color}...")

            await role.edit(color=color)

        else:
            await role.edit(color=discord.Color.from_rgb(180, 180, 180))
    except:
        print(
            f"couldn't change the color of {role.name}. Are you sure your color is a string?"
        )


async def set_role_attributes_from_sheet():
    """This definitely works if you have client.run(TOKEN) on at the bottom"""
    print("set_role_attributes_from_sheet")
    guild = client.get_guild(GUILD_ID)
    roles = await guild.fetch_roles()

    data = sheet.get_all_records()

    xdata = [x for x in data if "id" in x and x["id"] != "" and x["position"] != ""]
    # print(xdata)
    xdata.sort(key=lambda x: x["position"], reverse=True)
    # xdata.sort(
    #     key=lambda x: x["position"],
    # )

    for row in xdata:

        print(row["role"], row["id"], row["color"])

        try:
            role = next(x for x in roles if str(x.id) == str(row["id"]))
        except Exception as e:
            print(
                "set_role_attributes_from_sheet couldn't find a discord role matching the spreadsheet row['role']"
            )
            # print(row)
            continue

        if row["color"] not in ["", "#eeeeee"]:
            # print("color data in row")
            await set_color(role, color=str(row["color"]))
        # continue

        if role.id in skipper_role_ids:
            # print(f"Skipping {role.name}")
            # await role.edit(hoist=False)
            continue

        """ 'Hoisting' is making it visible in the sidebar. """
        try:
            # print(role)
            # print(role.hoist)
            if not role.hoist:
                print(f"trying to hoist {role} {role.id}")
                await role.edit(hoist=True)
                print("success")
        except Exception as e:
            print(e)

        """ Update the role's position in the hierarchy. This block only works if you run the script independently """
        try:

            # row = next(x for x in data if x["role"] == role.name)
            # print(role.name, role.id)
            position = int(row["position"])

            if position is not role.position:
                print(f"Updating {role.name} from {role.position} to {position}")

                try:
                    await role.edit(position=position)
                    print(f"success from  {role.position} to {position}")
                except discord.Forbidden:
                    print("You do not have permission to do that")
                except discord.HTTPException:
                    print(f"Failed to move role from {role.position} to {position}")
                except discord.InvalidArgument:
                    print("Invalid argument")
            else:
                print(f"{position}=={role.position}")
        except Exception as e:
            print(e)
            # print(f"no permission from {role.position} to {position}")
        print("\tdone.")


async def print_channel_attributes_to_sheet():
    """"""
    print("print_channel_attributes_to_sheet")
    guild = client.get_guild(GUILD_ID)
    roles = await guild.fetch_roles()
    channels = await guild.fetch_channels()
    # print(channels)
    data = sheet.get_all_records()

    new_channel_names = [x.name for x in channels if x not in [*data]]

    # print(new_channel_names)

    for row in data:
        # print(row["id"])
        row["id"] = str(row["id"])  # no idea why

        for channel in new_channel_names:
            if channel not in row:
                row[channel] = ""

    update_range(sheet, data)


    updated_header_row = headers + new_channel_names
    sheet.update("A1:ZZ1", [updated_header_row])
    # print(updated_header_row)

    data2 = sheet.get_all_records()

    # print(roles)

    for row in data2:

        # print(row["id"])
        row["id"] = str(row["id"])

        # Certain roles will never have access or deny to particular channels
        if row["type"] in ["0: bots"]:
            row[channel] = ""
            continue

        # print(row)
        # try:
        role = next((x for x in roles if str(x.id) == str(row["id"])), None)
        # for x in roles:
        #     print(x.id, row["id"], x.id == row["id"])
        #     if x.id == row["id"]:
        #         print("i found it!")
        #         role = x
        #         break
        # else:
        #     print
        #     x = None
        # role = roles[5]
        # print("asldkfj", role)
        if role is None:
            row[channel] = ""
            continue

        allow = ""
        deny = ""

        for channel in channels:
            # print(role, channel)
            overwrites = channel.overwrites_for(role)
            # print(overwrites)
            if not overwrites.is_empty() and role.name != "@everyone":

                # Returns the (allow, deny) pair from this overwrite.
                # print(channel.name, role.name, overwrites.pair())

                overwrites = overwrites.pair()
                # print(overwrites)
                allow = overwrites[0].value
                # print(allow)
                deny = overwrites[1].value
                # print(deny)

                # if allow != "":
                #     allow = "allow: " + str(allow)
                #     row[channel] = allow
                # if deny != "":
                #     deny = "deny: " + str(deny)
                row[channel] = "perms: " + str(allow) + str(deny)

            else:
                row[channel] = "asdf"
                # row["rules"] = "asldkfj"

            # print(row[channel])

    # print(data2)

    update_range(sheet, data2)

    #
    print("done with print_channel_attributes_to_sheet")


@client.event
async def on_ready():

    """
    For interacting with  the ROLES spreadsheet.
    https://docs.google.com/spreadsheets/d/1K51AJScqeqiGJquOdaHncgFe0UQUEvRCg0QnqeJQxHA/edit#gid=0

    Looks like it will run both in one fell swoop.
    You have to ctrl C to end the program

    This block is actually just for testing.
    Normally the routine runs as part of bot.py on_ready().
    """

    print(f"Logged in as {client.user.id}")
    print(client.intents)

    # user = client.user
    # print(user.top_role)

    await print_role_ids_to_sheet()

    await set_role_attributes_from_sheet()

    await print_channel_attributes_to_sheet()


if __name__ == "__main__":

    client.run(TOKEN)
