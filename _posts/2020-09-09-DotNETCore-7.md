---
layout: post
title: '.NET Core开源框架盘点'
date: 2020-09-09
author: HANABI
color: rgb(91,47,107)
tags: [.NET Core]
---

> 本来这篇是想用来记录WTM的使用方法，后面发现没有什么值得额外讲的，用法的话看官方文档已经可以了解得很清楚了，所以改成在这篇里盘点一些开源的.NET Core框架

## WTM框架

### 为什么使用WTM框架

*WTM(WalkingTec MVVM)*(这槽点十足的名字，作者肯定故意的)是一个`.NET Core`开源开发框架，主打优势是快速开发，即宣传的"低码开发，快速实现"，从这个设计理念可以看出来，非常适合小团队，个人开发者快速出成品的需要，具体使用体验深入了解之后才知道



### 创建第一个WTM项目并自动生成第一个业务模块

这几个步骤通过[官方文档](https://wtmdoc.walkingtec.cn/#/QuickStart/FirstProject)上的指引可以很快完成

1. 线上一键生成解决方案
2. 然后建立Model，自动生成数据表[^1]
3. 用框架自带的代码生成器生成基础代码

### 具体功能细节与配置

[官方文档](https://wtmdoc.walkingtec.cn)都有说，也没有需要特别理解的部分，看文档即可


[^1]: 按照官方文档的说法，暂时不支持自动更新数据库，当修改了Model，可以把原有数据库删掉重新生成新的，如果不方便删掉现有数据库，也有一些[其他方法](https://wtmdoc.walkingtec.cn/#/Data/Migration)