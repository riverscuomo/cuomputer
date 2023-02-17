from datetime import datetime, timezone


async def is_request_for_server_time(message, member):
    today = datetime.now(timezone.utc)
    age = today - member.joined_at
    joined = max(age.days, 0)
    if message.content in [".svtime", ".svtime."]:
        await message.channel.send(
            f"{member.name}, you joined my server {joined} days ago."
        )
        return True
