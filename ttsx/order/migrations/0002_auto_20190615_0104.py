# Generated by Django 2.0.7 on 2019-06-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_CLOSE', '交易关闭'), ('TRADE_FINISHED', '交易结束'), ('WAIT_BUYER_PAY', '交易创建'), ('TRADE_SUCCESS', '成功'), ('paying', '待支付')], default='paying', max_length=20, verbose_name='交易状态'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='post_script',
            field=models.CharField(default='', max_length=200, verbose_name='订单留言'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='signer_mobile',
            field=models.CharField(default='', max_length=11, verbose_name='联系电话'),
        ),
    ]
