import bs4
import requests
from bs4 import BeautifulSoup
import json
import logging
import jsonpath_ng.ext as jp


class ChapterScraper:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.session = requests.Session()
        self.session.headers
        self.session.headers.update(self.get_header())
        self.video_processed = 0
        self.total_chapters_found = 0
        self.completed = set()


    def get_header(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding" : "gzip, deflate",
            'Accept-Language': 'en-US,en;q=0.5',
            "Host": "www.youtube.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        return headers
    

    def get_content(self, video_id: str) -> bytes | None:
        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            res = self.session.get(url)
            response_body = res.text
            return response_body

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def get_script_tag(self, content: str) -> str | None:
        bs = BeautifulSoup(content, "lxml")
        script_tags: list[bs4.element.Tag] = bs.find_all("script")
        for script in script_tags:
            if "ytInitialData" in script.text:
                text = script.text.replace("var ytInitialData = ", "")
                text = text[:-1]
                return text
    
        return None
    
        
    def get_chapters(self, video_id: str) -> list[str] | None:
        content = self.get_content(video_id)
        if not content:
            return None
        jsontext = self.get_script_tag(content)
        if jsontext:
            try:
                data = json.loads(jsontext)
                query = jp.parse("$..macroMarkersListItemRenderer.title.simpleText")
                chapter = set()
                for chp in query.find(data):
                    chapter.add(chp.value)
                return chapter
            except json.JSONDecodeError as e:
                logging.error(f"An error occurred: {e}")
                return None

    def scrape_chapters(self):
        while True:
            if self.manager.event.is_set():
                self.manager.save_data()
                return
            if self.manager.video_search_done:
                self.manager.save_data()
                return
            if len(self.manager.video_ids) > 0:
                vid = self.manager.video_ids[0]
                if vid in self.completed:
                    continue
                chapters = self.get_chapters(self.manager.video_ids[0])
                del self.manager.video_ids[0]
                if chapters:
                    self.manager.update_chapters(chapters)
                    self.total_chapters_found += len(chapters)
                    self.manager.update_ui_queue.put({"total_chapters_found": f"{self.total_chapters_found}"})
                
                self.video_processed += 1
                self.manager.update_ui_queue.put({"video_processed": f"{self.video_processed}"})
            