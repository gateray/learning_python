#!/usr/bin/env python
# coding: utf-8
# 自己实现一个有序的字典(按key插入顺序排序)

from collections import KeysView, ItemsView, ValuesView
class DictSorted(dict):
    def __new__(*args, **kwargs):
        new_dict = dict.__new__(*args, **kwargs)
        new_dict.ordered_keys = []
        return new_dict
    def __setitem__(self, key, value):
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        super().__setitem__(key, value)
    def setdefault(self, k, d=None):
        if k not in self.ordered_keys:
            self.ordered_keys.append(k)
        super().setdefault(k, d)
    def __iter__(self):
        return self.ordered_keys.__iter__()

    #集合库为字典提供了3个只读视图(View对象),可以使用__iter__方法来遍历键,之后用__getitem__来获取值,所以只需重写
    # __iter__方法就可以让3个视图都重新工作起来
    def keys(self):
        return KeysView(self)
    def values(self):
        return ValuesView(self)
    def items(self):
        return ItemsView(self)
