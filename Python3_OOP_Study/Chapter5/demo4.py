#!/usr/bin/env python
# coding: utf-8

from urllib.request import urlopen
from time import time,sleep

class WebPage:
    def __init__(self, url):
        self.url = url
        self._content = None

    @property
    def content(self):
        if not self._content:
            print("Retrieving New Page...")
            self._content = urlopen(self.url).read()
        return self._content

if __name__ == '__main__':
    wb = WebPage("http://www.baidu.com")
    now = time()
    print(wb.content)
    print(time() - now)
    sleep(5)
    now = time()
    print(wb.content)
    print(time() - now)