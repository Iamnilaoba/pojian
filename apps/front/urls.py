#写这么多无非就是对数据库里的增删改查，你没理由不会！！！再不努力别人拿10k你只能拿3k！！！
from flask import Blueprint,request,make_response
from flask import render_template,session
from flask.views import MethodView
from apps.front.forms import *
import string
import random
from flask import jsonify
from apps.common.baseResp import *
from apps.common.captcha.xtcaptcha import Captcha
from io import BytesIO
from apps.common.memcachedUtil import saveCache,delete
from apps.front.models import  FrontUser
from config import *
from apps.common.models import *
from functools import wraps
from config import FRONT_USER_ID
from flask import redirect
from flask import url_for
import math
from flask_paginate import Pagination,get_page_parameter
from tasks import sendcmscode
bp=Blueprint('font',__name__)

def lonigDecotor(func):
    """限制登录的装饰器"""
    @wraps(func)
    def inner(*args,**kwargs):
        if not session.get(FRONT_USER_ID,None): # 没有登陆
            return redirect(location=url_for("font.signin"))
        else:
            r = func(*args,**kwargs)
            return r
    return inner

class Page:
    countofpage=10   #每页要显示的张数
    @property
    def page(self):
        count=Post.query.count()  #获取总共的张数
        return math.ceil(count/self.countofpage)  #返回一共多少页
    currentpage=0
    posts=None

#分页
@bp.route('/')
def index():
    banners=Banner.query.order_by(Banner.priority.desc()).limit(5)  #查询并按照优先级逆序排序
    banks=Bank.query.all()
    bank_id=request.args.get('bank_id')
    page = request.args.get(get_page_parameter(), type=int, default=1) # 通过分页插件返回总共所需页数
    begin = (page - 1) * 10
    end = begin + 10
    readCount=request.args.get('readcount',None)  #获取阅读量
    if bank_id: #如果有板块的话执行以下代码
        if readCount:
            tup=(Post.readCount.desc(),Post.create_time.desc())  #按阅读量，创建时间进行逆序排序
        else:
            tup=(Post.create_time.desc())
        posts = Post.query.filter(Post.bank_id == bank_id).order_by(tup).slice(begin, end)
        count = Post.query.filter(Post.bank_id == bank_id).count()
    else:  #没有板块
        if readCount:
            posts = Post.query.order_by(Post.readCount.desc(),Post.create_time.desc()).slice(begin, end)
        else:
            posts = Post.query.order_by(Post.create_time.desc()).slice(begin, end)  # asc:顺序，desc:逆序
        count = Post.query.count()
    pagination = Pagination(bs_version=3, page=page, total=count) #参数1：使分页方向是水平的否则为垂直，2：分页数，3：总共的帖子张数
    context = {
        'banners': banners,
        'banks':banks,
        'posts':posts,
        'pagination':pagination
    }
    return render_template("front/index.html", **context)

#注册
class Signup(MethodView):
    def get(self):
        return render_template('front/singup.html')

    def post(self):
        fm = SignupFrom(formdata=request.form)  #验证用户输入的内容（用户名是否重复，验证码是否正确等等）
        if fm.validate():
            u = FrontUser(telephone=fm.telephone.data, #如果通过验证则往数据库里添加即可
                          username=fm.username.data,
                          password=fm.password.data)
            db.session.add(u)
            db.session.commit()
            delete(fm.telephone.data)  # 注册成功，删除手机验证码
            return jsonify(respSuccess("注册成功"))
        else:
            return jsonify(respParamErr(fm.err))

#发送验证码
@bp.route('/send_sms_code/',methods=['post'])
def sendSMSCode():
    fm=SendSmsCodeForm(formdata=request.form)  #验证用户输入的手机号是否重复，格式是否正确
    if fm.validate():
        source=string.digits
        source=''.join(random.sample(source,4))  #生成4位随机数验证码
        sendcmscode.delay(fm.telephone.data,source)
        return jsonify(respSuccess("短信验证码发送成功，请查收"))
    else:
        return jsonify(respParamErr(fm.err))

#验证码
@bp.route('/img_code/')
def ImgCode():
    text,img=Captcha.gene_code()   #生成数字和背景图
    print(text) #在服务器中打印出生成的验证码
    out=BytesIO()
    img.save(out,'png')
    out.seek(0)
    saveCache(text,text,60)  #60秒有效时
    resp=make_response(out.read())
    resp.content_type='image/png'
    return resp

#注销
@bp.route('/logout/')
def logout():
    session.clear()  #注销清空session
    return redirect(url_for('font.signin')) #服务器转移到登录界面

