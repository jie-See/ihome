import json
import re
from django.db.utils import IntegrityError

from common.redis import rds
from .models import User
from django.http import HttpResponse, JsonResponse


def register(request):
    req = json.loads(request.body.decode())

    mobile = req['mobile']
    sms_code = req['sms_code']
    password = req['password']
    password2 = req['password2']

    # 校验参数
    if not all([mobile, sms_code, password, password2]):
        return JsonResponse({"err": "参数不完整"})

    # 判断手机号格式
    if not re.match(r"1[345678]\d{9}", mobile):
        return JsonResponse({"err": "手机号格式错误"})

    if password != password2:
        return JsonResponse({"err": "两次密码不一致"})

    # 从redis中取出短信验证码
    try:
        real_sms_code = rds.get("sms_code_%s" % mobile)
    except Exception as e:
        return JsonResponse({"err": "读取真实短信验证码异常"})


    # 判断短信验证码是否过期
    if real_sms_code is None:
        return JsonResponse({"err": "短信验证码失效"})

    # # 删除redis中的短信验证码，防止重复使用校验
    # try:
    #     rds.delete("sms_code_%s" % mobile)
    # except Exception as e:
    #     print(e)

    #


    # # 判断用户的手机号是否注册过
    # try:
    #     user = User.objects.filter(mobile=mobile).first()
    # except Exception as e:
    #     return JsonResponse({"err": "数据库异常"})
    # else:
    #     if user is not None:
    #         # 表示手机号已存在
    #         return JsonResponse({"err": "手机号已存在"})

    

    try:
        user = User(name=mobile, mobile=mobile)
        user.password = password
        user.save()
    except IntegrityError as e:
        return JsonResponse({"err": "手机号已存在"})
    except Exception as e:
        return JsonResponse({"err": "查询数据库异常"})

    return JsonResponse({"err": "注册成功"})



