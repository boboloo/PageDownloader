from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time
import glob
import os
import sys

class Downloader():

    def __init__(self, url):

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_position(0,0)
        self.driver.set_window_size(1920,1080)
        self.driver.get(url)

    def download(self):
        for i in range(100):
            time.sleep(2) # delay because pages render slowly via javascript
            self.driver.save_screenshot("images/"+str(i)+".png")
            # scroll down
            html = self.driver.find_element_by_tag_name('html')
            html.send_keys(Keys.PAGE_DOWN)
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")

    def close(self):
        self.driver.close()


class Sticher():

    def __init__(self):
        self.files = glob.glob('images/*.png')
        self.files.sort(key=os.path.getmtime)

    def stich(self):
        image = Image.open(self.files[0])

        for file in self.files[1:]:
            image2 = Image.open(file)
            image = self.merge(image, image2)

        image.save("stitch/image.png")

    def merge(self, image1, image2):
        (width1, height1) = image1.size
        height2 = image2.size[1]
        
        result_width = width1
        result_height = height1 + height2

        result = Image.new('RGB', (result_width, result_height))
        result.paste(image1, (0,0))
        result.paste(image2, (0,height1))
        return result

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1] == "download":
            d = Downloader(sys.argv[2])
            d.download()
            d.close()
    elif sys.argv[1] == "stitch":
        s = Sticher()
        s.stich()
