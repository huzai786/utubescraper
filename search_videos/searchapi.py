import requests


class ApiSearch:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.validate_key(api_key)

    # def validate_key(self, apikey):
    #     payload = (("api_key", apikey))
    #     try:
    #         requests.get("https://www.googleapis.com/youtube/v3/search", params=payload)
    #     pass

    def get_search_results(self) -> list[str]:
        pass
