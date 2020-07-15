---
layout: post
title: '部署Vue+.NET Core前后端分离项目中遇到的问题'
date: 2020-06-04
author: HANABI
color: rgb(35,169,242)
tags: [.NET Core]
---

> 这里记录一些在部署项目过程中容易忘记的点，主要做备忘用

## Nginx

### 1.双击之后一闪而过

这个是在Windows中使用的时候出现的，双击*nginx.exe*之后一闪而过，打开任务管理器也没有相关进程，在浏览器中输入*localhost*也无法访问欢迎页面，检查之后才知道是因为niginx的所在路径存在中文，换了没有中文的路径之后启动，没有出现此问题

### 2.配置vue项目后刷新后出现404的问题
根据[官方文档](https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E5%90%8E%E7%AB%AF%E9%85%8D%E7%BD%AE%E4%BE%8B%E5%AD%90
)，调整*nginx.conf*

```
location / {
  try_files $uri $uri/ /index.html;
}
```

### 3.解决访问后端API时的跨域问题

在*nginx.conf*中添加内容，设置代理，如这里的设置把要访问的后端API代理到前端

```
location /api {
    proxy_pass http://localhost:8081;
}
```

## IIS

### 1.使用IIS部署后访问出现404的问题

根据[官方文档](https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E5%90%8E%E7%AB%AF%E9%85%8D%E7%BD%AE%E4%BE%8B%E5%AD%90
)

1. 安装 [IIS UrlRewrite](https://www.iis.net/downloads/microsoft/url-rewrite)
2. 在你的网站根目录中创建一个 `web.config` 文件，内容如下：
```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="Handle History Mode and custom 404/500" stopProcessing="true">
          <match url="(.*)" />
          <conditions logicalGrouping="MatchAll">
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
            <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
          </conditions>
          <action type="Rewrite" url="/" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

### 2.解决访问后端API时的跨域问题

在后端代码中使用*CORS*中间件允许前端访问后端项目

官方示例(.NET Core 3.1)：https://docs.microsoft.com/zh-cn/aspnet/core/security/cors?view=aspnetcore-3.1