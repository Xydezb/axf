from django.db import models

# Create your models here.
 #用户表
class User(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False, blank=True, verbose_name="姓名")
    password = models.CharField(max_length=255, verbose_name="密码")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    GENDER = (
        ("male", "男"),
        ("female", "女")
    )
    gender = models.CharField(max_length=6, choices=GENDER, default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        db_table = 'user'

