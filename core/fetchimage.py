import requests
import platform
import os
from urllib.parse import urlparse

def fetch_image(url):
    """
    Fetch image from supplied URL. Store and use to display to user 
    in GUI.
    """
    if url[:8] != 'https://':
        url = 'https://' + url
    response = requests.get(f"{url}/favicon.ico")

    if response.status_code != 200:
        # No favicon found, use default image
        return

    directory = {
        "Linux": os.path.expanduser("~/.local/share/pm/images/"),
        "Windows": os.path.expanduser("~\\AppData\\pm\\images\\"),
    }
    dir = directory.get(platform.system())

    if dir is not None and not os.path.exists(dir):
        os.makedirs(dir)

    domain = urlparse(url).netloc
    with open(f"{dir}{domain}", "wb") as f:
        f.write(response.content)
