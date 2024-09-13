from gspreader import get_sheet
from rich import print

# Global cache for the sheet data
_sheet_cache = None
_roles_sheet_data_cache = None
_roles_sheet_headers_cache = None


def load_roles_sheet():
    """Load roles from the Google Sheet, only once."""
    global _sheet_cache, _roles_sheet_data_cache, _roles_sheet_headers_cache

    if _sheet_cache is None:
        # Load the sheet data only if it's not cached
        print("Loading roles from Google Sheets for the first time...")
        _sheet_cache = get_sheet("Roles", "data")
        _roles_sheet_data_cache = _sheet_cache.get_all_records()
        _roles_sheet_headers_cache = [* _roles_sheet_data_cache[0]]
    else:
        print("Serving cached roles data.")

    return _sheet_cache, _roles_sheet_data_cache, _roles_sheet_headers_cache
