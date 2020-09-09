---
layout: post
title: '.NET Core开源框架之WTM框架'
date: 2020-09-09
author: HANABI
color: rgb(91,47,107)
tags: [.NET Core]
---

> 工作原因，有一个项目用到了WTM框架，这里从官方文档和框架实现方式作为切入点，对整个框架的主要概念和用法进行了解

## 为什么使用WTM框架

*WTM(WalkingTec MVVM)*(这槽点十足的名字，作者肯定故意的)是一个`.NET Core`开源开发框架，主打优势是快速开发，即宣传的"低码开发，快速实现"，从这个设计理念可以看出来，非常适合小团队，个人开发者快速出成品的需要，具体使用体验如何，在深入了解之后才知道



## 创建第一个WTM项目并自动生成第一个业务模块

这几个步骤通过[官方文档](https://wtmdoc.walkingtec.cn/#/QuickStart/FirstProject)上的指引可以很快完成

1. 线上一键生成解决方案
2. 然后建立Model，自动生成数据表[^1]
3. 用框架自带的代码生成器生成基础代码





[^1]: 按照官方文档的说法，暂时不支持自动更新数据库，当修改了Model，可以把原有数据库删掉重新生成新的，如果不方便删掉现有数据库，也有一些[其他方法](https://wtmdoc.walkingtec.cn/#/Data/Migration)