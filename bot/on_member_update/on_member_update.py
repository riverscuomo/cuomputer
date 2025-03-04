from firebase_admin import firestore
from bot.db.fbdb import get_firestore_db
from bot.setup.services.roles_sheet import load_roles_sheet
from config import members_to_skip, service_message, GUILD_ID
from rich import print
from bot.setup.discord_bot import (
    client,

)
from bot.scripts.add_roles import get_firestore_user_by_id
from bot.setup.services.google_services import get_google_drive_service
import sys

from gspreader import get_sheet

sys.path.append("...")  # Adds higher directory to python modules path.


@client.event
async def on_member_update(before, after):
    """
    When you add or remove a role to a discord user,
    sync the change to the firestore user database.
    """
    # return

    # if message.guild is None or message.guild.id != GUILD_ID:
    #     # print("wrong guild")
    #     return
    # print(before, after)
    if before.id in members_to_skip:
        # print(f"skipping <{member_name} {member.id}>")
        return

    added_role = None
    removed_role = None

    # If you've just given them a new role
    if len(after.roles) > len(before.roles):
        added_role = [x.name for x in after.roles if x not in before.roles][0]
        print(f"added_role: {added_role}")

    # If you've just taken away one of their roles
    elif len(before.roles) > len(after.roles):
        removed_role = [
            x.name for x in before.roles if x not in after.roles][0]
        print(f"removed_role: {removed_role}")

    else:
        return

    # Query for just this user instead of fetching all users
    firestore_user = get_firestore_user_by_id(before.id)
    
    if firestore_user:
        roles_sheet_data = load_roles_sheet()

        # Get the matching role row from the roles sheet data
        role_object = next(
            (
                row
                for row in roles_sheet_data
                if row["role"] in [added_role, removed_role]
                and "folder_id" in row
            ),
            None,
        )

        db = get_firestore_db()

        # gET actual firestore record
        user = db.collection("users").where(
            "discordId", "==", str(before.id)).get()[0]

        email = firestore_user["email"]
        print("email", email)

        if added_role:

            message = f"You've been given the {added_role} role on my server."

            user.reference.update(
                {"badges": firestore.ArrayUnion([added_role])})

            if _is_valid_email(email):

                response = add_drive_access_to_role(
                    added_role, email, role_object)

                if response != "success":
                    message += f"\n\n{response}"

                if added_role == "Android":
                    additional_add_android_role_tasks(email, "Android")

                elif added_role == "iPhone":
                    additional_add_android_role_tasks(email, "iPhone")

                message = f"{message}"

                # print(message)

                if len(role_object["description"]) > 0:
                    message = message + "\n\n" + role_object["description"]

                if role_object["type"] in ["1. service", "4.5: role-assigner"]:
                    message = message + "\n\n" + service_message

                # if "type" in role
                channel = await after.create_dm()

                await channel.send(message)

        elif removed_role:

            # message = f"You've been removed from the {removed_role} role on my server."

            user.reference.update(
                {"badges": firestore.ArrayRemove([removed_role])})

            if _is_valid_email(email):

                remove_drive_access_for_role(added_role, email, role_object)

                # if removed_role == "Android":
                #     additional_message = remove_android_role(email, "Android")
                # if removed_role == "iPhone":
                #     additional_message = remove_android_role(email, "iPhone")

    else:
        print(f"There is no firestore_user for {before.name}")


def _is_valid_email(email: str):
    if not email or len(email) < 5 or "@" not in email:
        print(email, " is not a valid email.")
        return False
    return True


def additional_add_android_role_tasks(email: str, testers_sheet: str):
    """adds their email address to the android tester file. then you have to manually copy and paste to android developer console."""

    print(f"adding {email} to {testers_sheet} file.")

    testers_sheet = get_sheet("Testers", testers_sheet)
    testers = testers_sheet.get_values("A1")[0][0]
    # print(testers)
    testers = f"{testers}, {email}"
    testers_sheet.update("A1", testers)

    app_download_url = get_app_download_url(testers_sheet)

    return " You'll soon be added to the {testers_sheet} app testing group. You'll be able to download the app here: {app_download_url} . Maybe?"


def get_app_download_url(testers_sheet: str):
    """
    Gets the app download url for the given platfolrm.
    """
    if testers_sheet == "Android":
        return "https://play.google.com/apps/internaltest/4700435423750588325"
    elif testers_sheet == "iPhone":
        return "Test Flight app in the App Store"


def remove_android_role(email: str, testers_sheet: str):
    """removes their email address from the android tester file. then you have to manually copy and paste to android developer console."""
    print(f"removing {email} from {testers_sheet} sheet.")

    testers_sheet = get_sheet("Testers", testers_sheet)
    testers = testers_sheet.get_values("A1")[0][0]
    print(testers)
    testers = testers.replace(f", {email}", "").strip()
    testers_sheet.update("A1", testers)

    return " You'll soon be removed from the {testers_sheet} app testing group."


def remove_drive_access_for_role(added_role, email, role_object=None):
    """Does nothing if there is not role for drive access for this role"""

    if role_object and role_object["folder_id"]:
        role = role_object["role"]

        print(f"Removing {role} folder for {email}")

        drive_service = get_google_drive_service()

        print(f"Getting existing permissions on {role} folder ")
        all_permissions = (
            drive_service.permissions()
            .list(
                supportsAllDrives=True,
                fileId=role_object["folder_id"],
                fields="permissions/id, permissions/emailAddress",
            )
            .execute()
        )["permissions"]
        print(all_permissions)

        permission_id = next(
            x["id"] for x in all_permissions if x["emailAddress"] == email
        )
        print(permission_id)

        response = (
            drive_service.permissions()
            .delete(
                supportsAllDrives=True,
                permissionId=permission_id,
                fileId=role_object["folder_id"],
            )
            .execute()
        )
        print(response)


def add_drive_access_to_role(added_role, email, role_object=None):
    """
    For: Artist, Cryptographer, Camp counselor, TikTok.
    Does nothing if there is not rule for drive access for this role.
    Returns a string "success" or a string reason for failure.
    """

    if role_object and role_object["folder_id"]:
        role = role_object["role"]

        if role_object["google_drive_role"] == "":
            google_drive_role = "commenter"
        else:
            google_drive_role = role_object["google_drive_role"]

        print(f"Sharing {role} folder {google_drive_role} with {email}")

        drive_service = get_google_drive_service()

        # https://developers.google.com/drive/api/v3/reference/permissions/create
        try:
            response = (
                drive_service.permissions()
                .create(
                    body={
                        "role": google_drive_role,
                        # "role": "fileOrganizer",
                        "type": "user",
                        "emailAddress": email,
                        "useDomainAdminAccess": True,
                    },
                    sendNotificationEmail=True,
                    supportsAllDrives=True,
                    fileId=role_object["folder_id"],

                    emailMessage=role_object["google_drive_add_message"],
                )
                .execute()
            )
            return "success"
        except Exception as e:
            print(e)

            return str(e)

        # print(response)
