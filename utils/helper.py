import os
from sys import platform


def kill_browser():
    """[kill selenium browser instance when scraping is done.]"""
    if platform == "linux" or platform == "linux2":
        # linux
        pass
    elif platform == "darwin":
        # OS X
        os.system("pkill firefox")
    elif platform == "win32":
        # Windows...
        os.system("taskkill /im firefox.exe /f")
