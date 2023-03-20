from datetime import datetime, timezone


async def is_request_for_server_time(message):
    today = datetime.now(timezone.utc)
    age = today - message.author.joined_at
    joined = max(age.days, 0)
    if message.content in [".svtime", ".svtime."]:
        await message.channel.send(
            f"{message.author.name}, you joined my server {joined} days ago."
        )
        return True
