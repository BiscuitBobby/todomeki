from todomeki.secrets.dirs import json_dir
import datetime
import json


def get_events_within_month():
    try:
        with open(f'{json_dir}/data.json', 'r') as file:
            json_data = json.load(file)
            print(f"Reading '{'data.json'}'")
            
    except FileNotFoundError:
        # File does not exist, create an empty dictionary
        data = dict()
        print(f"'{'data.json'}' does not exist.")

        exit()

    current_date = datetime.date.today()

    events_within_month = {}

    for event, date_str in json_data.items():
        if date_str:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y").date()
            except ValueError:
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
                except ValueError:
                    try:
                        # Add a new try block for the date format with hyphens
                        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
                    except ValueError:
                        print(f"Skipping event '{event}' due to invalid date format: {date_str}")
                        continue

            # Check if the event date is in the current or next month
            if current_date <= date_obj <= current_date + datetime.timedelta(days=30):
                events_within_month[event] = date_obj.strftime("%B %d, %Y")
        else:
            return None

    return events_within_month


