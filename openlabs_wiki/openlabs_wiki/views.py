from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.context_processors import csrf


def login(request):
    """
    This takes the user credentials from the html page
    """
    context = {}
    context.update(csrf(request))
    return render_to_response('login.html', context)


def auth_view(request):
    """
    It checks for authentication of username and password and logsin the user
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/wiki')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    """
    This view lands the user to page that is private to the user after he
    logs in
    """
    return render_to_response(
        'loggedin.html', {
            'full_name': request.user.username
        }
    )


def invalid_login(request):
    """
    view to handle invalid login credentials
    """
    return render_to_response('invalid_login.html')


def logout(request):
    """view to handle logout"""
    auth.logout(request)
    return HttpResponseRedirect('/wiki')


def register_user(request):
    """view to handle user registration for the site"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/accounts/register_success')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    return render_to_response('register.html', args)


def register_success(request):
    """view to handle successful registration"""
    return render_to_response('register_success.html')
