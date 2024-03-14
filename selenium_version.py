import time
import queue


class YoutubeChapterScraperSelenium:
    def __init__(self, url, excelname, limit, queue: queue.Queue) -> None:
        self.url = url
        self.excelname = excelname
        self.limit = limit
        self.queue = queue
