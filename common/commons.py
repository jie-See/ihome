# coding:utf-8
from django.http import JsonResponse
import functools

def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 判断用户的登录状态

        user_id = request.session.get("islogin")

        # 如果用户是登录的，执行视图函数
        if user_id is not None:
            return view_func(request, *args, **kwargs)
        else:
            # 如果未登录，返回未登录的信息
            return JsonResponse({"err": "用户未登录"})
            session
    return wrapper

