from todomeki.data.process.clean_date import convert_to_specific_format
from todomeki.data.process.relavent_scrape import similar_search_scrape
from todomeki.secrets.dirs import img_dir
from pathlib import Path
import datetime
import builtins

def date_from_img(image, model, vision_model):
    # Validate that an image is present
    if not (img := Path(f"{img_dir}{image}")).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/png",
            "data": Path(f"{img_dir}{image}").read_bytes()
        },
    ]

    if builtins.siteurl:
        vision_prompt_parts = [
            f"here are some snippets from the website:{similar_search_scrape(builtins.siteurl)}\n\nExtract the date for the next event from the attached image (present year is {datetime.date.today():%Y})) in the format days, hours, minutes, seconds or extract the date for the next event from the image in the format day-month-year",
            image_parts[0],
            "\n",
        ]
    else:
        print('no data scraped from website')
        vision_prompt_parts = [
            f"\n\nExtract the date for the next event from the attached image (present date is {datetime.date.today():%d/%m/%Y})) in the format days, hours, or extract the date for the next event from the image in the format day-month-year",
            image_parts[0],
            "\n",
        ]

    print("extracting data from image")
    response = vision_model.generate_content(vision_prompt_parts)

    print(f"date extracted from image:\n{response.text}")
    formatted_date = convert_to_specific_format(response.text)

    return formatted_date
