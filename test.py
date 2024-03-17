from settings import api_key
from api_version.scraper_api import ApiSearch


api = ApiSearch(api_key)
videos = api.search_results("cats", 100)
print(videos)
