from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug import security

import os
import re
import hashlib
import select_insert_db
import json
import logging
import random




app = Flask(__name__)
app.secret_key = b'\x04\xff\x8c\x931\xe1\xdf\x92\x06\xf5'
app.logger.setLevel(logging.INFO)

@app.route("/")
def index():
    app.logger.info("来到了首页")
    return render_template("index.html")

@app.route("/pro/login", methods=["POST"])
def login():
    # # 需要直接返回js语句，让页面自动刷新
    # # 接受到请求的json数据
    # app.logger.info("来到login页面啦")
    app.logger.info("已经来到login页面啦.")
    # accept_json=request.get_data()
    # 接收到额的数据是 username=网邓凯&password=einsjfheafkn
    accept_json = request.get_data().decode("utf-8")
    username = re.search(r"=([^&]*)", accept_json).group(1)
    password = re.search(r"&.*?=(.*)$", accept_json).group(1)
    session["user_name"] = username
    # accept_dict=json.loads(accept_json)
    # accept_content=accept_json.decode("utf-8").encode("utf-8").split("&")
    # print(accept_json.decode("utf-8"))
    # 到数据库中检索一下，传输过去，经过加密的数据
    # 是否存在这个账户
    # 存在这个账户，那么登录成功
    # 不存在这个账户，提示重新登录，账号密码有错误
    # 调用函数，处理
    result = handle_data("login", username=username, password=password)
    # 根据result，决定返回值
    # if result:
    #
    #     pass
    # else:#返回正确登录的js
    #     #返回登录错误的js
    #     pass
    response = get_js(task_type="login", request_status=result, username=username)
    app.logger.info(url_for("register"))
    return (response).encode("utf-8")


@app.route("/pro/register", methods=["POST"])
def register():
    app.logger.info("来到register 页面了")
    app.logger.info("已经来到register页面啦.")
    app.logger.warning("zhehsiygie jinggao ")
    # 需要直接返回js语句，让页面自动刷新
    # 首先要获取发送过来的信息，name,password
    accept_json = request.get_data().decode("utf-8")
    username = re.search(r"=([^&]*)", accept_json).group(1)
    session["user_name"] = username
    password = re.search(r"&.*?=(.*)$", accept_json).group(1)
    # 将其加入到数据库中

    # 进行hex md5 加密
    # 返回js语句，更改状态。
    # 调用函数进行处理
    result = handle_data(task="register", username=username, password=password)
    # 判断结果，返回响应的js
    # if result:
    #     #注册成功，返回正确的js
    #     pass
    # else:
    #     #注册失败，返回错误的js
    #     pass
    response = get_js(task_type="register", request_status=result, username=username)
    # response_header="HTTP/1.1 200 OK\r\n\r\n"

    return (response).encode("utf-8")


@app.route("/getPhoto",methods=["POST"])
def get_photo():

    img_title_list=[]
    session["img_count"]=len(img_title_list)
    # app.logger.warning("22222222222222")
    img_title_list=get_img_title()
    # app.logger.warning("33333333333")
    return img_title_list

def get_img_title():
    # app.logger.warning("4444444")
    # 连接数据库
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",
                                              user_name=session["user_name"]
                                              )
    #从数据库取得图片的标题
    # app.logger.warning("55555555")
    app.logger.info("--get_img _title")
    app.logger.info(session["img_count"])
    img_title_list=manager_sql.get_user_own_img_title(session["img_count"])
    # app.logger.warning("66666666")
    # session["img_count"]+=len(img_title_list)
    # 直接返回图片的标题
    if len(img_title_list)<=0:
        return ""
    return json.dumps(img_title_list)
@app.route("/turn_page/<flag>",methods=["GET"])
def turn_page(flag):
    app.logger.info(session["img_count"])
    app.logger.info(flag)
    if session["img_count"] == 0:
        if flag=="up":
            app.logger.info(session["img_count"])
        elif flag == "down":
            session["img_count"]+=10
            app.logger.info(session["img_count"])
    elif flag == "up":
        session["img_count"]-=10
    elif flag == "down":
        session["img_count"]+=10
    app.logger.info(session["img_count"])
    img_title_list=get_img_title()

    app.logger.info(json.loads(img_title_list))
    return img_title_list


