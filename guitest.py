import threading
import time


class YoutubeChapterScraperSelenium:
    def __init__(self, url, excelname, limit, myqueue) -> None:
        self.url = url
        self.excelname = excelname
        self.limit = limit
        self.myqueue = myqueue


    def startWork(self, event: threading.Event):
        i = 0
        while i < 12:
            time.sleep(1)
            if event.is_set():
                break
            self.myqueue.put({"total_videos_found": f"{i}", "total_videos_scraped": f"{i+1}", "total_chapters_found": f"{i+2}"})
            i += 1
