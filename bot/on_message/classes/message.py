from datetime import datetime, timedelta
import random
import discord
from bot.setup.init import tz

# define a custom class called Message that takes in a discord.Message and adds some attributes to it
class Message(discord.Message):
    
    #initialize the class 
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
        self.is_newbie = datetime.now(tz) - self.author.joined_at  < timedelta(days= 7)
        self.is_question = self.content[-1]=='?'
        self.mentions_rivers = 'rivers' in self.content.lower()
        self.firestore_user = None
        self.id_of_user_being_replied_to = None
        self.user_score = 0# firestore_user["score"]          
        self.mentions_cuomputer = None
        self.test_message = None
        self.nick = None
        self.language_code = None
        self.author_roles = None

    def log(self):
        print(f"die_roll={ round(self.die_roll, 3)} user_score={self.user_score}, language_code={self.language_code}, is_newbie={self.is_newbie}, is_question={self.is_question}, mentions_rivers={self.mentions_rivers}, mentions_cuomputer={self.mentions_cuomputer}")

