try:
    from Screenshot import Screenshot
except Exception as e:
    print("Install package selenium-screenshot, try 'pip install selenium-screenshot' ")
    raise Exception(e)

from selenium.webdriver.chrome.options import Options
from todomeki.secrets.dirs import img_dir
from selenium import webdriver


def snap(url='https://google.com', img_name="0"):
    ob = Screenshot.Screenshot()

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # needed for headless mode on some systems

    # Create a headless Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    img_url = ob.full_screenshot(driver, save_path=img_dir, image_name=f'{img_name}.png',
                                 is_load_at_runtime=True,
                                 load_wait_time=1)
    print(img_url)

    driver.quit()
    return f'{img_name}.png'