@app.route("/getPhoto/<image_name>")
def get_one_image(image_name):
    #调用处理函数，返回image,

    # app.logger.info(image_name)
    read_img(image_name)
    response="""
                $(".show_img").empty().html('<img src="%s" width="500" height="500"/>');
    
        """ %session["image_path"]
    # app.logger.info(response)
    return response

def read_img(image_name):
    #连接数据库
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",user_name=session["user_name"])
    #获得路径
    image_path=manager_sql.get_user_own_img_path(image_name)
    session["image_path"]=image_path
    #返回图片
    # try:
    #     f=open(image_path,"rb")
    # except Exception:
    #     return "您好数据出问题啦！".encode("utf-8")
    # else:
    #     image_content=f.read()
    #     return image_content

@app.route("/favicon.ico",methods=["GET"])
def get_icon():
    with open("website_icon.jpg","rb") as f:
        response=f.read()

    return response

@app.route("/upload_photo",methods=["POST"])
def upload_photo():
    #设置随机数
    file_num=random.randint(0,20)
    #获取jquery发来的文件
    file=request.files["file"]
    #这是文件名字
    file_name=session["user_name"]+str(file_num)+file.filename
    #将文件的路径转为安全的。
    file_path=security.safe_join("images/",file_name)
    file.save(file_path)
    #将文件大小加入session
    file_size=os.path.getsize(file_path)
    session["file_size"]=file_size
    #将文件路径加入session
    session["file_path"]=file_path

    #将文件标题加入session
    session["file_title"]=request.form["title"]
    #调用函数插入数据库数据
    result=up_load_photo()
    if result:
        #完成后返回数据，提示已经上传成功。
        return "文件上传成功"
    else:
        return "文件上传失败，请检查网络和文件等，重新上传。"

#http://localhost:5000/images/IMG_20140511_100718.jpg
@app.route("/images/<image_photo>")
def look_image(image_photo):
    try:
        f=open("images/"+image_photo,"rb")
    except Exception:
        response="打不开"
        app.logger.info("打不开")
    else:
        response=f.read()
        app.logger.info("数据打开成功")

    return response

def handle_data(task, username, password, ):
    app.logger.info("来到数据处理啦")
    '''对数据进行加密，并调用相关的处理方法，操作成功返回True，操做失败返回False'''
    ha_password = hashlib.md5(password.encode("utf-8")).hexdigest()
    app.logger.info(type(ha_password))
    # 创建数据库管理对象，
    manager_sql = select_insert_db.ManagerMysql(table_name="user_infomation", user_name=username, password=ha_password)
    # 根据调用的函数，选择合适的操作，返回True或者
    if task == "register":
        result = manager_sql.add_infomation()
    elif task == "login":
        result = manager_sql.retrieve()
    else:
        result = False
    manager_sql.close_mysql_connect()
    return result


def get_js(task_type, request_status, username):
    app.logger.info("来到返回数据页面啦")
    # 根据task_type判断返回时登录还是注册的js
    page_js = None
    if task_type == "login":
        # 这是登录页面调用的，要返回js
        if request_status:
            page_js = """
                $("#non_login").css("display","none");
                $("#login").css("display","block");                
                $("#two_span").text("注册成功！，欢迎 %s,开始happy!");
                show_title_and_img();
               
               
            """ % username
        else:
            page_js = """
               
                alert("登录失败");
                $("#one_span").css("color","red");
                $("#one_span").text("您好，账号或密码错误，请重新登录");
                
                
            """
            # 根据request_status 返回正确或者失败的js。
    elif task_type == "register":
        # 这是注册页面调用的。
        if request_status:
            page_js = """
                $("#non_login").css("display","none");
                $("#login").css("display","block");                
                $("#two_span").text("欢迎 %s,开始happy!");
                show_title_and_img();
               
            """ % username
        else:
            page_js = """
               
                $("#one_span").css("display","block");
                $("#one_span").text("您好，您注册的账号已经存在，请选择新的！");
               
            """

    return page_js
def up_load_photo():
    #创建数据库对象，
    manager_sql=select_insert_db.ManagerMysql(table_name="photo_infomation",
                                              user_name=session["user_name"],
                                              img_ascription=session["user_name"],
                                              img_path=session["file_path"],
                                              img_size=session["file_size"],
                                              image_name=session["file_title"])
    result=manager_sql.add_infomation()
    #将数据插入到数据库中，返回True
    return result

if __name__ == "__main__":
    app.run()
