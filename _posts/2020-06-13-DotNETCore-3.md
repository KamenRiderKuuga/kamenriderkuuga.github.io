---
layout: post
title: '.NET Core前后端分离(2) - 配置文件与变量'
date: 2020-06-13
author: HANABI
color: rgb(91,47,107)
tags: [.NET Core]
---

> 在代码中，为了避免代码复用，以及在没有编译条件时能调整程序内部的一些设置，常常需要有一个配置中心，方便快速更改整个程序的全局变量，所以我们先来编写好配置中心的相关代码

## 在代码中编写全局变量的一些方法

1. 使用定义全局静态类，添加静态变量，方便修改，全局可用
2. 采用依赖注入的方式在项目中注入一个*Singleton*的变量，使其在整个项目周期中都可以使用

这两种，都是直接写在代码中的配置，所以我们需要一种可以直接通过非代码文件操作配置，并方便快速取用的方法

项目目录中，默认有*appssettings.json*文件，用于储存一些项目配置，所以我们需要将取用的方式封装成方便我们取用的方式

## 通过封装官方接口来注入配置

为了让项目层次更清晰，我们先在当前解决方案添加一个新的类库，取名*Hanabi.Flow.Common*，在类库下创建一个新的*Helpers*文件夹，并添加文件，名为*AppSettings.cs*

在新建的类库项目中安装*Microsoft.Extensions.Configuration.Json*包，在新建文件的类中添加构造函数，并传入*IConfiguration*，此时代码为

```c#
static IConfiguration Configuration { get; set; }

public AppSettings(IConfiguration configuration)
{
    Configuration = configuration;
}
```

这里的*IConfiguration*是之后会在项目启动注入服务时传入的，这里定义一个方函数，方便我们快速获取*Configuration*中的内容

```c#
/// <summary>
/// 封装要操作的字符
/// </summary>
/// <param name="sections">节点配置</param>
/// <returns></returns>
public static string app(params string[] sections)
{
    try
    {

        if (sections.Any())
        {
            // 获取配置中的对应内容
            return Configuration[string.Join(":", sections)];
        }
    }
    catch (Exception) { }

    return "";
}
```

最后，我们在主项目中引用当前类库项目，整个项目的*Startup.cs*处对这个类进行注入，在*ConfigureServices*函数中增加内容

```c#
services.AddSingleton(new AppSettings(Configuration));
```

## 在项目中使用注入好的配置类

在默认的*Controller*中，添加新的函数，测试注入的配置类已经生效，正确获取到了默认配置文件的内容

```c#
/// <summary>
/// 获取配置文件内容
/// </summary>
/// <returns></returns>
[HttpGet]
public string GetSetting()
{
    return AppSettings.app("Logging", "LogLevel", "Default");
}
```