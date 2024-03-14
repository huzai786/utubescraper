import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException


class SeleniumSearch:
    def __init__(self, manager) -> None:
        self.manager = manager
        options = Options()
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        options.add_argument("Accept-Language=en-US,en;q=0.5")
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        self.driver.implicitly_wait(5)
        self.video_count = 0

    def search_results(self, url, limit):
        self.driver.get(url)
        while self.driver.execute_script("return document.readyState;") != "complete":
            time.sleep(1)
        regex = r'\/watch\?v=([A-Za-z0-9_-]+)'
        videos = []
        current_video_index = 0
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ytd-section-list-renderer//ytd-item-section-renderer//ytd-video-renderer")))
            time.sleep(1.5)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if self.manager.event.is_set():
                break
            if new_height == last_height:
                print("No More Results Found!")
                break
            videos = self.driver.find_elements(By.XPATH, "//ytd-section-list-renderer//ytd-item-section-renderer//ytd-video-renderer")
            self.video_count = len(videos)
            self.manager.update_ui_queue.put({"total_videos_scraped": f"{self.video_count}"})
            if current_video_index < self.video_count:
                for i in range(current_video_index, self.video_count):
                    elem = videos[i]
                    try:
                        atag = elem.find_element(By.XPATH, ".//a")
                        href = atag.get_attribute("href")
                        vmatch = re.search(regex, href)
                        if vmatch:
                            vidid = vmatch.group(1)
                            self.manager.video_ids.append(vidid)
                    except NoSuchElementException:
                        pass
                current_video_index = self.video_count
            if self.video_count >= limit:
                break
            
            last_height = new_height

        self.cleanup()
    
    def cleanup(self):
        self.video_count = 0
        self.driver.quit()

    def check_ready_state(self):
        state = self.driver.execute_script("return document.readyState;")
        print(state)





