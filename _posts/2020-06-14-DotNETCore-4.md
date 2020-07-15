---
layout: post
title: '.NET Core前后端分离(3) - ORM的选用(SqlSugar) + Code First初始化数据库'
date: 2020-06-14
author: HANABI
color: rgb(91,47,107)
tags: [.NET Core]
---

> 经过之前的步骤，已经设置好了配置文件的读取方法，现在让我们来设置ORM，这里我们选用[SqlSugar](https://github.com/sunkaixuan/SqlSugar)作为本项目的ORM

## 构建Model层

因为要使用*Code First*,先在解决方案下新增类库项目*Hanabi.Flow.Model*，引入ORM包*sqlSugarCore*，会在这里构建项目的*Model*层，在其中添加文件*RootEntity.cs*，内容为

```c#
public class RootEntity
{
    /// <summary>
    /// ID
    /// </summary>
    [SugarColumn(IsNullable = false, IsPrimaryKey = true, IsIdentity = true)]
    public int Id { get; set; }
    
}
```
这是所有*Models*的基类，因为之后的所有*Models*都会具有*Id*列，所以它们都会继承这个类

新建类*UserRole.cs*以及*UserInfo.cs*，分别作为用户角色类以及用户信息类

这里只写出*UserRole.cs*的内容，注意详细定义每个字段的*SugarColumn*特性即可

```c#
/// <summary>
/// 权限ID
/// </summary>
[SugarColumn(IsNullable = false)]
public int RoleId { get; set; }

/// <summary>
/// 角色名称
/// </summary>
[SugarColumn(ColumnDataType = "nvarchar",Length = 20,IsNullable = true)]
public string Name { get; set; }

/// <summary>
/// 角色描述
/// </summary>
[SugarColumn(ColumnDataType = "nvarchar", Length = 50, IsNullable = true)]
public string Description { get; set; }

/// <summary>
/// 创建者ID
/// </summary>
[SugarColumn(IsNullable = true)]
public int? CreateId { get; set; }

/// <summary>
/// 创建时间
/// </summary>
[SugarColumn(IsNullable = false)]
public DateTime? CreateTime { get; set; } = DateTime.Now;

/// <summary>
/// 修改ID
/// </summary>
[SugarColumn(IsNullable = true)]
public int? ModifyId { get; set; }

/// <summary>
/// 修改时间
/// </summary>
[SugarColumn(IsNullable = true)]
public DateTime? ModifyTime { get; set; } = DateTime.Now;

/// <summary>
/// 逻辑删除
/// </summary>
[SugarColumn(IsNullable = true)]
public bool? IsDeleted { get; set; }
```

## 定义数据库上下文类

新建Data文件夹， 在这里面新增数据库上下文类*MyContext*，主要用于建立和数据库之间的连接，以及程序启动时数据库的生成，其中*object.ObjToEnum*是一个自定义的扩展方法，之后可以在项目中查看具体写了啥

```c#
using Hanabi.Flow.Common.Helpers;
using SqlSugar;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;

namespace Hanabi.Flow.Data
{
    public class MyContext
    {
        private SqlSugarClient _db;
        private static string _connectionString;
        private static DbType _dbType;

        /// <summary>
        /// 数据连接对象 
        /// Blog.Core 
        /// </summary>
        public SqlSugarClient Db
        {
            get { return _db; }
            private set { _db = value; }
        }

        /// <summary>
        /// 连接字符串 
        /// Blog.Core
        /// </summary>
        public static string ConnectionString
        {
            get { return _connectionString; }
            set { _connectionString = value; }
        }
        /// <summary>
        /// 数据库类型 
        /// Blog.Core 
        /// </summary>
        public static DbType DbType
        {
            get { return _dbType; }
            set { _dbType = value; }
        }

        public MyContext()
        {
            string connectionString = AppSettings.app("DBSetting", "DBString");
            string dbType = AppSettings.app("DBSetting", "DBType");
            _connectionString = connectionString;
            _dbType = dbType.ObjToEnum<DbType>();
            if (string.IsNullOrEmpty(connectionString))
            {
                throw new ArgumentNullException("数据库连接字符串为空");
            }

            _db = new SqlSugarClient(new ConnectionConfig()
            {
                ConnectionString = connectionString,
                DbType = _dbType,
                IsAutoCloseConnection = true,
                InitKeyType = InitKeyType.Attribute,//mark
                MoreSettings = new ConnMoreSettings()
                {
                    IsAutoRemoveDataCache = true
                }
            });
        }

        public void GeneratorData()
        {
            Console.WriteLine("正在初始化数据库...");
            _db.DbMaintenance.CreateDatabase();
            Console.WriteLine("数据库初始化完毕");

            Console.WriteLine("正在遍历Models");
            var modelTypes = Assembly.GetExecutingAssembly().GetTypes()
                                                       .Where(type => type.IsClass && type.Namespace == "Blog.Core.Model.Models")
                                                       .Select(type => type)
                                                       .ToList();

            modelTypes.ForEach(model =>
            {
                if (!_db.DbMaintenance.IsAnyTable(model.Name))
                {
                    Console.WriteLine($"正在建{model.Name}表");
                    _db.CodeFirst.InitTables(model);
                }
            });

            Console.WriteLine("建表完成");
        }

        /// <summary>
        /// 功能描述:根据实体类生成数据库表
        /// 作　　者:Blog.Core
        /// </summary>
        /// <param name="blnBackupTable">是否备份表</param>
        /// <param name="lstEntitys">指定的实体</param>
        public void CreateTableByEntity<T>(bool blnBackupTable, params T[] lstEntitys) where T : class, new()
        {
            Type[] lstTypes = null;
            if (lstEntitys != null)
            {
                lstTypes = new Type[lstEntitys.Length];
                for (int i = 0; i < lstEntitys.Length; i++)
                {
                    T t = lstEntitys[i];
                    lstTypes[i] = typeof(T);
                }
            }
            CreateTableByEntity(blnBackupTable, lstTypes);
        }

        /// <summary>
        /// 功能描述:根据实体类生成数据库表
        /// 作　　者:Blog.Core
        /// </summary>
        /// <param name="blnBackupTable">是否备份表</param>
        /// <param name="lstEntitys">指定的实体</param>
        public void CreateTableByEntity(bool blnBackupTable, params Type[] lstEntitys)
        {
            if (blnBackupTable)
            {
                _db.CodeFirst.BackupTable().InitTables(lstEntitys); //change entity backupTable            
            }
            else
            {
                _db.CodeFirst.InitTables(lstEntitys);
            }
        }
    }
}
```

接着我们在*Startup*中将其注册到服务

*
services.AddScoped<MyContext>();
*

接着在*Hanabi.Flow.API*项目中添加文件夹*Extensions*，添加文件*DataGenerator.cs*，在这里调用*MyContext*里的方法，实现启动时生成数据库

```c#
public static void UseDataGenerator(this IApplicationBuilder app, MyContext myContext)
{
    myContext.GeneratorData();
}
```

最后，在*Startup.cs*文件的*Configure*函数使用短路中间件(*UseEndpoints*)的后面使用这个新添加的中间件

```c#
app.UseDataGenerator(myContext);
```

启动程序，发现数据库已经在启动时被正确初始化了：

![](/assets/img/dotnetcore-6.JPG)

连接数据库查看，确实已经生成了库和表，至此，利用*SqlSugar*作为ORM，并实现*Code First*就完成了

![](/assets/img/dotnetcore-7.JPG)


