#!/usr/bin/env python
# coding: utf-8
#

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
import re
import sys
from time import sleep

LINK_REGEX = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")
class LinkCollector:
    def __init__(self, url):
        self.url = "http://" + urlparse(url).netloc
        self.collected_links = set()
        self.visited_links = set()

    def collect_links(self, path='/',i=0):
        if i >= 2: return
        full_url = self.url + path
        self.visited_links.add(full_url)
        page = str(urlopen(full_url).read())
        links = LINK_REGEX.findall(page)
        links = { self.normalize_url(path, link) for link in links }
        self.collected_links = links.union(self.collected_links)
        unvisited_links = links.difference(self.visited_links)
        for link in unvisited_links:
            try:
                self.collect_links(urlparse(link).path,i=i+1)
            except HTTPError as e:
                print(e.msg)
            except Exception:
                pass

    def normalize_url(self, path, link):
        if link.startswith("/"):
            return self.url + link
        elif link.startswith("http://") or link.startswith("https://"):
            return link
        else:
            return self.url + path.rpartition('/')[0] + '/' + link

if __name__ == '__main__':
    collector = LinkCollector(sys.argv[1])
    collector.collect_links()
    for link in collector.collected_links:
        print(link)
    print(len(collector.collected_links))