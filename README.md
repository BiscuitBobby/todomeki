Don't miss approaching events and opportunities again.
Scrape online results for upcoming events and track them.

Example code:
```
import dotenv
import os
from todomeki import Watcher

dotenv.load_dotenv()

# set up Watcher with google api key for gemini and programmable search engine (api_key),
# search engine id (cx) and location (gl) "us", "uk", "au", "cn", "in", etc
watcher = Watcher(api_key=os.getenv('search_key'), cx=os.getenv('engine_id'), gl="gb")

# search for event
query = input("Enter your search query: ")
watcher.track_event(query)

# return upcoming events in 30 day range
watcher.nearing_events()

# manually add event
watcher.manually_add_event('BiscuitBobby workshop', '12/2/2024')

# remove event
watcher.remove_event('BiscuitBobby workshop')

```
