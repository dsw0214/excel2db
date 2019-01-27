# excel2db
Excel 和 Database 相互转换工具

## 主要模块

```
1. 使用Configparser模块读取配置信息
2. 使用Argparse模块处理参数信息
3. 使用Sqlalchemy模块进行Engine创建
4. 使用Pandas模块进行Excel和数据库操作
5. 使用Logging模块进行操作日志记录
```

## 目录说明
```
├── Excel2db.py #数据操作主代码
├── LICENSE
├── README.md
├── config  # 代码使用的参数配置
│   ├── define.ini  # 代码使用的参数配置
│   ├── excel2db.sql    # 测试数据库(mysql)建表sql
│   └── logging.conf    # logging配置参数
├── db_back # 数据库备份目录
│   └── Department.xls
├── excel   # 源数据目录
│   └── Department.xls
├── lib
│   ├── Log.py
│   ├── __init__.py
├── logs
│   ├── logging.log
│   └── rotating_logging.log
└── requirements.txt    # 运行必须安装的核心模块

```
> 运行的时候，根据自己需要修改配置config/define.ini信息

## 参数说明
使用 `#python Excel2db.py -h` 查看参数

```
# python Excel2db.py -h
usage: Excel2db.py [-h] [--version] --operation {1,2,3,4} [--table TABLE]

Database and Excel Interoperate

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --operation {1,2,3,4}, -opt {1,2,3,4}
                        Operation Detail:
                            1:Load In Single Table By Table Excel Name
                            2:Load Out Single Table By Table Name
                            3:Load In All Files By Configure Source Path
                            4:Load Out All Tables By Configure Dbname
  --table TABLE, -t TABLE
                        Table Params Details
                           1.The name of the Excel to be operated:
                           2.There must be corresponding table names
                               in the configured database.
                           (When the name of the input table is empty,
                            all tables in the configuration database
                            are operated by default. )
```
参数描述：
```
-v  读取版本号信息
-opt 操作的类型：
    1）单表导入操作
    2）单表导出操作
    3）数据库全表导入操作
    4）数据库全表导出操作
-t  单表操作需要操作的表名
```
## 使用方式

创建环境获取代码（建议使用Python virtualenv)
```
1. virtualenv excel2db
2. cd excel2db
3. source bin/activate
4. git clone https://github.com/dsw0214/excel2db.git
5. cd bilibili-video-Excel2db
6. pip install -r requirements.txt
7. python Excel2db.py -h
8. deactivate
```

* 单表导入

`python Excel2db.py -opt 1 -t Department`

* 单表导出

`python Excel2db.py -opt 2 -t Department`

* 配置文件下面全部*.xls导入到数据库

`python Excel2db.py -opt 3`

* 配置文件下（指定的数据库）全部表名导出

`python Excel2db.py -opt 4`

## 开源协议
本代码采用[MIT](https://github.com/dsw0214/excel2db/blob/master/LICENSE "MIT")许可证。