from datetime import datetime, timedelta
import random
import discord
from config import short_name, tz


class CustomMessage(discord.Message):
    """
    This class represents a Message on Discord. This class is derived from discord.Message.

    Attributes
    ----------
    id : int
        The ID of the Message.
    type : MessageType
        The type of Message. 
    flags: MessageFlags
        The flags of the Message.
    message: discord.Message
        The Message.
    attachments: list
        The attachments of the Message.
    content: str
        The content of the Message.
    author: Member
        The author of the Message.
    channel: TextChannel, VoiceChannel, CategoryChannel, DMChannel
        The channel of the Message.
    guild: Guild
        The Guild of the Message.
    now: datetime
        Current time when the Message is created.
    raw_mentions: list
        Contains the raw mentions in the Message.
    raw_role_mentions: list
        Contains the raw role mentions in the Message.
    raw_channel_mentions: list
        Contains the raw channel mentions in the Message.
    reference: MessageReference
        The reference to another Message.
    die_roll: float
        A random float between 0 and 1.
    is_newbie: boolean
        If the author of the Message has joined less than 7 days.
    is_question: boolean
        If the content of the Message ends with '?' character.
    mentions_rivers: boolean
        If 'rivers' is mentioned in the content of the Message.
    firestore_user: User
        The Firestore user.
    id_of_user_being_replied_to: int
        The ID of the user being replied to.
    user_score: int
        The score of the user.
    mentions_cuomputer: boolean
        If 'cuomputer' is mentioned in the content of the Message.
    test_message: str
        A test message.
    nick: str
        The nickname of the author of Message.
    author_roles: list
        The roles of the author of the Message.
    """

    def __init__(self, message: discord.Message):
        self.message = message
        self.id = message.id
        self.type = message.type
        self.flags = message.flags
        self.content = message.content
        self.attachments = message.attachments
        self.author = message.author
        self.channel = message.channel
        self.guild = message.guild
        self.now = datetime.now(tz)
        self.raw_mentions = message.raw_mentions
        self.raw_role_mentions = message.raw_role_mentions
        self.raw_channel_mentions = message.raw_channel_mentions
        self.reference = message.reference

        # a variable which holds a random float between 0 and 1
        self.die_roll = random.random()
        self.is_newbie = datetime.now(
            tz) - self.author.joined_at < timedelta(days=7)
        self.is_question = len(self.content) > 0 and self.content[-1] == '?'
        self.mentions_rivers = short_name in self.content.lower(
        ) or 'rivers' in self.content.lower() or 'patrick' in self.content.lower()
        self.firestore_user = None
        self.id_of_user_being_replied_to = None
        self.user_score = 0
        self.mentions_cuomputer = None
        self.mentions_guest_bot = None
        self.test_message = None
        self.nick = None
        self.author_roles = None
        self.gpt_system = None
        self.mentions_the_bot_who_is_responding = False
        self.mentions_someone_else = False
        self.is_intended_for_someone_else = True

    def log(self):
        print(f"user_score={self.user_score}, die_roll={ round(self.die_roll, 3)}, is_newbie={self.is_newbie}, is_question={self.is_question}, mentions_rivers={self.mentions_rivers}, mentions_cuomputer={self.mentions_cuomputer}, mentions_guest_bot={self.mentions_guest_bot}")
