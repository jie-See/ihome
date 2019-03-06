import json
import os
import re
from urllib.parse import parse_qs

from common.redis import rds
from django.views import View
from django.http import HttpResponse, JsonResponse
from ihomeapp.verify_code import get_image_code
from .models import User, Area, House, Facility, HouseImage, Order
import random
from libs.yuntongxun.SendTemplateSMS import CCP
from common.commons import login_required
# from tasks.task_sms import send_sms
from tasks.sms.tasks import send_sms
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from alipay import AliPay

class image_codes(View):
    def get(self, request):
        """
        获取图片验证码
        :param request: a：验证码编号
        :return: 验证码图片
        """
        b = request.GET.get('a')
        name, text, image_data = get_image_code(b)
        return HttpResponse(image_data, content_type='image/jpg')

    def post(self, request):
        a = json.loads(request.body.decode())
        bianma = a['bianma']
        code = a['code']
        if rds.get("image_code_%s" % bianma):
            if code == rds.get("image_code_%s" % bianma).decode():
                rds.delete("image_code_%s" % bianma)
                return JsonResponse({"msg": "ok"})
            else:
                return JsonResponse({"msg": "no"})
        else:
            return JsonResponse({"msg": "cuowu"})


# def verify_code(request):
#     a = json.loads(request.body.decode())
#     b = a['a']
#
#     name, text, image_data = get_image_code(b)
#     return HttpResponse(image_data, content_type='image/jpg')

# 非异步处理发送短信
# def get_sms_code(request):
#     """
#     获取短信验证码
#     :param request: mobile,image_code,image_code_id
#     :return: code:0 成功 -1失败
#     """
#     image_code = request.GET.get('image_code')
#     image_code_id = request.GET.get('image_code_id')
#     mobile = request.GET.get('mobile')
#
#     if not all([image_code, image_code_id, mobile]):
#         # 参数不完整
#         return JsonResponse({"err": "参数不完整"})
#
#     # 业务逻辑处理
#     # 从redis中取出真实的图片验证码
#     try:
#         real_image_code = rds.get('image_code_%s' % image_code_id)
#     except Exception as e:
#         return JsonResponse({"err": "redis数据库异常"})
#
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         return JsonResponse({"err": "图片验证码失效"})
#
#     # 删除图片验证码
#     try:
#         rds.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         print(e)
#
#     # 与用户填写的值进行对比
#     if real_image_code.decode().lower() != image_code.lower():
#         return JsonResponse({"err": "图片验证码错误"})
#
#     # 判断60s内是否有发送短信
#     try:
#         send_flag = rds.get("send_sms_code_%s" % mobile)
#     except Exception as e:
#         print(e)
#     else:
#         if send_flag is not None:
#             return JsonResponse({"err": "请求过于频繁"})
#
#     # 判断手机号是否存在
#     try:
#         user = User.objects.filter(mobile=mobile).first()
#     except Exception as e:
#         print(e)
#     else:
#         if user is not None:
#             # 表示手机号已存在
#             return JsonResponse({"err": "手机号已存在"})
#
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     # 保存真实的短信验证码
#     try:
#         # rds.setex("sms_code_%s" % mobile, 300, sms_code)
#         rds.set("sms_code_%s" % mobile, sms_code)
#         # 保存发送给这个手机号码的记录，防止用户再60s内再次发送短信的操作
#         rds.setex("send_sms_code_%s" % mobile, 60, 1)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"err": "保存短信验证码异常"})
#     try:
#         ccp = CCP()
#         result = ccp.send_template_sms(mobile, [sms_code, 5], 1)
#     except Exception as e:
#         print(e)
#
#     if result == 0:
#         return JsonResponse({"msg": "发送成功", "code": 0})
#     else:
#         return JsonResponse({"msg": "发送失败", "code": -1})

