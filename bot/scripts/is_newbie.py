from config import num_roles_for_newbie


def is_newbie(author):
    return len(author.roles) <= num_roles_for_newbie
