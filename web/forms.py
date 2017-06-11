#coding:utf-8
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=10, widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "username", 'placeholder': "用户名"}))
    password = forms.CharField(label="密码", max_length=10, widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "password", 'placeholder': "密码"}))
