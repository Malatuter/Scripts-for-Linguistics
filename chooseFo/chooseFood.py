import random

#每行仅限添加一个选项
foodlist = '''泰国菜
东南亚
alfafa
美心
SU
谭仔
彩面
日之苑
阿一猪扒
绿野仙踪
西宝城日料
萨莉亚
...去深圳
'''



content = foodlist.split("\n")
#print(content)
choice = random.randint(0,len(content)-1)
print("今天吃",content[choice])

