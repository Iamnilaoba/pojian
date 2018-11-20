1. 下载  pip install flask-wtf
2. 暂时关闭crsf app.config["WTF_CSRF_ENABLED"] = False
3. 继承FlaskForm写自己的检验的form
4. 初始化 fm = UserForm(formdata=request.form)   fm.validate()
5. 获取错误 fm.errors

自定义校验器

1. 先定义这个字段
2. validate_字段名(self,field)
   值: field.data
   通过判断返回异常 ValidationError(message="你写的这个东西不符合要求")

# 文件上传下载

```python
form表单中enctype="multipart/form-data"
在服务器 file =  request.files 来获取文件数据
文件名称 file.filename 获取的文件名称，一定要服务器生成一个唯一的（否则会覆盖）
file.save('路径')

# 下载
```

   send_from_directory('图片文件夹',图片的名称)

```python
文件校验
使用FileField(validators=[file_required(message="文件不能为空"),
                              FileAllowed({'jpg','gif'},message="文件只能是jpg和gif格式")])
使用CombinedMultiDict([request.form,request.files]) 进行两个字典的合并
```

# cookie和session

因为http是无状态的，所有跟踪用户的行为
cookie

session
​    flask实现的session使用cookie进行传递



**上下文对象**

**钩子函数**

**crsf攻击和防御**

**restful使用（移动端，公众号）**
