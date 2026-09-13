```
import random

secret = random.randint(1, 10)   # 随机生成 1-10 的数
count = 0                         # 记录猜了几次
print("我想了一个 1-10 的数字，来猜猜看！")

while True:
    guess = int(input("你猜: "))
    count = count + 1

    if guess > secret:
        print("大了")
    elif guess < secret:
        print("小了")
    else:
        print(f"猜对了！答案是 {secret}，你一共猜了 {count} 次")
        break
```
