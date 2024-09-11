
import requests
from rich import print


class WeezerpediaAPI:
    def __init__(self):
        self.base_url = "https://www.weezerpedia.com/w/api.php"

    # Perform a general text search on Weezerpedia
    def search_pages(self, search_query="Songs from the Black Hole"):
        params_search = {
            "action": "query",
            "format": "json",
            "list": "search",  # Use search action
            "srsearch": search_query  # Search query
        }

        response_search = requests.get(self.base_url, params=params_search)
        if response_search.status_code == 200:
            search_results = response_search.json()
            return search_results
        else:
            print("Error fetching search results:",
                  response_search.status_code, response_search.text)
            return None

    # Fetch the full page content for a given title
    def fetch_page_content(self, title):
        params_full = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "revisions",
            "rvprop": "content"
        }
        response_full = requests.get(self.base_url, params=params_full)
        if response_full.status_code == 200:
            query = response_full.json()['query']
            pages = query['pages']
            page = pages[list(pages.keys())[0]]
            if 'revisions' in page:
                revisions = page['revisions']
                content = revisions[0]['*']
                return content
            else:
                return "No content available for this page."
        else:
            print("Error fetching page content:",
                  response_full.status_code, response_full.text)
            return None

    # Main method to get the knowledge to be used as context for GPT
    def get_search_result_knowledge(self, search_query="Songs from the Black Hole"):
        # Step 1: Perform a search based on the query
        search_results = self.search_pages(search_query)

        if search_results and 'query' in search_results and 'search' in search_results['query']:
            # Get the first search result
            first_result = search_results['query']['search'][0]
            title = first_result['title']

            # Step 2: Fetch full content for the first matching result
            full_content = self.fetch_page_content(title)

            # Step 3: Prepare the knowledge context text
            knowledge_text = f"Background information about '{title}':\n\n"
            # Truncate to 1000 chars for brevity
            knowledge_text += f"{full_content[:1000]}"

            return knowledge_text
        else:
            return f"No detailed information found for '{search_query}'."


def test():
    # Create an instance of the WeezerpediaAPI class
    wiki_api = WeezerpediaAPI()

    # Call the methods to fetch page information and content
    wiki_api.fetch_page_info()
    wiki_api.fetch_page_content()


if __name__ == "__main__":
    test()
