import re

from bot.setup.init import demoji


async def fix_nick(member):

    """
    for non-firestore-users, this fixes up their discord nick
    """

    # NICKNAME
    try:
        # print(member)
        nick = member.nick
        if nick is None:
            nick = member.name

        #     if "🌲" in nick:
        #         nick = "Tree"

        #     nick = nick.replace("🎸", "")

        try:
            # print(nick)
            # nick = nick.replace("🌲", "Tree")
            # print(nick)
            # print(len(nick))
            # print(nick, "!!!!")
            # nick = re.sub(r'[^a-zA-Z]', "", str(nick))
            # nick = nick.replace("ZibbityBop", "John")
            nick = nick.split("#")[0]  # .split(" ")[0]
            # replace everything that's not a-z?
            nick = re.sub(r"[^a-zA-Z]", "", str(nick))
            # nick = demoji.replace(nick, "")
            # if "🌲" in nick:
            #     nick = "Tree"
            # print(nick)
            # nick = nick.replace("🌲", "Tree")
            # print(nick)
            # print(len(nick))
            try:
                await member.edit(nick=nick)
            except Exception as e:
                # print("couldn't do member.edit(nick=nick)")
                # print(e)
                return nick
            return nick

        except Exception as e:
            print(e)

            return nick
    except Exception as e:
        print(e)
        return nick
