# -*- coding: utf-8 -*-
# @Time : 2022/3/13 17:02
# @Author : gemma_leo
# @File : Nagao.py
#使用Nagao算法进行串频统计，并计算熵值、combinability进行筛词，筛词标注为frequency>2,entropy>1.0,combinability<0.01，且左右邻熵值差不超过2
import os
import FileOperator
import re
import math
import time
import pickle as pkl

class nagao():
    def __init__(self):
        self.bt=time.time()
        self.fo = FileOperator.fileOp()
        self.data=None
        self.P=[]#储存Ptable
        self.L=[]#储存Ltable
        self.n_gram={}#储存ngram表
        self.e_table={}#储存熵值
        self.s_infor={}#储存字符串的频率、熵值和combinability
        self.neibor={}#储存字符串邻字信息
        self.words={}#储存潜在词串
        self.split_data=[]#存放分句后的文本
        self.addr=[]#存放字符串地址
        filename = "./Dict/汉字.pkl"  # 加载编码字典
        with open(filename, "rb") as f:
            self.codeData = pkl.load(f)
    def readFile(self,file):#加载文件
        self.bt = time.time()
        if os.path.exists(file) is False:
            return False
        b=time.time()
        code = self.fo.decode(file)
        with open(file, 'r', encoding=code,errors='ignore') as f:
            content = f.read()#.replace('\n', '')
            #content = re.sub('[a-zA-Z0-9\s\W\d]','',content)
            self.data = content#.replace('\t', '')
    def sort(self,result,index): #对list(result)按index从大到小排序，result为字典
        return sorted(result,key=lambda keys:keys.get(index),reverse=True)
    def sort_V(self,result):#对字典result进行排序，排序标准为字典的值（从大到小）
        self.bt = time.time()
        temp=sorted(result.items(),key=lambda x:x[1],reverse=True)
        newDict={}
        for i in temp:
            newDict[i[0]]=i[1]
        return newDict
    def createP(self):#创建Ptable
        self.bt = time.time()
        temp=[]#储存地址
        temp2=[]#储存字符串
        split_data=re.split('[a-zA-Z\d\W+]',self.data)
        temp1=[]
        for i in split_data:
            if len(i)!=0:
                temp1.append(i)
        self.split_data=temp1
        for i in range(0,len(temp1)):
            s=temp1[i]
            l=len(s)
            for j in range(0,l):
                temp.append([s[j:],i,j])
        self.bt=time.time()
        #for i in range(0,len(self.data)):
         #   temp.append(self.data[i:])
        #temp.sort()
        temp=sorted(temp,key=lambda keys:keys[0],reverse=True)
        for word in temp:
            temp2.append(word[0])
        self.addr=temp
        self.P=temp2
    def createL(self):#创建Ltable
        self.bt = time.time()
        temp=[]
        l=len(self.P)
        temp.append(0)
        for i in range(1,l):
            temp.append(self.shareStr(self.P[i],self.P[i-1]))
        self.L=temp
    def shareStr(self,s1,s2):#输出两个字符串相同最左字串大小
        l=len(s1)
        for i in range(1,l+1):
            temp=s1[:i]
            if s2.startswith(temp) is False:
                return len(temp)-1
        return len(temp)
    def getNgram(self,n,m=1):#获取出现频率>2的，长度在m到n之间的字符串频次
        self.bt = time.time()
        l=len(self.P)
        d={}#用以存放频次大于2的字符串
        s={}#用以存放邻字
        while n > m-1:
            for i in range(1,l):
                if self.L[i] >= n:#L中数值大于等于n，说明一个长度为n的字符串重复出现了一次
                    k=self.P[i][:n]#记录该重复出现的长度为n的字符串
                    if k in d.keys():
                        d[k]=d[k]+1
                        loc=self.addr[i]
                        if loc[2]==0:
                            pre='$'
                        else:
                            pre=self.split_data[loc[1]][loc[2]-1]
                        if loc[2]+n == len(self.split_data[loc[1]]):
                            suf='#'
                        else:
                            suf=self.split_data[loc[1]][loc[2]+n]
                        s[k][0].append(pre)
                        s[k][1].append(suf)
                    else:
                        d[k]=2
                        loc1=self.addr[i - 1]
                        loc=self.addr[i]
                        if loc[2]==0:
                            pre='$'
                        else:
                            pre=self.split_data[loc[1]][loc[2]-1]
                        if loc[2]+n == len(self.split_data[loc[1]]):
                            suf='#'
                        else:
                            suf=self.split_data[loc[1]][loc[2]+n]
                        if loc1[2]==0:
                            pre1='$'
                        else:
                            pre1=self.split_data[loc1[1]][loc1[2]-1]
                        if loc1[2]+n == len(self.split_data[loc1[1]]):
                            suf1='#'
                        else:
                            suf1=self.split_data[loc1[1]][loc1[2]+n]
                        s[k]=[[pre,pre1],[suf,suf1]]

            n=n-1
        self.n_gram=d
        self.neibor=s
        return d
    def countFile(self,f,n,m=1):#统计文件f中长度在m到n之间的潜在词，返回一个字典
        self.bt = time.time()
        if self.readFile(f) is False:
            return False
        self.createP()
        self.createL()
        self.getNgram(n,m)
        self.entropy(n,m)
        self.combinability()
        self.filter()
    def countDir(self,dir,n,m=1,index='frequency'):#统计文件f中长度在m到n之间的潜在词，返回一个字典
        b_t=time.time()
        self.bt = time.time()
        f_list=[]
        temp='./temp.txt'
        with open(temp,'w') as f1:
            for i in self.fo.walkDir(dir):
                if i.endswith('.txt'):
                    code=self.fo.decode(i)
                    with open(i,'r',encoding=code) as f2:
                        content=f2.read()
                    f1.write(content)
                    f1.write('\n')
        self.countFile(temp,n,m)
        self.sortInfor(index)
        return len(self.words.keys())
    def sortInfor(self,index):#根据index对筛选出的词表进行排序
        temp=[]
        for key in self.words.keys():
            fre=self.words[key][0]
            word=key
            gbk=''
            UTF8=''
            unicode=''
            pin=''
            for c in key:
                if c in self.codeData.keys():#滤掉非汉字字符
                    gbk=gbk+self.codeData[c]['gbk']
                    UTF8 = UTF8 + self.codeData[c]['UTF8']
                    unicode = unicode + self.codeData[c]['unicode']
                    pin = pin + self.codeData[c]['拼音']
                    entry={'word':word,'gbk':gbk,'UTF8':UTF8,'unicode':unicode,'拼音':pin,'frequency':fre}
                    temp.append(entry)
        newlist=self.sort(temp,index)
        result={}
        for record in newlist:
            result[record['word']]=record['frequency']
        self.words=result
        self.fo.writeDict(self.words, 'word_fre.txt',
                          comments='words\tfrequency')
        return 0
    def entropy(self,n,m):#计算所有待选词串（f>2)的左右邻熵值，返回一个字典
        self.bt = time.time()
        e = {}  # 邻接熵,words:[{lw:f},{rw:f},n]
        for word in self.n_gram.keys():
            l_neibor=self.neibor[word][0]
            r_neibor=self.neibor[word][1]
            fre=self.n_gram[word]
            lw={}
            rw={}
            le_v=0
            re_v=0
            for i in l_neibor:
                if i in lw.keys():
                    lw[i]=lw[i]+1
                else:
                    lw[i]=1
            for i in r_neibor:
                if i in rw.keys():
                    rw[i]=rw[i]+1
                else:
                    rw[i]=1
            for i in lw.keys():
                t=lw[i]/fre
                le_v = le_v - t * math.log(t, 2)
            for i in rw.keys():
                t = rw[i] / fre
                re_v = re_v - t * math.log(t, 2)
            e[word]=[fre,format(le_v,'.6f'),format(re_v,'.6f')]
        self.e_table=e
    def combinability(self):#计算combinability以反映待选词条的内部凝固度
        self.bt = time.time()
        d={}
        for i in self.n_gram.keys():
            l=len(i)
            temp_c=0
            base=self.n_gram[i]
            n=len(self.data)
            for j in range(1,l-1):
                try:
                    f1=self.n_gram[i[:j]]
                except:
                    f1=1
                try:
                    f2=self.n_gram[i[j:]]
                except:
                    f2=1
                f=(f1*f2)/(base*n)
                temp_c=max(f,temp_c)
            entry=self.e_table[i]
            entry.append(temp_c)
            d[i]=entry
        self.s_infor=d
        return d
    def filter(self,fre=3,com=0.001,le=1.0,re=1.0):#筛选文件中的潜在词，要求:频次大于3，combinability小于0.001，左右熵值均大于1.0
        self.bt=time.time()
        d={}
        for k in self.s_infor.keys():
            i=self.s_infor[k]
            l_e=float(i[1])
            r_e=float(i[2])
            if l_e>= le and r_e >= re and i[0]>=fre and i[3] < com and abs(l_e-r_e)<=2:
                d[k]=i
            if len(k)==1 and r_e >= re and l_e>= le and i[0]>=fre and abs(l_e-r_e)<=2:
                d[k]=i
        self.words=self.sort_V(d)
        self.fo.writeDict(self.words, 'word_count(中间文件).txt',
                          comments='words\tfrequency\tleft-entropy\tright-entropy\tcombinality')


#a=nagao()
#a.countFile('./测试文档/199801_new.txt',5)
#a.countFile('./测试文档/test.txt',5)



