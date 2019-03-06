from django.contrib import admin
from django.urls import path, include
from . import api, passport

api_v1_url = [
    # path('image_codes/<slug:image_code_id>',),
    path('image_codes/', api.image_codes.as_view()),
    path('register/', passport.register),
    path('get_sms_code/', api.get_sms_code),
    path('login/', api.login),
    path('check_login/', api.check_login),
    path('logout/', api.logout),
    path('area/', api.area),
    path('change_user_name/', api.change_user_name),
    path('get_user_info/', api.get_user_info),
    path('save_house_info/', api.save_house_info),
    path('save_house_image/', api.save_house_image),
    path('order_pay/', api.order_pay),
    path('save_order_payment_result/', api.save_order_payment_result),

]

urlpatterns = [
    path('api/v1/', include(api_v1_url))
]
