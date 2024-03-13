import dearpygui.dearpygui as dpg


dpg.create_context()
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("font.ttf", 20)

def pressme():
    print("pressed")

dpg.create_viewport(title='Youtube Scraper', width=800, height=600)
with dpg.window(tag="Youtube Scraper"):
    dpg.add_text("Youtube Scraper", indent=320)
    dpg.add_button(label="Save", callback=pressme)
    dpg.bind_font(default_font)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Youtube Scraper", True)
dpg.start_dearpygui()
dpg.destroy_context()
