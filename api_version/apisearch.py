import json
import requests
from datetime import datetime

class ApiSearch:
    def __init__(self, key, manager):
        self.manager = manager
        self.key = key
        self.session = requests.Session()

    def search_results(self, query, limit, publishedAfter: datetime=None, publishedBefore: datetime=None):
        url = "https://www.googleapis.com/youtube/v3/search"
        video_ids = []
        page_token = None
        total_results = 0
        while total_results <= limit:
            try:
                if self.manager.event.is_set():
                    break
                params = {
                    "key": self.key,
                    "q": query,
                    "maxResults": 50,
                    "safeSearch": "none",
                    "type": "video",
                    "videoDefinition": "any",
                    "videoDuration": "any",
                    "videoEmbeddable": "any",
                    "videoType": "any"
                }
                if publishedAfter:
                    params["publishedAfter"] = publishedAfter.strftime('%Y-%m-%dT%H:%M:%SZ')

                if publishedBefore:
                    params["publishedBefore"] = publishedBefore.strftime('%Y-%m-%dT%H:%M:%SZ')
                if page_token:
                    params["pageToken"] = page_token

                res = self.session.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    page_token = data.get("nextPageToken")

                    for item in data.get("items", []):
                        video_id = item["id"]["videoId"]
                        total_results += 1
                        video_ids.append(video_id)

                    self.manager.update_ui_queue.put({"total_vid_found": f"{total_results}"})
                        
                    if not page_token or total_results >= limit:
                        print("max results Found!")
                        break
                else:
                    if res.status_code != 200:
                        print(f"Error: {res.json()['error']['message']}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break

        return video_ids






