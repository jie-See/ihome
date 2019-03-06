from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=32, unique=True)
    password_hash = models.CharField(max_length=128)
    mobile = models.CharField(max_length=11)
    real_name = models.CharField(max_length=32, null=True)
    id_card = models.CharField(max_length=20, null=True)
    avatar = models.CharField(max_length=128, null=True)

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    @property
    def password(self):
        raise AttributeError("这个属性只能设置，不能读写")

    @password.setter
    def password(self, value):
        self.password_hash = make_password(value,"a",'pbkdf2_sha256')

    def check_password(self, passwd):
        """
        验证密码的正确性
        :return:正确返回True,否则返回False
        """
        print("11", self.password_hash)
        print("22", make_password(passwd,"a",'pbkdf2_sha256'))
        print(check_password(self.password_hash, passwd))
        return check_password(passwd, self.password_hash)

    def to_dict(self):
        user_dict = {
            'name': self.name,
            'mobile': self.mobile,
            'avatar': self.avatar,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return user_dict



class Facility(models.Model):
    name = models.CharField(max_length=32, verbose_name='设施名字')

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')





class House(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='房屋主人')
    title = models.CharField(max_length=64, verbose_name='标题')
    price = models.IntegerField(default=0, verbose_name='价格')
    address = models.CharField(max_length=512, verbose_name='地址')
    room_count = models.IntegerField(default=1, verbose_name='房间数量')
    acreage = models.IntegerField(default=0, verbose_name='房屋面积')
    unit = models.CharField(max_length=32, default='', verbose_name='房屋单元')
    capacity = models.IntegerField(default=1, verbose_name='房屋容纳人数')
    beds = models.CharField(max_length=64, verbose_name='床铺配置', default='')
    deposit = models.IntegerField(default=0, verbose_name='房屋押金')
    min_days = models.IntegerField(default=1, verbose_name='最少入住天数')
    max_days = models.IntegerField(default=0, verbose_name='最多入住天数')
    order_count = models.IntegerField(default=0, verbose_name='完成订单数')
    index_image_url = models.CharField(max_length=256, verbose_name='房屋主图片路径')
    facilities = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name='房屋设施')

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Area(models.Model):
    name = models.CharField(max_length=32)

    def to_dict(self):
        """将对象转化为字典"""
        d = {
            'aid': self.id,
            'aname': self.name
        }
        return d




class HouseImage(models.Model):
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    url = models.CharField(max_length=256, verbose_name='图片路径')

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')




class Order(models.Model):

    WAIT_ACCEPT = 0
    WAIT_PAYMENT = 1
    PAID = 2
    WAIT_COMMENT = 3
    COMPLETE = 4
    CANCELED = 5
    REJECTED = 6
    STATUS_TYPE = {
        WAIT_ACCEPT: '待接单',
        WAIT_PAYMENT: '待支付',
        PAID: '已支付',
        WAIT_COMMENT: '待评价',
        COMPLETE: '已完成',
        CANCELED: '已取消',
        REJECTED: '已拒单'
    }

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    begin_data = models.DateField(verbose_name='预定的开始时间')
    end_date = models.DateField(verbose_name='预定的结束时间')
    days = models.IntegerField(default=1, verbose_name='预定的总天数')
    house_price = models.IntegerField(verbose_name='房屋单价')
    amount = models.IntegerField(verbose_name='订单总金额')
    status = models.SmallIntegerField(verbose_name='订单状态', choices=STATUS_TYPE.items())
    comment = models.TextField(max_length=128, verbose_name='拒单原因')
    trade_no = models.CharField(max_length=128, verbose_name='交易编号')

    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
