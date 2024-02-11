from todomeki.data.retrieve.close_events import get_events_within_month
from todomeki.data.retrieve.search import SearchAgent
from todomeki.data.retrieve.track import EventTracker
from todomeki.secrets.keys import ConfigSecrets
class Watcher:
    def __init__(self, api_key, cx, gl):
        self.config = ConfigSecrets(api_key, cx, gl)

        self._search_engine = SearchAgent(self.config.api_key, self.config.cx, self.config.gl)
        print("initialized search engine")
        self._tracker = EventTracker(self._search_engine)
        print("initialized tracker")

    def track_event(self, query):
        self._tracker.track(query)

    def nearing_events(self):
        result = get_events_within_month()
        print(result)
        return result

    def manually_add_event(self, event_name, event_date):
        self._tracker.manually_add_event(event_name, event_date)
        print(f"added event: {event_name}: {event_date}")

    def remove_event(self, event_name):
        try:
            self._tracker.remove_event(event_name)
        except Exception as e:
            print("failed to remove event")
            return e
