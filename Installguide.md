  * 安装 [Django 1.0 beta1](http://www.djangoproject.com/download/1.0-beta-1/tarball/)，如果你不想安装这个版本，请将这个版本的Django目录放到 Tmiiter 的目录下面
  * 安装 [PIL 1.1.6](http://www.pythonware.com/products/pil/),安装方法见官方
  * 选择数据库，Sqlite3 或 PostgreSQL 或 MySQL
> Sqlite 安装说明
    * 安装 [pysqlite](http://initd.org/tracker/pysqlite)
    * 我们的源代码里面默认就带有Sqlite的数据库文件，在 **tmitter/db** 下面，请直接把 **tmitter.db** 删除掉。

> PostgerSQL 安装说明
    * 如果你使用 PostgreSQL 的话，请先安装 PostgreSQL 并创建数据库 tmitter
    * 修改 settings.py 的数据库配置部分的用户名密码,请将下面一段替换相应的地方
```
            DATABASE_ENGINE = 'postgresql3'
            DATABASE_NAME = 'tmitter'
            DATABASE_USER = 'monster' # 请将 monster 改为你的PostgreSQL账号的用户名
            DATABASE_PASSWORD = '123123' # 请将 12123 改为你的PostgreSQL账号的密码
            DATABASE_HOST = '127.0.0.1' # 请将 127.0.0.1 改为你的PostgreSQL的服务器地址
            DATABASE_PORT = '' # 这里是 PostgreSQL的端口号，如果是默认的这里就留空
```
    * 安装 [psycopg](http://initd.org/tracker/psycopg)

> MySQL 安装说明
    * 下载安装 MySQL,并创建 tmitter 数据库，并修改 settings.py 把 DATABASE\_ENGINE 的值改为 'mysql' 其它后面的 DATABASE相关的设置与 PostgreSQL的设置基本类似
    * 安装 [mysql-python](http://sourceforge.net/projects/mysql-python)
  * 打开命令窗口，并进入tmitter源代码目录，执行 `manage.py syncdb` 命令，根据提示完成操作。这样 Django 为自动为我们创建相关的表。
  * 运行 `manage.py runserver` 将会开始运行web服务器，最后打开提示出来的地址，如：http://127.0.0.1:8000/