'''
    功能：创建一个数据库管理类，其中连接数据库，然后进行插入数据，检索数据。
    有两个表，插入数据的时候，根据功能选择插入或者检索那个表。
    插入的值根据传入的参数进行插入。


'''
from app import app
import pymysql
# import logging
# logging.basicConfig(level=app.logger.info,format="%(lineno)-2d %(funcName)-10s %(message)s")

class ManagerMysql():
    def __init__(self,table_name="NULL",user_name="NULL",password="NULL",
                 image_name="NULL",img_path="NULL",
                 img_size=0.0,img_ascription="NULL"):
        self.db=pymysql.connect(host="localhost",user="root",passwd="new_password",db="manager_user",charset="utf8")
        self.cursor=self.db.cursor()
        self.table_name=table_name
        self.user_name=user_name
        self.password=password
        self.image_name=image_name
        self.img_path=img_path
        self.img_size=img_size
        self.ascript=img_ascription
        app.logger.info("数据库管理对象创建成功")
    def get_user_own_img_title(self,request_count):
        app.logger.info("来到获取图片的标题啦")
        #检索所有的图片标题
        get_img_title="""
                SELECT image_name FROM photo_infomation
                WHERE img_acription = "%s" and one_img_id <= "%d" and one_img_id >= "%d";
            """ %(self.user_name,request_count+9,request_count)
        #执行sql语句
        self.cursor.execute(get_img_title)
        #获取这行后的数据
        img_title_list=self.cursor.fetchall()
        #返回获取的数据
        return img_title_list
    def get_user_own_img_count(self):
        app.logger.info("来到图片数据库的检索数量啦")
        #检索photo_infomathion中某个用户的图片数量。
        retrieve_count_img="""
                SELECT one_img_id FROM photo_infomation
                WHERE  img_acription = "%s";
            """ % self.ascript
        result=self.cursor.execute(retrieve_count_img)
        app.logger.info(result)

        return result
    def get_user_own_img_path(self,image_name):
        app.logger.info("来到图片数据库的检索路径啦")
        #获得某个用户所有的图片路径
        get_img_path="""
                SELECT img_path  FROM photo_infomation
                WHERE  image_name = "%s" 
                ORDER BY  one_img_id;
            """ %(image_name)
        self.cursor.execute(get_img_path)
        result_path=self.cursor.fetchone()
        # raise Exception
        return result_path

    def retrieve(self):
        '''登录数据库的操作，进行检查是否有该用户'''
        app.logger.info('''登录数据库的操作，进行检查是否有该用户''')
        if self.table_name == "user_infomation":
            #检索的sql语句
            user_select="""
                    SELECT * FROM user_infomation  
                    WHERE user_name = "%s" and pass = "%s";
                """ %(self.user_name,self.password)
            result =self.cursor.execute(user_select)
            app.logger.info(result)
            if result:
                return True
            else:
                return False

        else:
            return False
    def add_infomation(self):
        '''注册用户的操作'''
        app.logger.info("注册用户的操作")

        if self.table_name == "user_infomation":
            #将新注册的用户，添加进来
            #检测这个用户是否存在
            flag=self.retrieve()
            if not flag:
                #这个用户不存在，可以插入了
                #插入的sql语句
                new_user_add_to_usertable="""
                    INSERT INTO user_infomation(user_name,pass)
                    VALUES ("%s","%s");
                """ %(self.user_name,self.password)
                self.cursor.execute(new_user_add_to_usertable)
                self.db.commit()
                return True


            else:
                #这个用户存在，不可以插入了，
                return False
        elif self.table_name == "photo_infomation":
            #把上传的图片信息保存起来

            one_img_id=self.get_user_own_img_count()
            new_img_to_photo="""
                INSERT INTO photo_infomation(image_name,img_path,img_time,
                        img_size,img_acription,one_img_id)
                        VALUES ("%s","%s",NOW(),%f,"%s",%d)
                """ %(self.image_name,self.img_path,self.img_size,self.ascript,
                      one_img_id)

            self.cursor.execute(new_img_to_photo)
            self.db.commit()

            return True
        else:
            return False
    def close_mysql_connect(self):
        #关闭数据库连接
        app.logger.info("关闭数据库连接")
        self.db.close()
def main():
    mm=ManagerMysql()
if __name__ == '__main__':
    main()