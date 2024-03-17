import requests

class ApiSearch:
    def __init__(self, key, manager=None):
        self.manager = manager
        self.video_count = 0
        self.key = key
        self.session = requests.Session()

    def search_results(self, query, limit):
        url = "https://www.googleapis.com/youtube/v3/search"
        video_ids = []
        page_token = None
        total_results = 0

        while total_results < limit:
            try:
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

                if page_token:
                    params["pageToken"] = page_token

                res = self.session.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    total_results = data["pageInfo"]["totalResults"]
                    page_token = data.get("nextPageToken")

                    for item in data.get("items", []):
                        video_id = item["id"]["videoId"]
                        video_ids.append(video_id)
                        self.video_count += 1

                    if not page_token or self.video_count >= limit:
                        break
                else:
                    print(f"Error: {res.status_code}, {res.text}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break

        return video_ids






