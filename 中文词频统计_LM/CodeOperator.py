# -*- coding: utf-8 -*-
# @Time : 2022/3/6 18:17
# @Author : gemma_leo
# @File : CodeOperator.py
#获取字符编码信息

import pickle as pkl
import os

class codeOp():
    def __init__(self):#加载储存字符编码的字典
        self.keys=["汉字","gbk","unicode","Big5","UTF8","拼音","笔画数"] #索引名
        filename = "./Dict/汉字.pkl"
        with open(filename, "rb") as f:
            self.data = pkl.load(f)
    def search(self,key): #根据输入字符key查询相应条目,以字典形式返回该字符的字符、gbk码、unicode码、big5码、utf8码、拼音和笔画数信息
        result=self.data.get(key)
        return result
    def sort(self,result,index): #对list(result)按index排序，result为字典
        return sorted(result,key=lambda keys:keys.get(index),reverse=False)

