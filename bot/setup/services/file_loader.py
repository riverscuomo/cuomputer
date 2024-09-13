from rich import print


def get_lines_from_file(filename):
    """Read lines from a given file and return them as a list."""
    print(f"Reading lines from {filename}")
    filepath = f"data/{filename}.txt"

    with open(filepath, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    return lines
