import random

#每行仅限添加一个选项
foodlist = '''泰国菜
东南亚
美心
冰室
彩面
绿野仙踪
萨利亚
日之苑
越北
越大哥
麦当劳
阿元来了
上海姥姥
华记车仔面
阿一猪扒
可可店
好吃的日料
mos burger
...去深圳
'''



content = foodlist.split("\n")
#print(content)
choice = random.randint(0,len(content)-1)
print("今天吃",content[choice])

