# safe_roles = [
#     "yes",
#     "Neighbor",
#     "@everyone",
#     "Server Booster",
#     "MEE6",
#     "Dyno",
#     "Cuomputer",
# ]
# # print(safe_roles)

# guild = await client.fetch_guild(GUILD_ID)
# # print(guild)
# i = 1
# async for member in guild.fetch_members(limit=3000):
#     print(i)
#     # print(i)
#     # print(member, member.roles)

#     # if type(member.roles != list):
#     #     continue

#     # print(type(member.roles))

#     for role in member.roles:
#         # print(type)

#         if role.name not in safe_roles:
#             print(role)
#             await member.remove_roles(role)

#     i += 1
