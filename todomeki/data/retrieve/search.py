import requests
from todomeki.data.process.snap import snap


class SearchAgent:
    def __init__(self, api_key, cx, gl="in"):
        self.api_key = api_key
        self.cx = cx
        self.gl = gl

    def search(self, query):
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query,
            'gl': self.gl
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            results = response.json()
            return results
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Error:", err)

    def print_search_results(self, results):
        n = 0
        if results and 'items' in results:
            for i, item in enumerate(results['items'], 1):
                print(f"{i}. {item['title']}")
                print(f"   {item['link']}")
                print(f"   {item['snippet']}")
                snap(item['link'], n)
                n += 1
        else:
            print("No results found or an error occurred.")