# 异步处理发送短信
def get_sms_code(request):
    """
    获取短信验证码
    :param request: mobile,image_code,image_code_id
    :return: code:0 成功 -1失败
    """
    image_code = request.GET.get('image_code')
    image_code_id = request.GET.get('image_code_id')
    mobile = request.GET.get('mobile')

    if not all([image_code, image_code_id, mobile]):
        # 参数不完整
        return JsonResponse({"err": "参数不完整"})

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = rds.get('image_code_%s' % image_code_id)
    except Exception as e:
        return JsonResponse({"err": "redis数据库异常"})

    # 判断图片验证码是否过期
    if real_image_code is None:
        return JsonResponse({"err": "图片验证码失效"})

    # 删除图片验证码
    try:
        rds.delete("image_code_%s" % image_code_id)
    except Exception as e:
        print(e)

    # 与用户填写的值进行对比
    if real_image_code.decode().lower() != image_code.lower():
        return JsonResponse({"err": "图片验证码错误"})

    # 判断60s内是否有发送短信
    try:
        send_flag = rds.get("send_sms_code_%s" % mobile)
    except Exception as e:
        print(e)
    else:
        if send_flag is not None:
            return JsonResponse({"err": "请求过于频繁"})

    # 判断手机号是否存在
    # try:
    #     user = User.objects.filter(mobile=mobile).first()
    # except Exception as e:
    #     print(e)
    # else:
    #     if user is not None:
    #         # 表示手机号已存在
    #         return JsonResponse({"err": "手机号已存在"})

    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码
    try:
        # rds.setex("sms_code_%s" % mobile, 300, sms_code)
        rds.set("sms_code_%s" % mobile, sms_code)
        # 保存发送给这个手机号码的记录，防止用户再60s内再次发送短信的操作
        rds.setex("send_sms_code_%s" % mobile, 60, 1)
    except Exception as e:
        print(e)
        return JsonResponse({"err": "保存短信验证码异常"})
    # 发送短信
    send_sms.delay(mobile, [sms_code, 5], 1)
    return JsonResponse({"msg": "发送成功", "code": 0})


def login(request):
    """
    登录
    :param request: 手机号，密码
    :return: 成功，失败
    """
    req = json.loads(request.body.decode())
    mobile = req['mobile']
    password = req['password']
    if not all([mobile, password]):
        # 参数不完整
        return JsonResponse({"err": "参数不完整"})

    # 手机号的格式
    if not re.match(r'1[34567]\d{9}', mobile):
        return JsonResponse({"err": "手机号格式错误"})

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求ip"："次数"
    user_ip = request.META['REMOTE_ADDR']
    try:
        access_nums = rds.get("access_num_%s" % user_ip).decode()
        print(type(access_nums), access_nums)
    except Exception as e:
        print(e)
    else:
        if access_nums is not None and int(access_nums) >= 5:
            return JsonResponse({"err": "错误次数过多，请稍后重试"})

    try:
        user = User.objects.filter(mobile=mobile).first()
    except Exception as e:
        print(e)
        return JsonResponse({"err": "获取用户信息失败"})

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            rds.incr("access_num_%s" % user_ip)
            rds.expire("access_num_%s" % user_ip, 300)
        except Exception as e:
            print(e)
        return JsonResponse({"err": "用户名或密码错误"})

    # 如果验证相同成功，保存登录状态，再session中
    request.session["islogin"] = True
    return JsonResponse({"msg": "登录成功"})


def check_login(request):
    # 尝试从session中获取用户的名字
    name = request.session.get("name")
    # 如果session中数据name名字存在， 则表示用户已登录，否则未登录
    if name is not None:
        return JsonResponse({"err": "tree"})
    else:
        return JsonResponse({"err": "false"})


def logout(request):
    # 清除session
    request.session.clear()
    return JsonResponse({"err": "ok"})


def area(request):
    # 尝试从redis中读取数据
    try:
        resp_json = rds.get("area_info")
    except Exception as e:
        print(e)
    else:
        if resp_json is not None:
            return JsonResponse({"data": json.loads(resp_json.decode()), "is": "yes"})

    try:
        area_li = Area.objects.all()
    except Exception as e:
        return JsonResponse({"err": "数据库异常"})

    area_dict_li = []
    for area in area_li:
        area_dict_li.append(area.to_dict())

    # 将数据保存到redis中

    areas = json.dumps(area_dict_li)
    try:
        rds.setex("area_info", 300, areas)
    except Exception as e:
        print(e)
    return JsonResponse({"data": area_dict_li, "is": "no"})


@login_required
def change_user_name(request):
    """修改用户名"""
    data = json.loads(request.body.decode())
    userid = data['userid']
    change_name = data['changename']
    if not all([userid, change_name]):
        return JsonResponse({"err": "参数不完整"})
    try:
        user = User.objects.get(mobile=userid)
    except Exception as e:
        return JsonResponse({"err": "不存在该用户"})

    user.name = change_name
    user.save()
    return HttpResponse("ok")


