#!/usr/bin/env python
# coding: utf-8

class LongNameDict(dict):
    '''支持返回长度最长的key'''
    def longest_key(self):
        longest = None
        for key in self:
            if not longest or len(longest) < len(key):
                longest = key
        return longest

if __name__ == '__main__':
    longest = LongNameDict({"short":1, "second-become-to-longest":2, "longestone":3}).longest_key()
    print(longest)