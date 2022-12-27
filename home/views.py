from django.shortcuts import render, redirect
from django.contrib import messages
from home.forms import add_product_product, NewCommentForm
from .views import *
from .models import *
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as u
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

@login_required(login_url="/login")
def home_page(request):
    data = add_product.objects.all()
    return render(request, 'home/index.html',{ 
        'data' : data 
    })

@login_required(login_url="/login")
def productDetail(request, pk):
    #data = add_product.objects.get(id=pk)
    #receive data from html and save in NewCommentForm and refresh current page
    #that is being handled in websocket
    try:
        comments = Comments.objects.filter(post=add_product.objects.get(id=pk))
        #comments = Comments.objects.get(id=pk)
    except:
        comments = 'code0'
    products = add_product.objects.get(id=pk)
    #for now nothing
    subc = None
    username = request.user
        
    return render(request, 'product/productdetails.html', 
        {
            'cm': comments,
            'ud': pk,
            'product': products,
            'comments': comments,
            'subc' : subc,
        }
    )
    #receive data sent by productdetails.html file

@login_required
def productDelete(pk):
    try:
        sa = add_product.objects.get(id=pk)
        sa.delete()
        print('item deleted')
    except Exception as r:
        print("unable to delete {}".format(pk))

@login_required(login_url="/login")
def addProduct(request):
    form = add_product_product()
    if request.method == 'POST':
        user_form = add_product_product(request.POST, request.FILES)
        #sv = user_form['image']
        if user_form.is_valid():
            print('valid data')
            user_form.save()
            print('form saved!!')
            messages.success(request,'Added item')
    else:

        messages.error(request,'Posted error')
        print('Error saving product!!')
    return render(request, 'product/addpage.html',context={

        'data' : form,
    
    })

#Below here will be register and login

def Login_form(request):
    if request.user.is_authenticated:
      return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            isr = authenticate(request,username=username,password=password)
            if isr is not None:
                login(request, isr)
                return redirect("/")
            else:
                messages.error(request, "Username or password incorrect")
        return render(request,'login/index.html')

def logout_form(request):
    logout(request)
    return redirect('/')

def register_form(request):
    if request.POST == 'POST':
        user1 = request.POST['username']
        print('getting the username {}'.format(user1))
        user = User.objects.create_user(user1)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.save()
        messages.success(request, 'user saved success')
    else:
        messages.error(request, 'Not registered !')
        print('Error saving the register')
    return render(request, 'login/register.html')
######################------------------------------------############

from .forms import UpdateUserForm, UpdateProfileForm

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'login/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'login/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


