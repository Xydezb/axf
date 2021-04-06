from django import forms



class addressForm(forms.Form):
    #收货地址用表单校验

    filename = forms.CharField(required=True,
                        error_messages={
                        'required': '收货人必填'
                        })
    address = forms.CharField(required=True,
                        error_messages={
                        'required':'请填写详细地址'
                        })

    zipcode = forms.IntegerField(required=False)
    number = forms.CharField(required=True,max_length=11,min_length=11,
                        error_messages={
                        'required':'亲，手机号不填拿不到货哦',
                        'max_length':'手机号码有误',
                        'min_length':'手机号码有误',
                                })
    def clean(self):
        return self.cleaned_data
