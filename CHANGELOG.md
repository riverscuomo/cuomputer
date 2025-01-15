# Changelog

## 1.3.0 (2025-01-15)

Changed python buildpack to use .python-version file.
Testing automatic deployment to Heroku.

## 1.2.0

- updated openai

## v0.1.2 (2023-07-19)

updated openai and discord2
switched from arthur to default replicate model

## v0.1.1

(2023-05-12)
skip forbidden on Fridays

(2023-05-03)

- fix googlebot(message) for qna channel

(2023-04-28)

- added fetch_and_print_messages() to get messages from a channel and print them to console

(2023-03-19)

- extended Message class
- did much work to integrate gpt4 into many channels
- restore openai_session context for the gpt response. this will probably be too expensive and I'll have to reduce access
- upgraded to discord.py 2.2.2 to get rid of the thread error on startup but I had to get rid of some of the slash commands (that no one was using).

(2023-03-12)

- moved neighbor threshold to config
- bumped neighbor threshold to 2 days

(2023-02-05)

### Feature

- added Arthurs replicate model for Rivers images

## v0.1.0 (2023-01-02)

### Feature

- added google tts for foreign languages

### Fix

- switched to rivertils 1.7 with google translate

### Tests

-

## v0.1.0 ()

1.1
refactored replicate request.
clearer print statements so i can make sure it's working properly.
bot now responds with a text message first, with requester name and prompt.
also, noticed that replicate requests included 'show me' so removed that.

1.0.2
refactored on message.
is_message_from_other_guild() now returns a boolean.
delete message based in genreal if image

1.0.1
removed visitor role from neighbors

Added await bad_guild.leave() to on message

Unchecked public bot here:
<https://discord.com/developers/applications/890946668940361778/bot>

Ok I've successfully migrated to
<https://github.com/Pycord-Development/pycord>
pycord (discord2) is a fork of discord.py that is actively maintained.
It still has traditional bot messages.
