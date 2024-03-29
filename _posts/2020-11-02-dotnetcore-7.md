---
layout: post
title: 'Identity Server 4原理和实战学习笔记 - OAuth 2.0协议'
date: 2020-11-02
author: HANABI
color: rgb(54,59,64)
tags: [.NET Core]
mermaid: true
category: [编程框架, ASP.NET Core]
---

> 学习.NET Core权限认证相关知识，看的是杨旭老师在B站上的教程，先开始了解OAuth 2.0协议

## 什么是OAuth 2.0协议

OAuth 2.0协议是一种**委托协议**，可以让那些控制资源的人允许某个应用**代表**他们来访问他们控制的资源。这个应用从资源的所有者那里获得*授权(Authorization)*和*access token*，随后就可以用这个*access token*来访问资源

这里有两点值得注意的，其一，OAuth 2.0是一种委托协议，什么叫做委托协议呢

```mermaid
graph LR;
用户--委托--> 客户端应用--访问-->受保护资源
```

**委托协议**

上面的客户端应用可以是WPF，ASP.NET Core MVC等客户端项目，受保护的资源可以是受到保护的ASP.NET Core Web API，当然这里只是举例，主要想说的是对委托协议这个词的解释，一个用户想要访问一些数据资源或者一些功能，必须要使用客户端应用，客户端再去访问这些受保护的资源。

这里可以看到，是用户允许了客户端应用去访问这些受保护的资源，客户端代表用户去做这件事情。所以这个代表的过程，也就是委托。

注意这里不是假冒或者模仿，什么叫做假冒或者模仿呢，指的是客户端或者应用，复制了一份用户的用户名，密码等凭证，从而获得了相应的授权。在这个过程，用户的用户名，密码等信息就泄露给应用了。而我们在这里说的OAuth 2.0协议是一个委托协议，它不会假冒或者模仿用户，所以客户端并没有得到用户的用户名和密码或其他凭证。这样做是比较合理的，因为有的客户端应用，我们是不一定会信任它的。



**授权和认证**

OAuth 2.0协议只是用来做授权的协议，授权的意思就是授予各种应用进行某些操作的权力，它无法做身份认证，身份认证的意思就是让访问的资源知道你是谁，关于这点我们通过OpenId Connect协议实现

|      | 授权       | 认证           |
| ---- | ---------- | -------------- |
| 协议 | OAuth 2.0  | OpenId Connect |
| 含义 | 你能干什么 | 你是谁         |



## 如何进行委托

资源所有者(*Resource Owner*)是如何委派权限给客户端应用(*Client*)，使其访问受保护的资源(*Resource Server*)呢，在这里我们就需要一个桥梁，叫做授权服务器(*Authorization Server*)，其在物理上，可以和我们的资源服务器放到一起，但是通常，是不放在一起的，整个获取数据的过程如图：



```mermaid
sequenceDiagram;
Client -->> Resource Owner:Authorization Request
Resource Owner -->> Client:Authorization Grant
Client -->> Authorization Server:Authorization Grant
Authorization Server -->> Client:Access Token
Client -->> Resource Server:Access Token
Resource Server -->> Client:Protected Resource
```

流程解释：用户(*Resource Owner*)在操作客户端软件(*Client*)的时候，这个软件突然需要访问一个受保护的资源，但是应用程序没有权限，所以应用程序需要先获得这个权限。它可能有两种方式来获得这个权限，其一是从用户处直接获得权限，另外就是让授权服务器(*Authorization Server*)作为一个中介，客户端软件再间接地获得这个权限。

如何获取到权限：想要使用授权服务器这个中介，客户端软件就需要把资源所有者发送到授权服务器。所谓的发送实际上就相当于一个跳转或者重定向，让资源所有者重定向到授权服务器，授权服务器通常会有一个页面，给客户端软件授权，所谓授权，就是授权服务器发布具有特定目的(通常是一部分的功能权限，或者称为*Scope*，一定范围内的功能)的安全凭据(*Access Token*)给应用。用户被重定向到资源服务器就可以直接给客户端授权吗，其实还不可以。首先需要进行身份认证，即前面提到过的*OpenId Connect*协议做的事情



## 授权的类型

授权类型(*Authorization Grant Type*)，首先授权这个过程可以获得一个代表资源所有者权限的凭据，*OAuth 2.0*中常用的授权类型有：

- Authorization Code：采用授权服务器作为客户端软件和资源所有者的中介来获取权限，不是直接从资源所有者处获得授权，授权服务器把资源所有者重定向回到应用时，带的这个临时的凭据，就是Authorization Code，或者说授权码，它代表资源所有者委托给客户端应用的权限，通常是通过跳转时前端URL带的参数传回。接着后端使用这个授权码进行客户端身份认证，因为得到的Access Token是直接发送到客户端应用的，不经过资源所有者的浏览器，所以对于ASP.NET Core MVC这种服务器端的Web应用来说是非常适合的，其不会把Aceess Token暴露给包括资源所有者在内的外界角色
- Implicit
- Resource Owner Password Credentials
- Client Credentials
- Device Code
- Refresh Token

另外其还定义了一个扩展机制，以便定义其他类型的授权

