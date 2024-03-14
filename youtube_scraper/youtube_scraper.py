import bs4
import requests
from bs4 import BeautifulSoup
import json
import logging
import jsonpath_ng.ext as jp

class ChapterScraper:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers
        self.session.headers.update(self.get_header())
        

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
            
