from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from datetime import date
from .models import *

def index(request):
    return render(request, 'index.html')

def index_redirect(request):
    return redirect('/')

def about(request):
    return render(request, 'about.html')

def sandwich_index(request):
    # get all sandwiches
    return render(request, 'sandwich/gallery.html')

def sandwich_new(request):
    return render(request, 'sandwich/new.html')

def sandwich_next(request, top_id, middle_id, bottom_id):
    pass

@login_required
def sandwich_create(request):
    """ 
        After successful sandwich creation,
        either redirect the user to the new sandwich's detail page,
        or to the full gallery.
        eg: return redirect('/sandwiches/{sandwich.id}')
        or return redirect('/sandwiches/')
    """
    pass

def sandwich_detail(request, sandwich_id):
    # get sandwich
    return render(request, 'sandwich/detail.html', {})

@login_required
def sandwich_edit(request, sandwich_id):
    # get sandwich
    # if request.user.id == sandwich.user_id
    return render(request, 'sandwich/edit.html')
    # else
    # raise PermissionDenied

@login_required
def sandwich_update(request, sandwich_id):
    return redirect(f'/sandwiches/{sandwich_id}')

def user_profile(request, user_id):
    # get user 
    return render(request, 'user/profile.html', {})

@login_required
def user_profile_edit(request, user_id):
    if request.user.id == user_id: 
        # get user
        return render(request, 'user/profile_edit.html', {})
    else:
      raise PermissionDenied  

@login_required
def user_profile_update(request, user_id):
    if request.user.id == user_id: 
    # get user
    # apply form data
    # save user
        return redirect(f'/users/{user_id}')
    else:
        raise PermissionDenied  

def user_sandwich_gallery(request, user_id):
    # get all sandwiches created by user
    return render(request, 'sandwich/gallery.html', {})

@login_required
def user_photo_gallery(request, user_id):
    if request.user.id == user_id: 
        # get all photo slice groups belonging to user
        return render(request, 'user/photo/gallery.html', {})
    else:
        raise PermissionDenied 

@login_required
def user_photo_detail(request, user_id, top_id, middle_id, bottom_id):
    if request.user.id == user_id: 
        # get photo slice group
        return render(request, 'user/photo/detail.html', {})
    else:
        raise PermissionDenied 


### USER SIGNUP ###
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)