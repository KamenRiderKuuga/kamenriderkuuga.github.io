---
layout: post
title: 'Python爬虫基础之广西人才网的信息爬取(3) - 分词统计'
date: 2020-05-24
author: HANABI
color: rgb(228,210,196)
tags: Python
---
> 在通过异步爬取提升了爬取速度之后，最后来扩展一下，进一步爬取每个工作的详情并利用分词库来对具体工作内容进行分词统计

## 准备工作

在上次爬取的过程中，我们异步获取了所有IT类工作的标题，在过程中也得了它们的详情页链接，这里在之前的基础上获取到每个链接的详情页，利用分词库进行分词，从而统计出每种编程语言在所有岗位中的占比，为此我们要用到中文分词库*[结巴分词](https://github.com/fxsjy/jieba)*，其安装方法和用法示例在页面中都有介绍。


## 编写代码

代码都放到了[这里](https://github.com/GadHao/gxrc_crawler)，在上次的基础上，主要加了在遍历岗位标题时打开详情页并记录详情页内容的代码：

```python
            # 打开详情页
            detailPage = await fetch(session, "https:" + href)
            jobDetail = BeautifulSoup(detailPage, 'lxml').find(
                "pre")
            global content
            content += str(jobDetail)
```

以及最后的分词统计部分

```python
    time_end = time.time()
    counter = Counter()
    words = jieba.cut(content, cut_all=False)
    for word in words:
        wordCommn = word.lower()
        if wordCommn in jobList:
            counter[wordCommn] += 1

    print('广西人才网IT岗统计结果(词频)')
    print('总岗位数量:' + str(len(jobsNum)))
    common = counter.most_common(len(jobList))
    for k, v in common:
        print(f"{k}  {v}次")
```

## 运行结果

```
广西人才网IT岗统计结果(词频)
总岗位数量:2233
java  665次
javascript  493次
sql  454次
css  446次
php  340次
js  263次
c#  202次
c++  154次
python  142次
go  13次
vb  6次
ruby  6次
swift  5次
```

## 总结

这次的代码其实很早就写好了，但是一直想不到有什么特别值得详细写的地方，加上最近比较忙，就没有更新这篇上去。

总的来说，使用Python写爬虫是一个非常舒服的过程，上手快，写出可用的爬虫的速度也快，对于爬虫这种随时可能因为爬取的网站结构或者反爬措施变化需要调整甚至全部重写的工具来说，选Python肯定不会错。

因为网络教程和使用范例的丰富，各种用来编写爬虫的库的使用方法已经不再是难点。对于爬取过程来说，最重要的还是网站结构的分析，以及请求头，Cookies都要按不同网站来做出调整，以及如何在数据量较大时，对整个爬取过程做优化，这才是最重要的地方。

## Python小工具合集

因为用Python来写一些小工具或者短时间使用的工具实在太方便了，最近就写了好几个，建了一个*repository*，之后会把这些小工具都更新到这里，供个人备忘以及大家参考
[python-little-tools](https://github.com/GadHao/python-little-tools)