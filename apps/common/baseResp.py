#定义个返回response类，方便使用
class BaseResp:
    def __init__(self,code,msg,data=None):
        self.code=code
        self.msg=msg
        self.data=data

class respCode:
    SUCCESS=200
    UNAUTHERROR=401
    PARAMERR=402

def respSuccess(msg,data=None):
    return BaseResp(code=respCode.SUCCESS,msg=msg,data=data).__dict__

def respParamErr(msg='参数错误',data=None):
    return BaseResp(code=respCode.PARAMERR,msg=msg,data=data).__dict__

def respUnAutherr(msg='没有访问权限'):
    return BaseResp(code=respCode.UNAUTHERROR,msg=msg).__dict__





