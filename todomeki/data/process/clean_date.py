import re
from datetime import datetime, timedelta


def convert_to_specific_format(date_string):
    # Function to parse relative date string to timedelta
    def parse_relative_date(relative_date_string):
        parts = re.findall(r"(\d+) (\w+)", relative_date_string)
        total_seconds = 0
        for value, unit in parts:
            if unit.startswith('day'):
                total_seconds += int(value) * 24 * 3600
            elif unit.startswith('hour'):
                total_seconds += int(value) * 3600
            elif unit.startswith('minute'):
                total_seconds += int(value) * 60
            elif unit.startswith('second'):
                total_seconds += int(value)
        return timedelta(seconds=total_seconds)

    patterns_to_try = [
        r"(\d{1,2}-\d{1,2}-\d{4})",
        r"(\d{1,2} \w{3})",  # days hours left
        r"(\d{1,2}/\d{1,2}/\d{4})",  # dd/mm/yyyy
        r"(\w{3} \d{1,2} \d{4})",  # Mon dd yyyy
        r"(\d{1,2} \w{3} \d{4})",  # dd Mon yyyy
        r"(\w{3} \d{1,2})",  # Mon dd
        r"(\d{4}-\d{1,2}-\d{1,2})",  # yyyy-mm-dd
        r"(\w+ \d{1,2}, \d{4})"  # Month dd, yyyy
    ]

    for pattern in patterns_to_try:
        match = re.search(pattern, date_string)
        if match:
            matched_date_string = match.group(1)
            try:
                # Check if the matched date is a relative date string
                if 'days' in date_string or 'hours' in date_string or 'minutes' in date_string or 'seconds' in date_string:
                    relative_timedelta = parse_relative_date(date_string)
                    absolute_date = datetime.now() + relative_timedelta

                elif pattern == r"(\d{4}-\d{1,2}-\d{1,2})":
                    absolute_date = datetime.strptime(matched_date_string, '%Y-%m-%d')

                else:
                    absolute_date = datetime.strptime(matched_date_string,
                                                      '%d-%m-%Y') if '-' in matched_date_string else datetime.strptime(
                        matched_date_string, '%B %d, %Y')

                # Check if the year is the current year
                if absolute_date.year == datetime.now().year:
                    formatted_date = absolute_date.strftime("%d/%m/%Y")
                else:
                    print("event past")
                    formatted_date = absolute_date.strftime("%d/%m/%Y")

                return formatted_date
            except ValueError:
                print(f"value error extracting date from: {date_string}")
                return None
            except Exception as e:
                print(f"failed extracting date from: {date_string}")
                print(e)

    return None