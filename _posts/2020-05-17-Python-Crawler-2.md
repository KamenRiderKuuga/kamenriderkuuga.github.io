---
layout: post
title: 'Python爬虫基础之广西人才网的信息爬取(2) - 异步爬虫'
date: 2020-05-17
author: HANABI
color: rgb(228,210,196)
tags: Python
---
> 经过之前的爬取，已经了解了网页的爬取流程，现在来了解异步爬取

## 为什么要进行异步爬取

[上一篇](https://colasaikou.com/2020/05/15/Python-Crawler-1.html)中，我们的代码是从上往下写的，逻辑比较清晰，先获取到每一页岗位的*url*，然后在*for*循环中获取每一页的岗位列表，再进行分析与统计，这样的代码虽然没有问题，但只是相当于一个人在飞快浏览网站内容然后做记录，我们的代码只是加速了这个过程，没有发挥爬虫的最大优势，如果能让程序变成很多人在同时帮我浏览并分析数据，那速度肯定能提高很多，带着这种想法，我们来试试用异步的方法执行爬取


## 了解需要用到的库

### asynico库

这次我们需要用到的库主要有*asyncio*和*aiohttp*两个库，其中*asyncio*库的官方文档简介如下
> asyncio 是用来编写 并发 代码的库，使用 async/await 语法。
> asyncio 被用作多个提供高性能 Python 异步框架的基础，包括网络和网站服务，数据库连接库，分布式任务队列等等。
> asyncio 往往是构建 IO 密集型和高层级 结构化 网络代码的最佳选择。

1.首先来了解*asyncio*，我们用下面这段代码来帮助我们理解

```python
import asyncio
import time

time_format = '%Y-%m-%d %X'


async def printTime(taskname):
    print(f"{taskname}开始时间:{time.strftime('%X')}")
    await asyncio.sleep(10)


async def main():
    print(f"开始时间:{time.strftime('%X')}")
    task1 = asyncio.create_task(printTime("任务一"))
    task2 = asyncio.create_task(printTime("任务二"))
    task3 = asyncio.create_task(printTime("任务三"))
    await task1
    task4 = asyncio.create_task(printTime("任务四"))
    await task2
    await task3
    await task4
    print(f"结束时间:{time.strftime('%X')}")

# 输出结果
# 开始时间:18:10:39
# 任务一开始时间:18:10:39
# 任务二开始时间:18:10:39
# 任务三开始时间:18:10:39
# 任务四开始时间:18:10:49
# 结束时间:18:10:59

asyncio.run(main())
```

可以看到，我们定义了一个函数`printTime()`，函数功能是输出当前任务的开始时间并等待十秒，从输出的结果可以看到，前面三个任务被同时开始了，第四个任务在他们开始的十秒之后也开始了，也就是说在这三个任务同时完成并且结束之后，任务四开始执行

如何来理解这样的运行结果呢，通过分析代码中的关键字和*asyncio*库的用法就可以很容易明白：

首先，在要运行的函数前面使用*async*来进行声明，可以将其指定为*协程*，*协程*不能直接调用并执行，在程序的入口部分，我们用`asyncio.run()`来异步执行被标记为*协程*的`main()`，在内部，使用*await*来对可等待对象，可等待对象包括*协程*，*任务*和*Futures*

每当程序运行到用*await*来进行等待的地方，会立即并发执行当前所有被创建的*任务*和*协程*，所以其实上面的代码可以简写，只要*任务*被创建，就在等待运行，使用一次*await*进行等待，所有*任务*就会并发执行，我们调整之前代码中的`main()`函数，可以看到输出结果发生了改变

```python
async def main():
    print(f"开始时间:{time.strftime('%X')}")
    asyncio.create_task(printTime("任务一"))
    asyncio.create_task(printTime("任务二"))
    asyncio.create_task(printTime("任务三"))
    await printTime("任务四")
    print(f"结束时间:{time.strftime('%X')}")

# 输出结果
# 开始时间:18:10:39
# 任务四开始时间:18:10:39
# 任务一开始时间:18:10:39
# 任务二开始时间:18:10:39
# 任务三开始时间:18:10:39
# 结束时间:18:10:49
```

当使用*await*时，马上调用任务四，并且之前队列中被创建的任务也全部异步开始，所以会出现这样的输出结果


### aiohttp库

关于*aiohttp*库，其主要是配合*asycio*使用，达到异步请求的目的，[官方示例](https://docs.aiohttp.org/en/stable/)已经用比较直观的代码介绍了用法

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

这里`main()`函数的调用可以不用太在意，是另一种异步启动协程的办法，这里用我们之前的写法`asyncio.run(main())`也是一样的效果，*aiohttp*库内的函数支持协程的特性，让其可以很好和异步编程配合

代码中使用`aiohttp.ClientSession()`创建了一个`session`对象，对于这个对象，官方文档这样说：
> 不要为每个请求都创建一个会话。大多数情况下每个应用程序只需要一个会话就可以执行所有的请求。 每个会话对象都包含一个连接池，可复用的连接和持久连接状态(keep-alives，这两个是默认的)可提升总体的执行效率。

可以理解成，通过反复使用创建的`session`对象并*keep-alives*，就能在单次会话中提高整体请求页面的速率，因为不用在每次请求时再建立新连接


## 开始编写代码

在了解了这两个库之后，我们对之前做的爬虫代码进行改善，这里直接上代码：

```python
from bs4 import BeautifulSoup
import urllib.request
import aiohttp
import asyncio
from collections import OrderedDict
import time

# IT类工作地址
listTypes = ['5480', '5484']
jobsNum = []
jobList = ["c#/.net", "java", "php", "web"]
dicResult = OrderedDict()
urls = []

# 伪装浏览器头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36'
}

# 获取网页（文本信息）


async def fetch(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    async with session.get(url, headers=headers) as response:
        return await response.text()


def getData(page):
    soup = BeautifulSoup(page, 'lxml')
    searchResultPage = soup.find_all(name='div', attrs='rlOne')
    bolTypeRight = False
    for job in searchResultPage:
        tag_a = job.find('a')
        href = tag_a.get('href')
        company = job.find('li', 'w2').text
        salary = job.find('li', 'w3').text
        jobName = tag_a.text.lower()
        if href not in jobsNum:
            jobsNum.append(href)
            for jobType in jobList:
                if '-' in salary:
                    if '/' in jobType:
                        bolTypeRight = jobType.split(
                            '/')[0] in jobName or jobType.split('/')[1] in jobName
                    else:
                        bolTypeRight = jobType in jobName

                    if bolTypeRight:
                        if jobType not in dicResult.keys():
                            dicResult[jobType] = [int(salary.split('-')[0])]
                        else:
                            dicResult[jobType].append(
                                int(salary.split('-')[0]))

            print(company + " " + jobName + ":" + salary + " " + href)


# 处理网页
async def download(url):
    async with aiohttp.ClientSession() as session:
        page = await fetch(session, url)
        getData(page)

time_start = time.time()

for type_number in listTypes:
    url_prefix = 'https://s.gxrc.com/sJob?schType=1&expend=1&PosType=' + \
        type_number + '&page='

    # Request类的实例，构造时需要传入Url,Data，headers等等的内容
    request = urllib.request.Request(url=url_prefix + '1', headers=headers)
    first_page = urllib.request.urlopen(request)
    soup = BeautifulSoup(first_page, 'lxml')
    intLastPageNumber = int(soup.find('i', {"id": "pgInfo_last"}).text)
    urls.extend([url_prefix + str(i) for i in range(1, intLastPageNumber + 1)])


async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))

    for task in tasks:
        await task

    print('广西人才网IT岗统计结果(按岗位标题)')
    print('总岗位数量:' + str(len(jobsNum)))
    for resultKey, value in dicResult.items():
        print(resultKey + '岗位总数量:' + str(len(value)) +
              ',平均工资(按岗位最低工资为准):' + str(sum(value) / len(value)))

    time_end = time.time()
    print('time cost', time_end-time_start, 's')

asyncio.run(main())
```

值得注意的是，对于其中的这一段代码：

```python
async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))

    for task in tasks:
        await task
```

可以写成：

```python
async def main():
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))

    await asyncio.gather(*tasks)
```
这里不需要太过在意，把`asyncio.gather(*tasks)`起到的作用当作和第一种写法实现的相同即可，减少代码量，并发运行所有列表中的协程

但是如果写成：

```python
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))

    await(tasks[0])
```

发现程序运行到一半就停止了，只处理了一部分url，这是因为，虽然使用`await`时所有任务是会同时并发运行，但是我这里只等待了第一项，所以当第一条url完全处理完时，之后程序将不会再等待剩余协程的情况


## 对比非异步的版本

终于，我们的异步爬虫编写好了，我们在之前编写的代码和现在编写的代码文件中`import time`，在循环开始前加上`time_start = time.time()`，在统计完成后加上
```python
time_end=time.time()
print('time cost',time_end-time_start,'s')
```

通过对比两次的结果可以看到，爬虫的速度从90s左右变成了20s左右，提升非常巨大，由此可以可以看到，协程配合*aiohttp*提供的*session*，可以让爬虫的效率有质的飞跃！
