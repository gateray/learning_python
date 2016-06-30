#!/usr/bin/env python
# coding: utf-8

#命名元组
from collections import namedtuple
#namedtuple(),第一个参数为命名元组的描述,第二个参数为属性字符串,每个属性以空格分开
Stock = namedtuple("Stock", "symbol current high low")
stock = Stock("GOOD", 613.30, high=625.86, low=610.50)
print("name: {0}, current: {1}, high: {2}, low: {3}".format(
    stock.symbol,
    stock.current,
    stock.high,
    stock.low
))

#使用默认字典统计一个字母在给定句子中的出现次数
from collections import defaultdict
def letter_freq(sentence):
    #defaultdict类构造函数中可以接收一个函数作为参数,当访问字典中一个不存在的key时,会以无参方式调用该函数,将其返回值作为该key的默认值
    freq = defaultdict(int)
    for letter in sentence:
        freq[letter] += 1
    return freq

freq = letter_freq("python is very nice program language.")
for k,v in freq.items():
    print("{}:{}".format(k,v))

