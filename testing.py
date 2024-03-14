from search_videos.searchselenium import SeleniumSearch


ss = SeleniumSearch()

videosids = ss.search_results("https://www.youtube.com/results?search_query=pygame", limit=100)
print(videosids)

