import requests
import dotenv
import os

from snap import snap

dotenv.load_dotenv()

def google_search(api_key, cx, query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'gl':gl
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

def print_search_results(results):
    n = 0
    if results and 'items' in results:
        for i, item in enumerate(results['items'], 1):
            print(f"{i}. {item['title']}")
            print(f"   {item['link']}")
            print(f"   {item['snippet']}")
            snap(item['link'], n)
            n+=1
    else:
        print("No results found or an error occurred.")

api_key = os.getenv('search_key')
cx = os.getenv('engine_id')  # custom search engine id
gl = "in"

query = input("Enter your search query: ")
results = google_search(api_key, cx, query)

print("\nSearch Results:")
print_search_results(results)
