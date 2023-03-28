# -*- coding: utf-8 -*-
# @Time : 2022/3/6 20:12
# @Author : gemma_leo
# @File : fileOperator.py
#文件夹操作类

import os
import chardet

class fileOp():
    def walkDir(self,dir):#传入文件夹地址。遍历文件夹，返回其下所有文件名(以list储存)
        if os.path.exists(dir) is False:#文件夹不存在时，返回False
            return False
        f_list = [] #用于储存文件名
        for dirpath, dirnames, filenames in os.walk(dir):
            for file in filenames:
                f=os.path.join(dirpath,file)
                f_list.append(f)
        return f_list
    def decode(self,filename):#输入文件名，返回文件编码格式。文件不存在时，返回False。
        if os.path.exists(filename) is False:
            return False
        with open(filename,"rb") as f:
            content=f.read()
            code=chardet.detect(content)
        return code['encoding']
    def tran_code(self,filename,newcode):#输入文件名，将文件编码格式转换为指定格式(GBK,utf8,unicode)。文件不存在时，返回False。
        if os.path.exists(filename) is False:
            return False
        if newcode not in ['utf8','gbk','unicode']:
            return False
        with open(filename,"rb") as f1:
            content=f1.read()
            encoding = chardet.detect(content)["encoding"]
            content = content.decode(encoding).encode(newcode)
        with open(filename,'wb') as f2:
            f2.write(content)
        return 0
    def writeDict(self,d,f,flag='w',comments=None):#将字典以每行一条key value记录的格式写入txt文档f，默认为写入模式，
        #可设置为追加模式(flag='a'),亦可在文件开头添加注释comments
        with open(f,flag) as f:
            if comments is None:
                f.write('----------------这是一条分割线----------------\n')
            else:
                f.write(comments+'\n')
            t=list(d.values())[0]
            if isinstance(t,list):
                for k in d.keys():
                    s=k+' \t '
                    for v in d[k]:
                        s=s+str(v)+' \t '
                    s=s+'\n'
                    f.write(s)
            else:
                for k in d.keys():
                    entry=str(k)+'\t'+str(d[k])+'\n'
                    f.write(entry)








