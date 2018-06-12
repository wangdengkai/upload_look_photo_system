'''

实现持久层：

本引用需要两个表。分别存放用户信息和相片信息。

用户信息主要保存：用户名，密码等信息。
相片信息，则保存相片的标题，相片对应的文件名，以及该相片的属主
等。

因此，用户表和相片表有主从表关联关系，一个用户可以对应于多个相片。

'''
import pymysql

class CreateMysqlTable(object):
    def __init__(self):
        #连接数据库，
        self.db=pymysql.connect("localhost","root","new_password","manager_user")
        #创建游标
        self.cursor=self.db.cursor()


    def run(self):
        #写创建表的SQL语句
        user_table="""
                    CREATE TABLE user_infomation(
                      id INT NOT NULL ,
                      user_name CHAR（20） NOT NULL,
                      pass CHAR（50） NOT NULL,
                      PRIMARY KEY(id),
                      UNIQUE (user_name)
                    
                    );
                """
        photo_table="""
                    CREATE TABLE photo_infomation(
                      id INT NOT NULL AUTO_INCREMENT,
                      image_name CHAR（20） NOT NULL,
                      img_path CHAR（50） NOT NULL,
                      img_time DATE NOT NULL,
                      img_size FLOAT NOT NULL,
                      img_acription CHAR（20） NOT NULL,
                      one_img_id INT NOT NULL,
                      PRIMARY KEY(id),
                      UNIQUE(img_path)
                    );
                """

        #执行sql语句
        # self.cursor.execute(user_table)
        self.cursor.execute(photo_table)
        #提交事务
        self.db.commit()
        #关闭数据库
        self.db.close()



def main():
    create_mysql_table=CreateMysqlTable()
    create_mysql_table.run()
if __name__ == '__main__':
    main()
