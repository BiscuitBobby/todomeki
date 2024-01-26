from Screenshot import Screenshot
from selenium import webdriver

def snap(url = 'http://www.w3schools.com/js/default.asp',img_name ="img.png"):
    ob = Screenshot.Screenshot()
    driver = webdriver.Chrome()

    driver.get(url)
    img_url = ob.full_screenshot(driver, save_path=r'.', image_name=f'{img_name}.png', is_load_at_runtime=True,
                                            load_wait_time=1)
    print(img_url)
    driver.close()

    driver.quit()
