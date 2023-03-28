# -*- coding: utf-8 -*-
# @Time : 2022/3/12 23:59
# @Author : gemma_leo
# @File : CharFrequency.py
#字频统计
import pickle as pkl
import FileOperator as fo

class charF():
    def __init__(self):
        self.alphaD={} #储存字母字符
        self.digitD={} #储存数字字符
        self.charD={} #储存中文字符
        self.restD={} #储存其他字符
        filename = "./Dict/汉字.pkl" #加载编码字典
        with open(filename, "rb") as f:
            self.codeData = pkl.load(f)
        self.fileOp=fo.fileOp()#加载文件处理器
    def sort(self,result,index): #对list(result)按index从大到小排序，result为字典
        return sorted(result,key=lambda keys:keys.get(index),reverse=True)
    def sort_V(self,result):#对字典result进行排序，排序标准为字典的值（从大到小）
        temp=sorted(result.items(),key=lambda x:x[1],reverse=True)
        newDict={}
        for i in temp:
            newDict[i[0]]=i[1]
        return newDict
    def count_file(self,filename):#统计单个文件数字字符、汉字字符、字母字符及其他字符频次
        code=self.fileOp.decode(filename)
        with open(filename,encoding=code) as f:#
            content=f.read()
        content=content.replace('\n','')
        content = content.replace('\t', '')
        for i in content:
            if i.isdigit() :#统计数字字符
                if i in self.digitD.keys():
                    self.digitD[i]=self.digitD[i]+1
                else:
                    self.digitD[i]=1
            elif i in self.codeData.keys():#统计汉字字符
                if i in self.charD.keys():
                    self.charD[i]['frequency']=self.charD[i]['frequency']+1
                else:
                    entry = self.codeData[i]
                    entry['frequency'] = 1
                    self.charD[i]=entry
            elif i.isalpha():#统计字母字符
                if i in self.alphaD.keys():
                    self.alphaD[i] = self.alphaD[i] + 1
                else:
                    self.alphaD[i] = 1
            else:#统计其他字符
                if i in self.restD.keys():
                    self.restD[i]=self.restD[i]+1
                else:
                    self.restD[i]=1
    def count_dir(self,dirname,order=None,flag=True): #统计一个文件夹下所有文件的字符（仅支持txt文件）
        #并根据指定排序要求order(unicode、gbk、UTF8，拼音、frequency)对汉字字符进行排序
        #返回四个字典格式的结果，{char:frequency}，默认按字频排序
        for i in self.fileOp.walkDir(dirname):
            if i.endswith('.txt'):
                self.count_file(i)
        result=[]
        if order is not None:
            if order not in ['unicode','gbk','UTF8','拼音','frequency']:
                temp=self.sort(list(self.charD.values()),'frequency') #输入无效排序标准时，默认按字频顺序输出
            else:
                temp = self.sort(list(self.charD.values()), order)
        else:
            temp = self.sort(list(self.charD.values()), 'frequency')  # 未输入排序标准时，默认按字频顺序输出
        newDict={}
        num=0
        for i in temp:
            newDict[i['汉字']]=i['frequency']
            num=num+1
        self.digitD=self.sort_V(self.digitD)
        self.alphaD = self.sort_V(self.alphaD)
        self.restD = self.sort_V(self.restD)
        result.append(newDict)
        if flag is True:
            result.append(self.digitD)
            num=num+len(self.digitD.keys())
            result.append(self.alphaD)
            num = num + len(self.alphaD.keys())
            result.append(self.restD)
            num = num + len(self.restD.keys())
            comment = ['汉字统计结果','数字统计结果','字母统计结果','其他字符统计结果']
        else:
            comment = ['汉字统计结果']
        savepath='char_fre.txt'

        self.saveResult(result,savepath,comment)
        return num
    def saveResult(self,result,file,comments=None): #将统计结果result保存进file文件中
        if comments is not None and len(result)== len(comments):
            for i in range(0,len(result)):
                if i ==0:
                    self.fileOp.writeDict(result[i], file, 'w', comments[i])
                else:
                    self.fileOp.writeDict(result[i],file,'a',comments[i])
        else:
            for i in range(0,len(result)):
                self.fileOp.writeDict(result[i],file,'w')
#a=charF()
#r=a.count_dir(r'.\测试文档','frequency',False)
