from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login as auth_login
from .models import *

from .helper import orderTeams
def index(request):
    # Display team standings
    context = { 'teams': orderTeams() }
    return render(request, 'view/index.html', context)

def refereeIndex(request):
    # If user isn't logged in, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    # If user doesn't have referee permissions, raise 403
    if not request.user.groups.filter(name='referee').exists():
        raise PermissionDenied()

    # If user has permissions, list assigned teams and problems
    context = {
        'user': request.user,
        'teams': request.user.referee.assignedTeams.all(),
        'problems': Problem.objects.all(),
    }

    return render(request, 'referee/index.html', context)

def manageIndex(request):
    return render(request, 'manage/index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'utils/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # If authentication is succesful, login user and redirect
        if user is not None:
            auth_login(request, user)
            
            # if user is a referee, redirect to referee page
            if user.groups.filter(name='referee').exists():
                return redirect('refereeIndex')
            
            # If user is a manager, redirect to manager page
            if user.groups.filter(name='manager').exists():
                return redirect('manageIndex')

            # If user is neither, redirect to default index
            return redirect('index')

        # If authentication isn't succesful, resend form
        context = { 'unsuccesfull': True }
        return render(request, 'utils/login.html', context)        