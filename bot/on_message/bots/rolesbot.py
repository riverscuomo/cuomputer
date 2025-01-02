from bot.setup.services.roles_sheet import load_roles_sheet
from bot.scripts.message.finalize_response import finalize_response
import sys
from better_profanity import profanity

sys.path.append("...")  # Adds higher directory to python modules path.

role_info_link = "\n\nInformation about all the roles can be found here: <https://docs.google.com/spreadsheets/d/1K51AJScqeqiGJquOdaHncgFe0UQUEvRCg0QnqeJQxHA>"


async def post_roles_response(
    message
):
    """
    Returns role description and earned by from the sheet if "role" in test_message and "how" in test_message
    """
    test_message = message.test_message.lower()
    print(f"post_roles_response {test_message}")
    if "role" in test_message and (
        "how" in test_message or "what" in test_message or "when" in test_message
    ):

        sheet, data, headers = load_roles_sheet()

        try:
            row = next(x for x in data if x["role"].lower() in test_message)

            response = ""
            if row["description"] != "":
                response += (
                    f"The {row['role']} role is for someone who {row['description']}"
                )
            if row["earned by"] != "":
                response += (
                    f" You can get the '{row['role']}' role by {row['earned by']}"
                )
            response += role_info_link

            response = finalize_response(
                response, message.nick)

            message = await message.channel.send(response)
            # print(message)

            await message.edit(embed=None)

        except:

            print(f"no role found in {test_message}")

            response = (
                f"Which role in particular were you curious about?{role_info_link}"
            )

            response = finalize_response(
                response, message.nick)

            message = await message.channel.send(response)

        return True

    else:
        print("No response from rolesbot.")
        return False