@login_required
def get_user_info(request):
    mobile = request.GET.get('mobile')
    user = User.objects.filter(mobile=mobile).first()
    data = user.to_dict()
    return JsonResponse({"data": data})


@login_required
def save_house_info(request):
    data = json.loads(request.body.decode())
    house = House()
    facility = Facility.objects.filter(id=data['facilities']).first()
    user = User.objects.filter(id=data['userid']).first()
    house.title = data['title']
    house.price = data['price']
    house.address = data['address']
    house.room_count = data['room_count']
    house.acreage = data['acreage']
    house.unit = data['unit']
    house.capacity = data['capacity']
    house.beds = data['beds']
    house.deposit = data['deposit']
    house.min_days = data['min_days']
    house.max_days = data['max_days']
    house.order_count = data['order_count']
    house.facilities = facility
    house.user_id = user
    house.save()
    return JsonResponse({'msg': 'ok'})


@login_required
def save_house_image(request):
    data = json.loads(request.body.decode())
    house = House.objects.filter(id=data['house_id']).first()
    house_image = HouseImage()
    house_image.house_id = house
    house_image.url = data["url"]
    house_image.save()
    return JsonResponse({'msg': 'ok'})


def get_house_list(request):
    """获取房屋的列表信息（搜索页面）"""
    # start_date = request.GET.get('sd')
    # end_date = request.GET.get('ed')
    # area_id = request.GET.get('aid')
    # sort_key = request.GET.get('sk')
    # # page = request.GET.get('p')
    #
    # # 处理时间
    # try:
    #     if start_date:
    #         start_date = datetime.strftime(start_date, "%Y-%m-%d")
    #
    #     if end_date:
    #         end_date = datetime.strftime(end_date, "%Y-%m-%d")
    #
    #     if start_date and end_date:
    #         assert start_date <= end_date
    # except Exception as e:
    #     return JsonResponse({"err": "日期参数有误"})
    #
    # # 判断区域id
    # try:
    #     area = Area.objects.filter(id=area_id)
    # except Exception as e:
    #     return JsonResponse({"err": "区域参数有误"})
    #
    # try:
    #     page = int(page)
    # except Exception as e:
    #     page = 1

    # 查询数据库
    house_list = House.objects.filter().all()

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(house_list, 1)

    #从前端获取当前的页码数,默认为1
    page = request.GET.get('p', 1)

    try:
        print(page)
        list = paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return JsonResponse({"data": list})


@login_required
def order_pay(request):
    """发起支付宝支付"""
    data = json.loads(request.body.decode())
    order_id = data['order_id']
    # 判断订单状态
    try:
        order = Order.objects.filter(id=order_id).first()
    except Exception as e:
        return JsonResponse({"err": "数据库异常"})

    if order is None:
        return JsonResponse({"err": "订单数据有误"})

    # 创建支付宝sdk的工具对象
    app_private_key_string = open(os.path.join(os.path.dirname(__file__), "key\\app_private_key.pem")).read()
    alipay_public_key_string = open(os.path.join(os.path.dirname(__file__), "key\\alipay_public_key.pem")).read()
    alipay_client = AliPay(
        appid="2016092500594174",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单编号
        total_amount=str(order.amount/100.0),  # 总金额
        subject=u"爱家租房 %s" % order.id,  # 订单标题
        return_url="https://www.baidu.com",  # 返回的链接地址
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 构建让用户跳转的支付连接地址
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return JsonResponse({"data": {"pay_url": pay_url}})


def save_order_payment_result(request):
    """保存订单支付结果"""
    data = request.body.decode()
    post_data = parse_qs(data)
    post_dict = {}
    # 支付宝的数据进行分离，提取出支付宝的签名参数sign和剩下的其他数据
    for k, v in post_data.items():
        post_dict[k] = v[0]
    alipay_sign = post_dict.pop("sign")

    app_private_key_string = open(os.path.join(os.path.dirname(__file__), "key\\app_private_key.pem")).read()
    alipay_public_key_string = open(os.path.join(os.path.dirname(__file__), "key\\alipay_public_key.pem")).read()
    alipay_client = AliPay(
        appid="2016092500594174",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    result = alipay_client.verify(post_dict, alipay_sign)
    if result:
        # 修改数据库的订单状态信息
        order_id = post_dict.get("out_trade_no")
        order = Order.objects.filter(id=order_id).first()
        order.status = 4
        order.save()
        return JsonResponse({"msg": "ok"})
    else:
        return JsonResponse({'err': 'error'})
