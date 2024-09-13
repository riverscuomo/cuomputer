import demoji
from rich import print


def initialize_demoji():
    """Initialize demoji for emoji handling"""
    if not demoji.last_downloaded_timestamp():
        demoji.download_codes()
        print("Demoji codes downloaded.")


initialize_demoji()
