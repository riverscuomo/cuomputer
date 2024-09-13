
import logging
import re
import requests
from rich import print

logging.basicConfig(level=logging.INFO)


class WeezerpediaAPI:
    def __init__(self):
        self.base_url = "https://www.weezerpedia.com/w/api.php"

    # Perform a general text search on Weezerpedia
    def search_pages(self, search_query="Songs from the Black Hole"):
        # params_search = {
        #     "action": "query",
        #     "format": "json",
        #     "list": "search",  # Use search action
        #     "srsearch": search_query  # Search query
        # }

        params_search = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_query,
            "srwhat": "text",  # Could also try "title" or "nearmatch"
            "srlimit": 1,
            "srprop": "snippet|titlesnippet|redirecttitle"
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
    import re

    def preprocess_query(self, query):
        # Remove common stop words and punctuation
        stop_words = {
            'the',
            'with',
            'did',
            'songs',
            'song',
            'of',
            'from',
            'and',
            'in',
            'a',
            'an',
            'weezer',
        }
        # Simple tokenization and lowercasing
        tokens = re.findall(r'\b\w+\b', query.lower())
        # Remove stop words
        key_terms = [word for word in tokens if word not in stop_words]
        return ' '.join(key_terms)

    # Main method to get the knowledge to be used as context for GPT
    def get_search_result_knowledge(self, search_query="Songs from the Black Hole"):
        logging.info(f"Original query: {search_query}")

        # Step 1: Preprocess the query
        processed_query = self.preprocess_query(search_query)
        logging.info(f"Processed query: {processed_query}")

        # Step 2: Search with the processed query
        search_results = self.search_pages(processed_query)
        if self.has_search_results(search_results):
            logging.info("Found results with processed query.")
        else:
            logging.info(
                "No results with processed query. Trying original query.")
            # Step 3: Search with the original query
            search_results = self.search_pages(search_query)
            if not self.has_search_results(search_results):
                logging.info(
                    "No results with original query. Trying named entities.")
                # # Step 4: Extract named entities and search
                # entities_query = extract_named_entities(search_query)
                # logging.debug(f"Named entities extracted: {entities_query}")
                # if entities_query:
                #     search_results = self.search_pages(entities_query)

        if not self.has_search_results(search_results):
            logging.info(
                f"No detailed information found for '{search_query}'.")
            return None

        # Proceed with fetching the first result
        first_result = search_results['query']['search'][0]
        title = first_result['title']
        logging.info(f"Fetching content for page title: {title}")

        # Fetch full content
        full_content = self.fetch_page_content(title)

        # Prepare the knowledge context text
        knowledge_text = f"Background information about '{title}':\n\n"
        knowledge_text += f"{full_content[:1000]}"

        logging.info(f"Knowledge text: {knowledge_text}")

        return knowledge_text

    def has_search_results(self, search_results):
        return (
            search_results and
            'query' in search_results and
            'search' in search_results['query'] and
            search_results['query']['search']
        )


def test():
    # Create an instance of the WeezerpediaAPI class
    # wiki_api = WeezerpediaAPI()

    # # Call the methods to fetch page information and content
    # wiki_api.fetch_page_info()
    # wiki_api.fetch_page_content()

    api = WeezerpediaAPI()
    knowledge = api.get_search_result_knowledge(
        "Ecce Homo in the Weezer context")
    print(knowledge)


if __name__ == "__main__":
    test()
