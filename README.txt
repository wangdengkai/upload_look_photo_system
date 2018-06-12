项目介绍:
项目名称：简单的电子相册系统。
实现功能：1  用户注册登录
        2   用户上传图片
        3   用户查看图片

使用技术：1  flask
        2   python
        3   mysql
        4   jquery
        5   html
        6   css



1   搭建静态页面,文件名：index.html
2   设置css格式,文件名：index.css
3   动态js,文件名：inde.js
4   创建数据表，create_db.py
5   管理数据库,select_insert_db.py
6   服务器的搭建，文件名：app.py


遇到的问题：
1   jquery异步发送请求数据时，会首先将数据序列化，需要decodeURIComponent()来反序列化
    var for_data=decodeURIComponent(formStr,true);
2   服务器返回js代码，是否需要包装<script>,是否需要某种转换。
    最后经过搜素和测试，直接返回js代码，并且不需要任何标签包裹。
3   点击按钮激发的js函数，如何获得参数。经过大胆的猜测，测试。
    直接在onclicked=function_name(value),果然将参数传递进去了。
4   创建数据库的时候，char没有指定位数，导致插入的数据，char类型的字符位数，
    都是1位数，只显示最前面的第一位。然后使用alter 进行的修改。
5   数据库的编码问题，一开始创建数据库时，没有指定编码，导致数据库无法正常显示中文，解决办法是
    修改数据表的编码，连接数据库的时候指定编码。修改一张表的编码.--->
    alter table tablename convert to character set utf8; 连接数据库的时候指定编码--->
    self.db=pymysql.connect(host="localhost",user="root",passwd="new_password",db="manager_user",charset="utf8")
6   数据库的等于操作符号是单个的等号（=），而不是双等号（==）。
7   服务器的图片连接也会发送请求来，需要编写相关的路径，来让他们能够找到对应的图片信息，并返回。
8   会话session可以在设定一次之后，在整个app.py里面反复使用。不需要传递参数。
9   编写路由的时候，最好指定相关的请求方法。

任务耗费时间：大概3天。