import random
with open("foodlist.txt") as f:
	content = f.readlines()
choice = random.randint(0,len(content))
print("今天吃",content[choice])

