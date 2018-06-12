//处理用户登录的函数,检查用户输入是否正确

function proRetrive() {
    //获取两个文本框的数值
    var user = $.trim($("#user").val());
    var pass = $.trim($("#pass").val());
    var flag=false;
    if (user === null || user === "" || pass === null || pass === "") {
        alert("必须输入用户名和密码才能登录.");
        return flag;
    }
    else {
        //要求用户名是字母数字下划线和中文,并且长度大于4
        var user_r, re_user, pass_r, re_pass;
        re_user = /.{3,}/;
        re_pass = /[a-zA-Z0-9_]{8,}/i;
        //匹配结果
        user_r = user.match(re_user);
        pass_r = pass.match(re_pass);
        if(user_r ===null)
            {
                alert("用户名必须大于3位，可以是字母数字下划线中文");
                return flag;
            }
        else if (pass_r === null )
                {
                    alert("密码必须大于8位，并且是字母数字下划线");
                    return flag;


            }

    }
    flag=true;
    return flag;

}
//处理用户登录的函数
function proLogin(){

    //先调用处理用户登录的函数,检查用户输入是否正确
    if (proRetrive()){
        //alert("用户名和密码输入正确")
        //alert("用户名密码输入正确")
        //向服务器发送post注册请求,“Pro/login”是服务器路径“/pro”，
        // $("#user,#pass").serializeArray()是发送的数据，转换为array类型
        //{name:value},null,表示没有回调函数。script表示返回的类型是script的代码，可以直接执行
        var formStr=$("#user,#pass").serialize();
        //序列化中文时之所以乱码是因为.serialize()调用了encodeURLComponent方法将数据编码了
        //原因：.serialize()自动调用了encodeURIComponent方法将数据编码了
        //解决方法：调用decodeURIComponent(XXX,true);将数据解码
        var for_data=decodeURIComponent(formStr,true);
        // params = decodeURIComponent(formStr,true); //关键点
        $.post("/pro/login",for_data,null,"script")
        // console.log(for_data["username"])

    }
    else{
        //alert("用户名和密码输入不正确")
    }
}
//处理用户注册的函数
function proRegister() {

    //先处理用户登录的函数,检查用户输入是否正确
    if (proRetrive()) {
        //alert("用户名密码输入正确")
        //向服务器发送post注册请求,“Pro/register”是服务器路径“/pro”，
        // $("#user,#pass").serializeArray()是发送的数据，转换为array类型
        //{name:value},null,表示没有回调函数。script表示返回的类型是script的代码，可以直接执行
        var form_str = $("#user,#pass").serialize();
        var for_data = decodeURIComponent(form_str, true);
        $.post("/pro/register", for_data, null, "script")
    }
    else {
        //alert("用户名密码输入错误。")
        return null;
    }
}

//如果用户登录成功，周期性的获取当前用户页面的相片。
// function onLoadHandler()
// {
//     //给服务器发送异步get请求
//     $.getScript("getPhoto");
//     //制定了1s之后再执行这个方法
//     setTimeout("onLoadHandler()",1000);
// }
//定义上传函数,效果，就是用户已点击，那么就弹出一个上传窗口，然后在窗口中可以找到文件，点击上传就上传。
// 最后还要有回调函数，如果上传成功，那么就结束窗口，然后返回到原来界面，并在table栏目里面出现文件名
//这个文件名字是带连接的。，点击后，右面就会出现相应的图片。每次显示大概10章。
// funtion getFileType(file_path)
// {
//     var startIndex = filePath.lastIndexOf(".");
//     if(startIndex != -1)
//         return filePath.substring(startIndex+1, filePath.length).toLowerCase();
//     else return "";
// }
function up_load() {
    $("#upload_div").show();
    $(".show_img").hide();
    $("#file").val("");
    $("#title").val("");
}
function judge_file_type_size(){


    var file_path=$("#file").val();


    if ("" != file_path){

        var file_type=get_file_type(file_path);
        // alert("这是judge_file_type");
        //判断是否上传的附件是否是图片
        if("jpg" != file_type && "jpeg" != file_type && "bmp" !==file_type && "png" != file_type && "gif" != file_type ){
            $("#file").val("");
            alert("请你上传JPG，JPEG，BMP，png,gif 格式的图片");
            return false;
        }
        else{

            //获取文件的大小（单位kb)
            var file_size=$("#file").size/1024;
            // alert("eles");
            // alert(file_size);
            if(file_size >2) {
                alert("图片不能大于2Mb");
                return fasle;

            }
            else{
                // alert("图像大小合适");
                return true;
            }
        }
    }
}
function get_file_type(file_path){
    // alert(file_path);
    //获得文件的类型
    var file_path=file_path;
    var startIndex=file_path.lastIndexOf(".");
    // alert("数据--size");
    if (startIndex != -1){
        return file_path.substring(startIndex+1,file_path.length).toLowerCase();
    }
    else{
        return "";
    }


}
function up_load_file(){
    // alert("数据传送来啦");
    var file_title=$("#title").val();
    var file_content=$("#file").val();
    // alert(file_content);
    // alert(file_title);
    if (file_title=="" || file_content==""){
            alert("题目和标题需要填写");
            return null;
    }
    else{
        var file_state=judge_file_type_size();
        //发送数据
        if (!file_state) {

            up_load();
        } else {

            // 自动搜索表单信息(表单内没有name属性的input不会被搜索到)，IE<=9不支持FormData
            var file_data = new FormData($("form")[0]);
            //还可以添加额外的表单数据
            // file_data.append("b","nihao");
            $.ajax({
                url: "/upload_photo",
                type: "POST",
                success: callback,
                error: function () {
                    alert("请检查文件标题,文件是否重复等等问题！")
                },
                data: file_data,
                //下面的选项告诉jq不要缓存数据而且使用表单本身得分contenttype
                cache: false,
                // 当有文件要上传时，此项是必须的，否则后台无法识别文件流的起始位置(详见：#1)
                contentType: false,
                // 是否序列化data属性，默认true(注意：false时type必须是post，详见：#2)
                processData: false

            })
        }
    }

}
function callback(msg){
    alert(msg);
    //隐藏文件上传的对话框
    $("#upload_div").hide();
    //清空title，file两个表单域
    $("#hideframe").attr("src","");
    $(".show_img").show();
}
//显示左面的标题列表，和第一个图片
function show_title_and_img(){
    //给服务器发送请求获取图片列表
    $.post("/getPhoto",null,show_first,"json")

}
//显示列中的第一个图片列表.
function show_first(data){
    $("#img_list").empty();
    for( var img_title in data){

        $("#img_list").append('<tr><td><button name="button" type="button" value="' +
                                data[img_title]+'" onclick="request_photo(value);"><span>'+
                                data[img_title]+
                                '</span></button>'+
                                '</td></tr>');

    }

}
function request_photo(button_value){
    var button_data=decodeURIComponent(button_value,true);
    $.get("/getPhoto/"+button_data,null,null,"script");
}
function turn_page(flag)
{
    $.get("/turn_page/"+flag,null,show_first,"json");
}
//定义页面加载模块
$(document).ready(function(){

});
