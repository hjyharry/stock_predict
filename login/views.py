from django.shortcuts import render, redirect
# Create your views here.
# login/views.py
from . import models
from stock.models import myFavourite
from .form import UserForm,RegisterForm
from django.http import HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json


def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')

    login_form = UserForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey':hashkey,'image_url':image_url}

    if request.method == "POST":
        login_form = UserForm(request.POST)
        capt = request.POST.get("captcha",None)
        key = request.POST.get("hashkey",None)
        message = ""
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name = username)
                if user.password == password:
                    if jarge_captcha(capt,key):
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        return redirect('/index/')
                    else:
                        message = "验证码错误"
                else:
                    message = "密码不正确"
            except:
                message = "用户名不存在"
        return render(request,'login/login.html', {"login_form":login_form,"message":message})

    return render(request,'login/login.html', {"login_form":login_form,"captcha":captcha})

def register(request):
    register_form = RegisterForm()
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    message = ""
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        capt = request.POST.get("captcha", None)
        key = request.POST.get("hashkey", None)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            pwd_0 = register_form.cleaned_data['password_0']
            pwd_1 = register_form.cleaned_data['password_1']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if pwd_0 != pwd_1:
                message = "两次密码输入不同，请重新输入"
                return render(request,"login/register.html",locals())
            else:
                same_name_user = models.User.objects.filter(name = username)
                if same_name_user:
                    message = "用户名已存在，请重新输入"
                    return render(request,"login/register.html",locals())
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    message = "邮箱已存在，请使用其他邮箱"
                    return render(request,"login/register.html",locals())
                if jarge_captcha(capt,key):
                    new_user = models.User.objects.create()
                    new_user.name = username
                    new_user.password = pwd_0
                    new_user.email = email
                    new_user.sex = sex
                    new_user.save()

                    return redirect('/login/')
                else:
                    message = "验证码错误"
                    return render(request,"login/register.html",locals())

    return render(request,"login/register.html",locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index')
    request.session.flush()
    return redirect('/index')

#创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey':hashkey,'image_url':image_url}
    return captcha

#验证验证码
def jarge_captcha(captchaStr,captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
        return False

def refresh_captcha(request):
    new_key = CaptchaStore.pick()
    to_json_response = {
        "hashkey": new_key,
        "image_url": captcha_image_url(new_key),
    }
    return HttpResponse(json.dumps(to_json_response), content_type="application/json")


def home(request):
    user_id = request.session.get('user_id')
    if not models.User_info.objects.filter(id=user_id):
        user_info = {
            "id":models.User.objects.filter(id = user_id)[0]
        }
        models.User_info.objects.create(**user_info)
    info = models.User_info.objects.filter(id = int(user_id)).values()

    #判断用户是否喜欢列表
    list_num = len(list(myFavourite.objects.filter(id = user_id).values()))
    if list_num == 0:
        favourite_list = []
    else:
        favourite_list = list(myFavourite.objects.filter(id = user_id).values('code','code__cur_stock__NAME','code__cur_stock__PRICE','code__cur_stock__OPEN','code__cur_stock__HIGH','code__cur_stock__LOW'))
    return render(request,'login/home.html',{"user_info":info,"favourite_list":favourite_list})