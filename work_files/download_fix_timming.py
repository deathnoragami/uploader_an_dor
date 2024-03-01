import requests
import os
import subprocess

class FixTimming:
    def __init__(self) -> None:
        url = os.getenv('URL_FIX_TIMMING')
        with requests.get(url) as r:
            path = os.path.join(os.getcwd(), 'Add_Keys.reg')
            with open(path, 'wb') as f:
                f.write(r.content)
        os.startfile(path)

            