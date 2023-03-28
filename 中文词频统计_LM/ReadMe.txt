介绍：本程序所实现的功能如下
(1) 对一个文件夹下所有文件，统计字符频度，结果输出到文件，
    可以分类统计汉字字符、字母字符、数字字符和其他字符
    可以按照内码、音序和频次排序
    文件夹路径在‘字频统计’界面下输入，提供是否只输出汉字字符和按照何种标准排序的选项
(2) 对一个文件夹下所有文件，抽取词表（每个词条附带频度信息，含单字词，词条最长为5）。
    输出一个带有frequency,entropy和combinability的中间文件
    输出一个按指定标准（内码、音序、频次）排序的词表
    文件夹路径在‘词频统计’界面下输入，提供按照何种标准排序的选项
注：本程序同时支持unicode、utf8和gbk三种编码
    测试所用文件夹为./测试文档，其中包括三种编码格式的txt文本，以及课程所提供的199801.txt语料
    测试所生成字频统计文件为char_fre.txt,词频统计文件为word_fre.txt

关于词频统计及词表抽取：
1. 词频统计所用的算法为Nagao算法
    将文本以非汉字字符为边界切分，存入list表，再由切分结果生成P表、L表及Ngram表（如果生成P表所使用的字符串过长，会带来极大的内存空间代价）
2. 词表抽取分为计算entropy、combinability及筛选三个步骤
    1) entropy计算
    本次作业尝试采用了两种方式计算entropy，一种是用不同长度4左右邻字并记录，两种方法所需的时间代价均较大，以测试文本（199801.txt）为例，前一种
    方法耗时约在30-40秒之间，后一种方法约在20-30秒之间，因此会造成运行时较长时间的等待
    使用第二种方法，整个程序耗时约为38秒，因此entropy的计算占用了大量时间，是本程序有待改进的部分
    2）combinability计算
    按照课件所给方法计算
    3）筛选
    筛选标准为词频>2，combinability<0.01, 左右邻熵均大于1.0且差值不超过2
    在比较左右邻熵的情况下，抽取词数为40382，不比较的情况下，词数为42715
    一个可能的原因是，对于一些不成词且位于词首或词尾的语素或语素组，其左右邻熵可能产生较大的不平衡，
    因此限制左右邻熵差值能够对这样的不成词字符串进行过滤

不足：
1.由于调试代码占用了较多时间，还没来得及对词表进行人工抽样检查正确率，希望在稍后补上
2.对于作业要求中所说的“亿美元”“日电记者”“月中旬”“记者龚”这样的单位，在测试所抽取的词表中并没有被识别为词，但不能够解释原因是什么

运行本程序所需模块参见module_list.txt

项目组成：

Main.py #主程序入口

Frame.py #窗口界面
    class frame(tk.Tk):
        def setup(self):#主界面生成
        def instruction(self):#显示程序说明
        def windowChar(self):#创建字频统计窗口
        def queryChar(self,dir,order,flag):#字频统计,统计dir下的所有文件的潜在词频，并按指定排序方式order进行排序,flag指示是否需要纳入非汉字字符
        def windowWord(self):#创建词频统计窗口
        def queryWord(self,dir,order):#词频统计，统计dir下的所有文件的潜在词频，并按指定排序方式order进行排序

FileOperator.py  #文件操作
    class fileOp() #文件操作类
        def walkDir(dirpath) #遍历文件夹地址dirpath下所有文件，并返回储存文件名的list。若文件夹地址不存在，返回False。
        def decode(self,filename):#输入文件名，返回文件编码格式。文件不存在时，返回False。`
        def tran_code(self,filename,newcode):#输入文件名，将文件编码格式转换为指定格式(GBK,utf8,unicode)。文件不存在时，返回False。
        def writeDict(self,d,f,flag='w',comments=None):#将字典以每行一条key value记录的格式写入txt文档f，默认为写入模式，
        #可设置为追加模式(flag='a'),亦可在文件开头添加注释comments

CharFrequency.py #字频统计
        class charF():
            def sort(self,result,index): #对list(result)按index从大到小排序，result为字典
            def sort_V(self,result):#对字典result进行排序，排序标准为字典的值（从大到小）
            def count_file(self,filename):#统计单个文件数字字符、汉字字符、字母字符及其他字符频次
            def count_dir(self,dirname,order=None): #统计一个文件夹下所有文件的字符（仅支持txt文件）
            #并根据指定排序要求order(unicode、gbk、UTF8，拼音、frequency)对汉字字符进行排序
            #返回四个字典格式的结果，{char:frequency}，默认按字频排序
            def saveResult(self,result,file): #将统计结果result保存进file文件中

Nagao.py #使用Nagao算法进行串频统计，并计算熵值、combinability进行筛词，筛词标注为frequency>2,entropy>1.0,
         #combinability<0.01，且左右邻熵值差不超过2
    class nagao():
        def readFile(self,file):#加载文件
        def sort(self,result,index): #对list(result)按index从大到小排序，result为字典
        def sort_V(self,result):#对字典result进行排序，排序标准为字典的值（从大到小）
        def createP(self):#创建Ptable
        def createL(self):#创建Ltable
        def shareStr(self,s1,s2):#输出两个字符串相同最左字串大小
        def getNgram(self,n,m=1):#获取出现频率>2的，长度在m到n之间的字符串频次
        def countFile(self,f,n,m=1):#统计文件f中长度在m到n之间的潜在词，返回一个字典
        def countDir(self,dir,n,m=1,index='frequency'):#统计文件夹dir中长度在m到n之间的潜在词，返回一个字典
        def sortInfor(self,index):#根据index对筛选出的词表进行排序
        def entropy(self,n,m):#计算所有待选词串（f>2)的左右邻熵值，返回一个字典
        def combinability(self):#计算combinability以反映待选词条的内部凝固度
        def filter(self,fre=3,com=0.001,le=1.0,re=1.0):#筛选文件中的潜在词，要求:频次大于3,
            #combinability小于0.001，左右熵值均大于1.0且差值不超过2
