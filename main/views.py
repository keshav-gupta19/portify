from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from portfolio.models import Project,Portfolio,Experience,Education, Template

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email='theloonyguy@gmail.com',
                to = ['grdfaiyaz786@gmail.com'],
                reply_to=[email]
            )
            email.send()
            messages.success(request,"message sent successfully !!")
            return redirect('home')
    else:
        form = ContactForm()
    return render(request,'main/home.html',{'form':form})

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        password1 = request.POST['password1'].strip()

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Registration successful')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

        return redirect('register')
    else:
        return render(request, 'main/register.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # Replace 'home' with the name of your home view
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'main/login.html')
    
def logout_view(request):
    logout(request)
    return render(request,'main/home.html')


def dashboard_view(request,username):
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=user)
    except Portfolio.DoesNotExist:
        portfolio = None    
    templates = Template.objects.filter(user=user)
    base_url = "http://"+request.META['HTTP_HOST']
    print(base_url)
    return render(request,'main/dashboard.html',{'user':user,"portfolio":portfolio,'templates':templates,'base_url':base_url})