from config import channels
from rich import print


def init_openai_sessions():
    """Initialize OpenAI sessions for each configured channel."""
    openai_sessions = {id: [] for channel_name, id in channels.items()}
    print(f"openai_sessions={openai_sessions}")
    return openai_sessions

# Test function for module


def _test():
    openai_sessions = init_openai_sessions()
    print(openai_sessions)


if __name__ == "__main__":
    _test()
