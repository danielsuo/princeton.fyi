import os

import pandas as pd
import requests

class Source():
    def __init__(self):
        self.url = None
        self.df = None
        self.filename = None
        self.ext = None

        self.path = None
        self.raw_path = None

    def set_path(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data", self.filename)
        self.raw_path = "{}_raw.{}".format(self.path, self.ext)
        self.path = "{}.{}".format(self.path, self.ext)

    def download(self):
        if self.filename is None or self.ext is None:
            raise ValueError("self.filename or self.ext is None")


        if self.url is None:
            raise ValueError("self.url not specified")

        with open(self.raw_path, "wb") as f:
            f.write(requests.get(self.url, allow_redirects=True).content)

    def parse(self):
        with open(self.raw_path, "r") as f:
            self.df = pd.read_csv(f)
