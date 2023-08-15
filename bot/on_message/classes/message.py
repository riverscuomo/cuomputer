from datetime import datetime, timedelta
import random
import discord
from bot.setup.init import tz


class Message(discord.Message):
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
    message: str
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
    language_code: str
        The language code of the Message.
    author_roles: list
        The roles of the author of the Message.
    """

    def __init__(self, message):
        self.id = message.id
        self.type = message.type
        self.flags = message.flags
        self.message = message
        self.content = message.content
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
        self.is_question = self.content[-1] == '?'
        self.mentions_rivers = 'rivers' in self.content.lower()
        self.firestore_user = None
        self.id_of_user_being_replied_to = None
        self.user_score = 0  # firestore_user["score"]
        self.mentions_cuomputer = None
        self.test_message = None
        self.nick = None
        self.language_code = None
        self.author_roles = None

    def log(self):
        print(f"die_roll={ round(self.die_roll, 3)} user_score={self.user_score}, language_code={self.language_code}, is_newbie={self.is_newbie}, is_question={self.is_question}, mentions_rivers={self.mentions_rivers}, mentions_cuomputer={self.mentions_cuomputer}")
