# -*- coding: utf-8 -*-
# @Time : 2022/3/6 22:47
# @Author : gemma_leo
# @File : Frame.py
import  tkinter as tk
import tkinter.messagebox as tkm
from tkinter import *
import FileOperator
import CodeOperator
import os
import CharFrequency
import Nagao

class frame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.information=["字频查询：输入一个文件夹地址，统计其下utf8、gbk和unicode编码格式的txt文件的单子字符，结果输出为一个txt文件",
                          "词频查询：发现一个文件夹地址，统计其下utf8、gbk和unicode编码格式的txt文件的潜在词串（frequency>2,"
                          "左右邻熵值均大于1且两者差距不大于2，combinality<0.001,长度小于等于5），结果输出为一个txt文件"]
        self.setup()#主界面加载
        self.top=None#当前小窗口

    def setup(self):
        #基本框架
        self.mainframe = tk.Frame(self, width=500, height=100)#主界面
        self.title('字频及词频程序')#标题
        self.geometry('500x100+400+130')
        #菜单生成
        self.menubar = tk.Menu(self, tearoff=0,  fg='black')
        self.menubar.add_command(label='说明', command=self.instruction) #程序说明
        self.menubar.add_command(label="字频查询",command=lambda : self.windowChar())
        self.menubar.add_command(label="词频查询",command=lambda : self.windowWord())
        self.menubar.add_command(label="退出", command=self.mainframe.quit)#退出程序
        #主窗口组件
        self.lable1 = tk.Label(self.mainframe,font=('Kaiti', 20),bg='white',height=2,text="请在菜单栏中选择所需功能",width=30)#指示标签
        self.lable1.pack(pady=18)

        self.mainframe.pack()
        self.config(menu=self.menubar)
    def instruction(self):#显示程序说明
        infor=''
        for i in self.information:
            infor = infor+i+"\n"
        tk.messagebox.showinfo('说明',infor)

    def windowChar(self):#创建字频统计窗口

        if self.top is not None:
            self.top.destroy()#清除此前窗口
        self.top=tk.Toplevel()
        self.top.title('字频查询')
        self.top.geometry('400x300+400+200')
        lable1=tk.Label(self.top,font=('Kaiti', 14),height=2,text="请输入一个文件夹目录")
        lable1.pack(pady=3)
        statement = StringVar()  # 输入内容
        entry = tk.Entry(self.top, width=35, font=('Kaiti', 14), textvariable=statement,justify='center')  # 输入框
        statement.set("./测试文档")
        entry.pack(pady=10)

        radioFrame=tk.Frame(self.top)
        radioFrame.pack(side=LEFT,expand='no',fill='y',padx=20)
        lable2 = tk.Label(radioFrame, font=('Kaiti', 12), height=2, text="请选择排序标准")
        lable2.pack(side=TOP)
        #'unicode', 'gbk', 'UTF8', '拼音', 'frequency'
        order=StringVar()
        order.set('frequency')
        R1 = tk.Radiobutton(radioFrame, text="unicode", variable=order, value='unicode')
        R2 = tk.Radiobutton(radioFrame, text="gbk", variable=order, value='gbk')
        R3 = tk.Radiobutton(radioFrame, text="UTF8", variable=order,value='UTF8')
        R4 = tk.Radiobutton(radioFrame, text="拼音", variable=order, value='拼音')
        R5 = tk.Radiobutton(radioFrame, text="frequency", variable=order,value='frequency')
        R1.pack(side=TOP)
        R2.pack(side=TOP)
        R3.pack(side=TOP)
        R4.pack(side=TOP)
        R5.pack(side=TOP)

        lable3 = tk.Label(self.top, font=('Kaiti', 12), height=2, text="是否包含非汉字字符")
        lable3.pack(padx=20, side=TOP)
        flag=BooleanVar()
        flag.set(True)
        R7 = tk.Radiobutton(self.top, text="是", variable=flag, value=True)
        R8 = tk.Radiobutton(self.top, text="否", variable=flag, value=False)
        R7.pack(padx=25, side=TOP)
        R8.pack(padx=25, side=TOP)
        b1=tk.Button(self.top,text='执行',font=('Kaiti', 12),command=lambda: self.queryChar(statement.get(),order.get(),                                                                                         flag.get()),padx=4)
        b1.pack(pady=40)
    def queryChar(self,dir,order,flag):#字频统计
        if os.path.exists(dir) is False:
            tk.messagebox.showerror('提示','该文件夹不存在，请重新输入')
            return
        self.charOp=CharFrequency.charF()

        try:
            r=self.charOp.count_dir(dir,order,flag)
            del self.charOp
            infor='字频统计成功！共统计'+str(r)+'个字符，详见char_fre.txt文件'
            tk.messagebox.showinfo('提示',infor)
        except:
            tk.messagebox.showerror('警告','发生错误，请重新尝试')
    def windowWord(self):#创建词频统计窗口
        if self.top is not None:
            self.top.destroy()  # 清除此前窗口
        self.top = tk.Toplevel()
        self.top.title('词频查询')
        self.top.geometry('400x300+400+200')
        lable1 = tk.Label(self.top, font=('Kaiti', 14), height=2, text="请输入一个文件夹目录")
        lable1.pack(pady=3)
        statement = StringVar()  # 输入内容
        entry = tk.Entry(self.top, width=35, font=('Kaiti', 14), textvariable=statement, justify='center')  # 输入框
        statement.set("./测试文档")
        entry.pack(pady=10)

        radioFrame = tk.Frame(self.top)
        radioFrame.pack(side=LEFT, expand='no', fill='y', padx=50)
        lable2 = tk.Label(radioFrame, font=('Kaiti', 12), height=2, text="请选择排序标准")
        lable2.pack(side=TOP)
        # 'unicode', 'gbk', 'UTF8', '拼音', 'frequency'
        order = StringVar()
        order.set('frequency')
        R1 = tk.Radiobutton(radioFrame, text="unicode", variable=order, value='unicode')
        R2 = tk.Radiobutton(radioFrame, text="gbk", variable=order, value='gbk')
        R3 = tk.Radiobutton(radioFrame, text="UTF8", variable=order, value='UTF8')
        R4 = tk.Radiobutton(radioFrame, text="拼音", variable=order, value='拼音')
        R5 = tk.Radiobutton(radioFrame, text="frequency", variable=order, value='frequency')
        R1.pack(side=TOP)
        R2.pack(side=TOP)
        R3.pack(side=TOP)
        R4.pack(side=TOP)
        R5.pack(side=TOP)

        b1 = tk.Button(self.top, text='执行', font=('Kaiti', 12),
                       command=lambda: self.queryWord(statement.get(), order.get()), padx=4)
        b1.pack(pady=60,padx=60)
    def queryWord(self,dir,order):#词频统计
        if os.path.exists(dir) is False:
            tk.messagebox.showerror('提示','该文件夹不存在，请重新输入')
            return
        self.wordOp = Nagao.nagao()  # 加载词频处理器
        tk.messagebox.showinfo('提示','若数据处理量较大，"程序可能需要一定时间运行(如示例文件夹需要约30秒钟处理),请稍作等待，不要直接关闭程序')
        try:
            r=self.wordOp.countDir(dir,5,index=order)
            del self.wordOp
            infor='词频统计成功！共统计'+str(r)+'个长度为1-5的潜在词串，详见word_fre.txt文件'
            tk.messagebox.showinfo('提示',infor)
        except:
            tk.messagebox.showerror('警告','发生错误，请重新尝试')