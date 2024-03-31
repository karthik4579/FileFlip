from nicegui import ui
from utils import fileflip_utils

utils = fileflip_utils()

@ui.page('/convert')
def file_conversion_ui():
    utils.render_conversion_ui()

@ui.page('/upload')
def upload_ui():
    utils.render_upload_ui()

@ui.page('/download')
def download_ui():
    utils.render_download_ui()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()