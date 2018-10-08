from flask import Blueprint,session
from flask.views import MethodView
from flask import render_template
from apps.cms.forms import *
from flask import request,jsonify
from apps.common.baseResp import *
from apps.cms.models import *
from config import REMBERME,LOGIN,CURRENT_USER_ID
import string,random
from apps.common.memcachedUtil import saveCache
from functools import wraps
from apps.common.models import *
from qiniu import Auth
from tasks import sendmsg

bp=Blueprint('cms',__name__,url_prefix='/cms')

#验证登录装饰器
def loginDecotor(func):
    @wraps(func)
    def inner(*args,**kwargs):
        login=session.get(REMBERME)
        if login==LOGIN:
            return func(*args,**kwargs)
        else:
            return render_template('cms/login.html')
    return inner

#验证权限装饰器
def checkPermission(permission):
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            # 取出来当前的用户， 并判断这个用户有没有这个权限
            userid = session[CURRENT_USER_ID]
            user = User.query.get(userid)
            r = user.checkpermission(permission)
            if r:
                return func(*args,**kwargs)
            else:
                return render_template("cms/login.html")
        return inner
    return outer

@bp.route('/')
def loginView():
    return render_template('cms/login.html')

#登录
@bp.route('/login/',methods=['post'])
def login():
    fm=UserForm(formdata=request.form)  #验证用户输入的信息
    if fm.validate():
        email=fm.email.data   #如果通过验证就获取到用户输入的信息
        pwd=fm.password.data
        user=User.query.filter(User.email==email).first()  #跟数据库里的用户信息进行比较
        if not user:
            return jsonify(respParamErr('用户不对'))
        if user.checkPwd(pwd):
            remberme=request.values.get('remberme')
            session[REMBERME]=LOGIN
            session[CURRENT_USER_ID]=user.id
            if remberme=='1':
                session.permanent=True
            return jsonify(respSuccess('登陆成功'))
        else:
            return jsonify(respParamErr('密码错误'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route('/index/')
@loginDecotor
def cms_index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@loginDecotor
def logout():
    session.clear()
    return render_template('cms/login.html')

@bp.route('/user_infor/')
@loginDecotor
@checkPermission(Permission.USER_INFO)
def user_infor():
    return render_template('cms/userInfo.html')

#修改密码
class ResetPwd(MethodView):
    decorators=[checkPermission(Permission.USER_INFO),loginDecotor]
    def get(self):
        return render_template('cms/resetpwd.html')

    def post(self):
        fm=ResetPwdForm(formdata=request.form)
        if fm.validate():
            userid=session[CURRENT_USER_ID]   #如果通过验证把userid存放到session中以便取用
            user=User.query.get(userid)
            r=user.checkPwd(fm.oldpwd.data)
            if r:   #如果旧密码跟数据库里的旧密码一样的话执行下面代码
                user.password=fm.newpwd.data
                db.session.commit()
                return jsonify(respSuccess(msg='修改成功'))
            else:
                return jsonify(respParamErr(msg='修改失败，旧密码错误'))
        else:
            return jsonify(respParamErr(msg=fm.err))

#修改邮箱
class Resetmail(MethodView):
    decorators = [checkPermission(Permission.USER_INFO),loginDecotor]  #通过装饰器验证登录以及权限
    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        fm=ResetEailForm(formdata=request.form)   #验证用户输入的信息
        if fm.validate():
            user=User.query.get(session[CURRENT_USER_ID])
            user.email=fm.email.data   #用户数据库里的旧邮箱等于用户输入的新邮箱
            db.session.commit()
            return jsonify(respSuccess(msg='修改邮箱成功'))
        else:
            return jsonify(respParamErr(msg=fm.err))

#发送验证码（重点：有阿里云账号，并且从阿里云下载并导入Python文件（dysms_python），修改send）
@bp.route("/send_email_code/",methods=['post'])
@loginDecotor
@checkPermission(Permission.USER_INFO)  #可以查看个人信息的权限
def sendEmailCode():
    fm = ResetEmailSendCode(formdata=request.form)  #用户输入信息验证（邮箱是否重复格式是否正确）
    if fm.validate():
        r = string.ascii_letters+string.digits
        r = ''.join(random.sample(r, 6))  #生成验证码send发送验证码
        saveCache(fm.email.data,r.upper(),30*60)  # r.upper()：验证码不分大小写
        recvmail=fm.email.data    #异步处理
        sendmsg.delay(recvmail,r)
        return jsonify(respSuccess(msg='发送成功，请查看邮箱'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route('/banner/')
@loginDecotor
@checkPermission(Permission.BANNER)  #轮播图的权限
def banner_view():
    banners=Banner.query.all()   #查询出所有轮播图
    context={
        'banners':banners
    }
    return render_template("cms/banner.html",**context)

#添加轮播图
@bp.route('/addbanner/',methods=['post'])
@loginDecotor
@checkPermission(Permission.BANNER)
def addBanner():
    fm=BannerForm(formdata=request.form)   #验证用户输入的信息
    if fm.validate():
        banner=Banner(bannerName=fm.bannerName.data,
                      imglink=fm.imglink.data,
                      link=fm.link.data,
                      priority=fm.priority.data)
        db.session.add(banner)     #将用户输入的信息添加到数据库中
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

@bp.route("/deletebanner/",methods=['post'])
@loginDecotor
@checkPermission(Permission.BANNER)
def deleteBanner():
    banner_id = request.values.get("id")  #获取到用户输入的id
    "".isdigit()   # 验证id是否为整数
    if not banner_id or not banner_id.isdigit() :
        return  jsonify(respParamErr(msg='请输入正确banner_id'))
    banner = Banner.query.filter(Banner.id == banner_id).first()   #对比用户传入的id是否跟数据库里的id一样
    if banner :
        db.session.delete(banner)  # 从数据库删除
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else: # 没有
        return jsonify(respParamErr(msg='请输入正确banner_id'))

@bp.route("/updatebanner/",methods=['post'])
@loginDecotor
@checkPermission(Permission.BANNER)
def updateBanner():
    fm = BannerUpdate(formdata=request.form)  #验证用户输入的内容
    if fm.validate():
        banner = Banner.query.get(fm.id.data)  #拿到该图片的id并添加用户输入的信息到数据库中
        if banner :
            banner.link = fm.link.data
            banner.imglink = fm.imglink.data
            banner.priority = fm.priority.data
            banner.bannerName = fm.bannerName.data
            db.session.commit()
            return jsonify(respSuccess(msg='更新成功'))
        else:
            return jsonify(respParamErr(msg='id失效'))
    else:
        return jsonify(respParamErr(msg=fm.err))

#板块管理
@bp.route('/bank/')
@loginDecotor
@checkPermission(Permission.PLATE)
def bank_view():
    banks=Bank.query.all()  #查询到所有版块
    context={
        'banks':banks
    }
    return render_template("cms/bank.html",**context)

#添加板块
@bp.route('/addbank/',methods=['post'])
@loginDecotor
@checkPermission(Permission.PLATE)
def addBank():
    fm = BankForm(formdata=request.form)   #验证用户输入的信息（版块名称是否为空是否重复）
    if fm.validate():
        bank = Bank(bankname=fm.bankname.data)  #将用户输入的信息添加到数据库中
        db.session.add(bank)
        db.session.commit()
        return jsonify(respSuccess(msg='添加成功'))
    else:
        return jsonify(respParamErr(msg=fm.err))

#删除板块
@bp.route('/delebank/',methods=['post'])
@loginDecotor
@checkPermission(Permission.PLATE)
def deleBank():
    bank_id = request.values.get("id")  #获取到用户要删除板块的id
    "".isdigit()  #验证id是否为整数
    if not bank_id or not bank_id.isdigit():
        return jsonify(respParamErr(msg='请输入正确bank_id'))
    bank = Bank.query.filter(Bank.id == bank_id).first()   #比较用户输入的id是否跟数据库里的id是否一样
    if bank:
        db.session.delete(bank)   #删除板块
        db.session.commit()
        return jsonify(respSuccess(msg='删除成功'))
    else:
        return jsonify(respParamErr(msg='请输入正确bank_id'))

#更新板块
@bp.route('/updatebank/',methods=['post'])
@loginDecotor
@checkPermission(Permission.PLATE)
def updateBank():
    fm = BankUpdate(formdata=request.form)  #验证用户输入的信息
    if fm.validate():
        bank = Bank.query.get(fm.id.data)   #查询出用户要更新板块的id
        if bank:    #如果id相同，则进行修改
            bank.bankname = fm.bankname.data
            db.session.commit()
            return jsonify(respSuccess(msg='更新成功'))
        else:
            return jsonify(respParamErr(msg='id失效'))
    else:
        return jsonify(respParamErr(msg=fm.err))

#帖子管理页面
@bp.route('/showpost/')
@loginDecotor
@checkPermission(Permission.POSTS)
def showPost():
    posts=Post.query.all()  #查询出所有帖子
    context={
        'posts':posts
    }
    return render_template('cms/postmgr.html',**context)

#添加精
@bp.route('/addtag/',methods=['post'])
@loginDecotor
@checkPermission(Permission.POSTS)
def addTag():
    post_id=request.values.get('post_id')
    post=Post.query.filter(Post.id==post_id).first()
    if post:
        tag=Tag(post=post,status=True)
        db.session.add(tag)
        db.session.commit()
        return jsonify(respSuccess('加精完成'))
    else:
        return jsonify(respParamErr('请传入正确的post_id'))

#取消精
@bp.route('/deletetag/',methods=['post'])
@loginDecotor
@checkPermission(Permission.POSTS)
def deteleTag():
    post_id=request.values.get('post_id')
    tag=Tag.query.filter(Tag.post_id==post_id).first()
    if tag:
        tag.status=False
        db.session.commit()
        return jsonify(respSuccess('取消加精成功'))
    else:
        return jsonify(respParamErr('请传入正确的id'))

bp.add_url_rule('/resetemail/',endpoint='resetemail',view_func=Resetmail.as_view('resetemail'))
bp.add_url_rule('/resetpwd/',endpoint='resetpwd',view_func=ResetPwd.as_view('resetpwd'))


#上传图片给七牛云（必须七牛云账号）
@bp.route("/qiniu_token/")
def qiniukey():
    # 通过secer-key id 生成一个令牌，返回给客户端
    ak = "gixRZTC9nnM_ODSEyAmDtFPVBD5sBWJo1dsfszvB"
    sk = "X8TYRWzELi-hfyzl1MeAkEbS9i5DKL_8qI4m_o3l"
    q = Auth(ak, sk)
    bucket_name = 'pjssb' # 仓库的名字
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken': token})

#钩子函数：在每次请求时都会先执行这个函数
@bp.context_processor
def requestUser():
    login = session.get(REMBERME)
    if login == LOGIN:
        userid = session[CURRENT_USER_ID]
        user = User.query.get(userid)
        return {'user':user}
    return {}
