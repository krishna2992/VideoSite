from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import SignupForm, UserSignupForm
from app.models import Channel, Item
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('Account:home')
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        type = request.POST.get('login_type', None)
        if not type:
            raise Http404('Does not found')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if type=='channel' and  not user.channel:
                    raise Http404('Does not found')
                login(request, user)
                # Redirect to a success page or the 'next' URL if it exists
                request.session['auth_type'] = type
                next_url = request.GET.get('next')
                if next_url:
                    response = redirect(next_url)
                    
                elif type == 'channel':
                    response = redirect('app:channel_home')
                else:
                    response =  redirect('Account:home')
                return response  # Redirect to home page if 'next' parameter not present
    return render(request, 'User/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('app:index')  # Replace 'home' with the name of your homepage URL pattern.


def channel_signup_view(request):
    if request.method != 'POST':
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            channel = form.save()
            login(request, channel.user)
            request.session['auth_type'] = 'channel'
            return redirect('app:channel_home')
    return render(request, 'Channel/channel_signup.html', {'form': form, 'head':'Channel Signup'})


def user_signup_view(request):
    if request.method != 'POST':
        form = UserSignupForm()
    else:
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(username=user.username,
                    password=request.POST['password1'])
            login(request,authenticated_user)
            return redirect('Account:home')
    
    return render(request, 'User/user_signup.html', {'form': form, 'head':'Signup'})




@login_required
def user_home(request):
    context = {'head':'Home'}
    cookie_value = request.session.get('auth_type')
    if cookie_value == 'channel':
        return redirect('app:channel_home')
    

    context={
        'num-pages':1,
        'page':1,
    }
    if request.user.channel:
        items = Item.objects.filter(channel=request.user.channel)
        paginator = Paginator(items, settings.DEFAULT_PAGINATOR_PAGE_SIZE)  # Show 10 images per page
        context = {
            'num_pages': paginator.num_pages,
            'page':1
        }

    
    return render(request,  'User/home.html', context=context)



    

