from django.forms import ModelForm
from django import forms
from .models import Trade, Middleman
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TradeForm(ModelForm):
    middleman = forms.ModelChoiceField(queryset=Middleman.objects.all())
    def __init__(self, uid, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
        self.fields['middleman'].queryset = Middleman.objects.exclude(garlic_user_id=uid)

    class Meta:
        model = Trade
        fields = ['item_1', 'item_2', 'middleman']
        labels = {'item_1': "I am trading", 'item_2': 'for'}

class SignUpForm(UserCreationForm):
    address = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'address', ]