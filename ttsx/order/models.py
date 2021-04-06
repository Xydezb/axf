from django.db import models

from goods.models import Goods
from user.models import User


class OrderInfo(models.Model):
    """
	订单模型
	"""
    ORDER_STATUS = {
	    ('TRADE_SUCCESS', '成功'),
	    ('TRADE_CLOSE', '交易关闭'),
	    ('WAIT_BUYER_PAY', '交易创建'),
	    ('TRADE_FINISHED', '交易结束'),
	    ('paying', '待支付')
	    }

    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='交易号')
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=20, verbose_name='交易状态')
    post_script = models.CharField(max_length=200, verbose_name='订单留言',default='')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='支付时间')

    # 用户收货信息
    address = models.CharField(max_length=200, default='', verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='收货人')
    signer_mobile = models.CharField(max_length=11,default='', verbose_name='联系电话')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_order'


class OrderGoods(models.Model):
    """
	订单详情商品信息模型
	"""
    order = models.ForeignKey(OrderInfo, verbose_name='订单详情', related_name='goods', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    goods_nums = models.IntegerField(default=0, verbose_name='数量')

    class Meta:
        db_table = 'f_order_goods'


#收货地址表
class UserAddress(models.Model):
    user = models.CharField(max_length=25, null=False, verbose_name='用户名字')
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    signer_postcode = models.CharField(max_length=11, default='', verbose_name='邮编')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'user_address'