import os
import threading
import time
import dearpygui.dearpygui as dpg
import queue

from api_version.scraper_api import YoutubeChapterScraperApi

class GUI:
    def __init__(self) -> None:
        self.queue = queue.Queue()
        self.default_font = None
        self.scrapingthread = None
        self.event = None
        self.start_time = None
        self.end_time = None
        if not os.path.exists("data"):
            os.mkdir("data")

    def error_popup(self, sender, app_data):
        with dpg.window(label="Error", width=300, height=100, pos=[240, 200],  no_close=True, no_collapse=True, tag="error", modal=True):
            dpg.add_text("Please fill in all fields!")
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("error"))

    def success_popup(self):
        with dpg.window(label="Success", width=300, height=220, pos=[240, 200],  no_close=True, no_collapse=True, tag="success", modal=True):
            dpg.add_text("Scraping completed!")
            dpg.add_text(dpg.get_value("total_vid_found"))
            dpg.add_text(dpg.get_value("total_video_processed"))
            dpg.add_text(dpg.get_value("total_chapter_found"))
            dpg.add_text(f"In {self.end_time - self.start_time:.2f} seconds")
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("success"))

    def scraper_thread(self, query, excel_name, limit):
        self.event = threading.Event()
        scraper = YoutubeChapterScraperApi(query, excel_name, limit, self.queue, self.event)
        scraper.startScraping()


    def start_scraper(self, sender, app_data):
        query = dpg.get_value("search_query")
        excel_name = dpg.get_value("excel_name")
        limit = dpg.get_value("max_limit")
        if not query or not excel_name or not limit:
            self.error_popup(None, None)
            return
        else:
            dpg.configure_item("search_query", enabled=False)
            dpg.configure_item("excel_name", enabled=False)
            dpg.configure_item("max_limit", enabled=False)
            dpg.configure_item("stop", enabled=True)
            dpg.configure_item("start", enabled=False)
            self.start_time = time.perf_counter()
            self.scrapingthread = threading.Thread(target=self.scraper_thread, args=(query, excel_name, limit))
            self.scrapingthread.start()

    def check_queue_callback(self):
        if not self.queue.empty():
            value = self.queue.get()
            if total_videos_found := value.get("total_vid_found", None):
                dpg.set_value("total_vid_found", f"Total Videos Found: {total_videos_found}")
            if video_processed := value.get("video_processed", None):
                dpg.set_value("total_video_processed", f"Total Videos Processed: {video_processed}")
            if total_chapters_found := value.get("total_chapters_found", None):
                dpg.set_value("total_chapter_found", f"Total Chapters Found: {total_chapters_found}")

            dpg.set_value("status", "Status: Running")

        if self.scrapingthread and not self.scrapingthread.is_alive():
            self.end_time = time.perf_counter()
            self.success_popup()
            self.start_time = None
            self.end_time = None

            dpg.set_value("total_vid_found", "Total Videos Found: 0")
            dpg.set_value("total_video_processed", "Total Videos Processed: 0")
            dpg.set_value("total_chapter_found", "Total Chapters Found: 0")
            dpg.set_value("status", "Status: Not Running")
            dpg.set_value("search_query", "")
            dpg.set_value("excel_name", "")
            dpg.set_value("max_limit", 100)
            self.scrapingthread = None
            dpg.configure_item("search_query", enabled=True)
            dpg.configure_item("excel_name", enabled=True)
            dpg.configure_item("max_limit", enabled=True)
            dpg.configure_item("stop", enabled=False)
            dpg.configure_item("start", enabled=True)
            
            

    def stop_thread(self):
        self.event.set()

    def initiate_gui(self):
        dpg.create_context()
        dpg.create_viewport(title='Youtube Scraper Api Version', width=800, height=600, vsync=True)
        dpg.setup_dearpygui()

        with dpg.font_registry():
            self.default_font = dpg.add_font("font.ttf", 20)
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvInputText, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 68), category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvInputInt, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 68), category=dpg.mvThemeCat_Core)
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 30, 30, 68), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 68), category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)
        with dpg.window(tag="Youtube Scraper"):
            dpg.add_text("Youtube Scraper Api Version", indent=280)
            dpg.add_text("Enter query:")
            dpg.add_input_text(tag="search_query", width=300)
            dpg.add_text("Enter Excel File name: ")
            dpg.add_input_text(tag="excel_name", width=300)
            dpg.add_text("Enter Max limit: ")
            dpg.add_input_int(tag="max_limit", width=300, default_value=100)

            dpg.add_button(label="Start", callback=self.start_scraper, pos=[10, 510], width=100, height=40, tag="start")
            dpg.add_button(label="Stop", callback=self.stop_thread, pos=[120, 510], width=100, height=40, enabled=False, tag="stop")
            dpg.add_separator()
            dpg.add_text("Total Videos Found: 0", tag="total_vid_found")
            dpg.add_text("Total Videos Processed: 0", tag="total_video_processed")
            dpg.add_text("Total Chapters Found: 0", tag="total_chapter_found")
            dpg.add_text("Status: Not Running", tag="status", pos=[600, 520])
            dpg.bind_font(self.default_font)

        dpg.show_viewport()
        dpg.set_primary_window("Youtube Scraper", True)

    def main_loop(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            self.check_queue_callback()
        dpg.destroy_context()

gui = GUI()
gui.initiate_gui()
gui.main_loop()