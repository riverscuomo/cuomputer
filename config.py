from datetime import datetime
import os
from dotenv import load_dotenv
import pytz

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN = os.environ.get("TOKEN")

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
import os
import json

import os
import json

# Check if we're running on Heroku with JSON credentials
if 'GOOGLE_CREDENTIALS' in os.environ:
    # Heroku environment - use the JSON config var
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_path = '/tmp/google-credentials.json'
    
    # Write the credentials to a temporary file
    with open(creds_path, 'w') as f:
        f.write(creds_json)
    
    # Set the environment variable to point to this file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
    print(f"Using Heroku credentials configuration")
    
else:
    # Local environment - use the file path approach
    creds_path = os.path.join(os.environ.get("CRED_PATH", ""), "rivers-public-service-account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    print(f"Using local credentials file at: {creds_path}")

print('the creds path is', creds_path)    

# Add verification for Firestore connection
try:
    from google.cloud import firestore
    db = firestore.Client()
    print(f"Successfully initialized Firestore client for project: {db.project}")
except Exception as e:
    print(f"ERROR connecting to Firestore: {str(e)}")

    
GOOGLE_DRIVE_CREDFILE = os.environ.get("GOOGLE_DRIVE_CREDFILE")
VOICE_API_KEY = os.environ.get("VOICE_API_KEY")

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


tz = pytz.timezone('America/Los_Angeles')

# testing = False

OAUTH2_URL = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&scope=bot"
OAUTH2_URL = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&redirect_uri=https%3A%2F%2Frcwebserver.herokuapp.com%2F&response_type=code&scope=bot%20activities.write%20activities.read%20relationships.read%20applications.entitlements%20applications.store.update%20applications.commands%20applications.builds.read%20rpc.voice.read%20rpc.voice.write%20rpc.activities.write%20webhook.incoming%20messages.read%20applications.builds.upload%20identify%20email%20connections%20guilds%20guilds.join%20gdm.join%20rpc%20rpc.notifications.read"
GENERAL_ID = 890292832198344724
GUILD_ID = 890210072381247548

# Different possible wait periods for the neighbor role assignment (values in hours)
neighbor_role_waiting_period_options = {
    "instant": 0,            # 0 hours = immediate role assignment
    "delayed24": 1 * 24 * 1  # 24 hours = 1 day waiting period
}

# Set the waiting period (in hours) by changing to the appropriate neighbor_role_waiting_period_options key 
neighbor_role_waiting_period = neighbor_role_waiting_period_options["instant"] 

image_threshold = 2  # user_score
gpt_threshold = 4  # user_score
num_roles_for_newbie = 1

sessions = []

short_name = "Rivers"
long_name = "Rivers Cuomo"
""" Channels """
channels = {
    "artists": 913828394888736799,
    "coach": 903672810277318666,
    "dan": 892599614191063071,
    "foodies": 906963583567560804,
    "gamers": 908704398325207120,
    "geezerville": 901827523279749230,
    "memes": 998236631511347271,
    "movies-tv-books": 1164041947976048660,
    "music": 938551407093620776,
    "musicians": 901547467298975784,
    "qna": 895330177456963645,
    "welcome": 1022159784528597023,
    "general": 892873789262680164,
    "based": 1023211668949438504,
    "japanese": 930818686686724146,
    "korean": 894614202315051101,
    "pink": 893943182507782154,
    "sarah": 1187565432161439877,
    "spanish": 892197175776383000,
    "tiktok": 928747669361418270,
    "vangie": 892536534186745907,
    "connect": 908388613786570782,
    "shrine": 909450021353705533,
    "zoo": 908369813389324378,

    # VOICE
    "rctalk": 892514465923366954,
    "rcmusic": 910331814697107466,
    "vangiesvc": 1046958343308193842,
    "lounge": 890210073308172347,
    "lounge2": 1059229073466998854,
    "jamroom": 890210073308172348,
}

# all_response_channels = []


qna = "❔-questions-and-help"
general = "🌟-general"

# only respond to messages posted in these channels
library_response_channels = [
    general,
    qna,
    # "ask-rivers",
    "espanol",
]
coach_response_channels = ["aunt-vangie", "coach-cuomo"]
rivers_response_channels = [general, qna]
q_and_a_channels = [qna, general, "espanol"]
spanish_channels = ["espanol"]
japanese_channels = ["日本"]
korean_channels = ["한국어"]
foreign_channels = spanish_channels + japanese_channels + korean_channels
standard_reponse_channels = foreign_channels + [
    general,
]

always_respond_channels = ["coach-cuomo"]

all_response_channels = list(
    set(
        q_and_a_channels
        + library_response_channels
        + coach_response_channels
        + rivers_response_channels
        + foreign_channels
    )
)


""" Members """
user_to_remove = None
everyone = 890210072381247548

rivers_id = 734902900257718355  # ????
cuomputer_id = (
    890946668940361778  # this is the bot that posts the messages on your behalf
)

riverbot_id = cuomputer_id
dyno_id = 155149108183695360
another_rivers_server_id = 895330177456963645  # announcement channel?
server_publish_message_id = 903799822350422138
fm_bot = 356268235697553409
carlbot = 235148962103951360

# skip all the message processing for simple bots that are just removing posts or slash commands posts
members_to_skip = [
    carlbot,
    rivers_id,
    cuomputer_id,
    another_rivers_server_id,
    dyno_id,
    server_publish_message_id,
    fm_bot,
]

""" Roles """
cuomputer_role_id = 890953816667729950
mee6_role_id = 892442873801367565
dyno_role_id = 890234650381918219
server_booster_role_id = 890283397753213010
stan_role_id = 1036300448052818051

skipper_role_ids = [
    dyno_role_id,
    server_booster_role_id,
    everyone,
    cuomputer_role_id,
    mee6_role_id,
]

srs_role_id = 891296798319190056


testing = True
# If testing,  don't skip the message processing for your posts/
if testing:
    members_to_skip.remove(rivers_id)


""" MESSAGES """
negativity_threshold = -0.4 # -0.6
never_respond = 10  # t has to be higher
threshold_for_not_mentioning_rivers = 97  # if no 'river', t has to be higher
threshold_for_non_questions = 97  # if no '?', t has to be higher
always_respond = 99

firestore_time_format = "%a, %d %b %Y %H:%M:%S %Z"
og_cutoff = datetime(2021, 9, 19)

bundles_map = {
    "30": "White",
    "34": "Ewbaite",
    "35": "Pre-Weezer",
    "36": "Blue-Pinkerton",
    "37": "Black Room",
    "38": "Green",
    "39": "Maladroit",
    "40": "Red-Raditude-Hurley",
    "42": "Make Believe",
    "45": "Patrick & Rivers",
    "48": "Weezma",
    "bu0QgWG8ILJw7afdqkvp": "Pac Black",
    "Xuq6DptPbiXebElzip99": "The Black Album",
    "CZnb2XGfNUSPYA5izsg1": "OK Human",
    "qki8QLSg7m8W6yVyD1OO": "Van Weezer",
    "K8B5vBaQJnck9aoSAZ1b": "SZNZ",
}

# # OHHHHHHHHHHHHHH!!!!!!
# # None of these can have the same key (1 or 1*1)
# time_based_roles = {
#     1: "Visitor",
#     1 * .9: "Neighbor",
# }


""" for dialogflow """
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
language_code = "en-us"

# Colors
discord_background_color = "36393F"
default_color = "fafafa"

""" Drive Folders """
green_nft_folder_id = "1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY"
cryptographer_folder_id = "1B3ZjiZ2BB-ZqbnUpwqJGtKfvBAwZ0H11"
mr_rivers_neighborhood_folder_id = "0ALAAAi81yQw3Uk9PVA"


""" Outgoing Messages """
service_message = """

If you find yourself stressed or overwhelmed by requests from me or others, feel free to ignore us. 
Service should be fun (most of the time). Family, work, school, and you are more important.
"""
