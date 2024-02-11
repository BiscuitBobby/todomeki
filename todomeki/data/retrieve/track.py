from todomeki.data.process.date_from_screenshot import date_from_img
from todomeki.models.vision import GeminiProVision
from todomeki.data.process.snap import snap
from todomeki.secrets.dirs import json_dir
from todomeki.models.llm import GeminiPro
import threading
import traceback
import builtins
import json

builtins.siteurl = None
output_dates = dict()

try:
    with open(f'{json_dir}/data.json', 'r') as json_file:
        data = json.load(json_file)
        print(f"Reading '{f'{json_dir}/data.json'}'")

except FileNotFoundError:
    data = dict()
    print(f"'{'data.json'}' does not exist, new file will be created.")

except json.JSONDecodeError:
    data = dict()
    print(f"'{'data.json'}' is empty or an invalid JSON")

except Exception as e:
    print(f"An error occurred getting JSON: {e}")
    traceback.print_exc()

lock = threading.Lock()


class EventTracker:
    def __init__(self, search_engine):
        self.search_engine = search_engine
        self.data = data
        self.vision_model = GeminiProVision(search_engine.api_key).model
        self.llm_model = GeminiPro(search_engine.api_key).model

    def process_date(self, image):
        global output_dates
        date = date_from_img(image, self.llm_model, self.vision_model)

        with lock:
            if date not in output_dates:
                output_dates[date] = 1
            else:
                output_dates[date] += 1

    def double_check(self, image):
        global output_dates
        threads = []

        for i in range(2):
            thread = threading.Thread(target=self.process_date, args=(image,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if not output_dates:
            return None

        max_frequency = max(output_dates.values())
        max_dates = [key for key, value in output_dates.items() if value == max_frequency]

        if len(max_dates) > 1:
            return self.double_check(image)
        else:
            return max_dates[0]

    def track(self, event):
        results = self.search_engine.search(event)
        title = event
        link = results['items'][0]['link']
        print(link)
        image = snap(url=link, img_name='test')
        builtins.siteurl = link  # used in check if

        date = self.double_check(image)
        print(f"{event} -> {date}")
        self.data[title] = date

        try:
            with open(f'{json_dir}/data.json', 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
            print("Writing into 'data.json'.")
        except FileNotFoundError:
            with open(f'{json_dir}/data.json', 'x') as json_file:
                json.dump(self.data, json_file, indent=4)
            print("Created new Json file.")
        except Exception as e:
            print(f"An error occurred storing Json: {e}")

        return {"event": date}

    def remove_event(self, event_title):
        try:
            with lock:
                if event_title in data:
                    del data[event_title]
                    with open(f'{json_dir}/data.json', 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                    print(f"Removed '{event_title}' from 'data.json'.")
                    return {"message": f"Event '{event_title}' removed successfully."}
                else:
                    print(f"Event '{event_title}' not found in 'data.json'.")
                    return {"error": f"Event '{event_title}' not found in 'data.json'."}
        except Exception as e:
            print(f"An error occurred removing event from JSON: {e}")
            return {"error": f"An error occurred removing event from JSON: {e}"}

    def manually_add_event(self, event_title, event_date):
        try:
            with lock:
                data[event_title] = event_date
                with open(f'{json_dir}/data.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"Manually added '{event_title}' with date '{event_date}' to 'data.json'.")
                return {"message": f"Event '{event_title}' added successfully with date '{event_date}'."}
        except Exception as e:
            print(f"An error occurred manually adding event to JSON: {e}")
            return {"error": f"An error occurred manually adding event to JSON: {e}"}