#登录
class Signin(MethodView):
    def get(self):
        return render_template('front/signin.html')
    def post(self):
        fm=SigninFrom(formdata=request.form)   #登录验证手机号密码是否正确
        if fm.validate():
            user=FrontUser.query.filter(FrontUser.telephone==fm.telephone.data).first() #比较数据库里的手机号码跟用户输入的手机号码
            if not user:
                return jsonify(respParamErr('电话号码没有注册，请注册'))
            r=user.checkPwd(fm.password.data)  #比较用户输入的密码跟数据库里的是否一致
            if r:
                remberme = request.values.get('remberme')
                session[REMBERME] = LOGIN
                session[FRONT_USER_ID] = user.id
                if remberme == '1':
                    session.permanent = True
                return jsonify(respSuccess('登陆成功'))
            else:
                return jsonify(respParamErr("密码错误"))
        else:
            return jsonify(respParamErr(fm.err))

#找回密码
class FindPwd(MethodView):
    def get(self):
        return render_template('front/findpwd.html')
    def post(self):
        fm=FindpwdForm(formdata=request.form)   #验证用户输入的信息是否有误
        if fm.validate():
            r=FrontUser.query.filter(FrontUser.telephone==fm.telephone.data).first() #从数据库里找出该用户
            r.password=fm.password.data  #令该用户的密码等于输入的密码
            db.session.commit()
            return jsonify(respSuccess(msg='密码修改成功'))
        else:
            return jsonify(respParamErr(fm.err))
@bp.route('/sendcode/',methods=['post'])
def sendcode():
    fm=SendCodeForm(formdata=request.form)
    if fm.validate():
        rs=string.digits
        rs=''.join(random.sample(rs,4))
        sendcmscode.delay(fm.telephone.data, rs)
        return jsonify(respSuccess("短信验证码发送成功，请查收"))
    else:
        return jsonify(respParamErr(fm.err))

#发布帖子
class Addpost(MethodView):
    decorators = [lonigDecotor]
    def get(self):
        banks = Bank.query.all()  #数据库查出所有版块
        context = {
            "banks": banks
        }
        return render_template("front/addpost.html",**context)

    def post(self):
        fm = AddPostForm(formdata=request.form)  #验证用户输入的内容
        if fm.validate() :
            user_id = session[FRONT_USER_ID]
            post = Post(title=fm.title.data,content=fm.content.data, #往数据库里存入用户输入的信息
                 bank_id=fm.bank_id.data,user_id=user_id)
            db.session.add(post)
            db.session.commit()
            return jsonify(respSuccess("发布成功"))
        else:
            return jsonify(respParamErr(fm.err))

#展示帖子的内容
@bp.route('/showpostdetail/')
def showpostdetail():
    post_id=request.args.get('post_id')  #获取该帖子的id
    if not post_id:
        return render_template('/')
    post=Post.query.filter(Post.id==post_id).first()  #比较该帖子的id是否跟数据库里的一样
    if not post:
        return render_template('/')
    commons = Common.query.filter(Common.post_id == post_id).all() #查出该帖子里对应的评论
    if post.readCount:  #帖子浏览数量
        post.readCount=post.readCount+1   #每浏览一次帖子就+1
    else:
        post.readCount=1
    db.session.commit()
    context = {
        'post': post,
        'commoms': commons
    }
    return render_template("front/postdetail.html", **context)

#评论帖子
@bp.route('/addcommon/',methods=['post'])
def addCommon():
    user_id=session.get(FRONT_USER_ID,None)  #获取要评论用户的id
    if not user_id:
        return jsonify(respParamErr('请先登录'))
    post_id=request.values.get('post_id')  #获取用户输入的内容
    content=request.values.get('content')
    if not content:
        return jsonify(respParamErr('帖子内容不能为空'))
    commom=Common(content=content,post_id=post_id,user_id=user_id) #将用户评论的内容添加到数据库中
    db.session.add(commom)
    db.session.commit()
    return jsonify(respSuccess('评论成功'))


#钩子函数：在每次请求时都会先执行这个函数
@bp.context_processor
def requestUser():
    userid = session.get(FRONT_USER_ID,None)
    if not userid :
        return {}
    user = FrontUser.query.get(userid)
    return {'user':user}

    # fm.user.data  基于request.from 是平时post请求中中最常用的
	# request.values.get('user')  get和post请求中都可使用
	# request.args.get('user')  只能用于get请求


bp.add_url_rule("/addpost/",endpoint='addpost',view_func=Addpost.as_view('addpost'))
bp.add_url_rule("/findpwd/",endpoint='findpwd',view_func=FindPwd.as_view('findpwd'))
bp.add_url_rule('/signin/',endpoint='signin',view_func=Signin.as_view('signin'))
bp.add_url_rule("/signup/", endpoint='signup', view_func=Signup.as_view('signup'))