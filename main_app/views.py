from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from datetime import date, datetime
from .models import *
# added lines below for sandwich_new controller to help stack
# slices
import cv2
import numpy as np
import random


def index(request):
    return render(request, 'index.html')


def index_redirect(request):
    return redirect('/')


def about(request):
    return render(request, 'about.html')


def sandwich_index(request):
    # get all sandwiches
    # sandwiches = Sandwich.objects.filter(is_public=True)
    sandwiches = Sandwich.objects.all()
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches})


def random_slices():
    # loads top, middle and bottom into lists
    id = list(Photo.objects.values_list('id', flat=True))
    top = list(Photo.objects.values_list('top', flat=True))
    middle = list(Photo.objects.values_list('middle', flat=True))
    bottom = list(Photo.objects.values_list('bottom', flat=True))

    print("top_id is", id)
    print("top is", top)
    tops, middles, bottoms = [], [], []
    for i in range(len(top)):
        tops.append(f'{top[i]}_{str(id[i])}')
        middles.append(f'{middle[i]}_{str(id[i])}')
        bottoms.append(f'{bottom[i]}_{str(id[i])}')
    print("tops is", tops)

    # randomizes the top, middle and bottom lists
    tops = random.sample(tops, len(tops))
    middles = random.sample(middles, len(middles))
    bottoms = random.sample(bottoms, len(bottoms))
    print("top is", tops)
    print("middle is", middles)
    print("bottom is", bottoms)
    # joins them into a string to be used by javascript
    top_string = ','.join(tops)
    middle_string = ','.join(middles)
    bottom_string = ','.join(bottoms)
    # pass these strings into the new.html template which
    # should have a line to connect to toggle.js
    return (top_string, middle_string, bottom_string)
# contains new page that has all of the image slices as strings


def sandwich_new(request):
    (top_string, middle_string, bottom_string) = random_slices()
    # tops = top_string.split(',')
    # for element in tops:
    #     top = element.split("_")[0]
    #     print("top in sandwich new", top)

    # print("Top string is", top_string)
    # print("Middle string is", middle_string)
    # print("Bottom string is", bottom_string)
    # , 'top': tops, 'middle': middles, 'bottom': bottoms})
    return render(request, 'sandwich/new.html', {'top_string': top_string, 'middle_string': middle_string, 'bottom_string': bottom_string})


# contains the edit page, which is essentially new but with a specific photo
# to start and everytime you toggle
def sandwich_edit(request, top_id, middle_id, bottom_id):
    (top_string, middle_string, bottom_string) = random_slices()
    top = Sandwich.objects.get(id=top_id).top
    middle = Sandwich.objects.get(id=middle_id).middle
    bottom = Sandwich.objects.get(id=bottom_id).bottom
    (top, middle, bottom) = (sandwich_top, sandwich.middle, sandwich.bottom)
    # , 'top': top, 'middle': middle, 'bottom': bottom})
    return render(request, 'sandwich/new.html', {'top_string': top_string, 'middle_string': middle_string, 'bottom_string': bottom_string})


# this is activated when the button save it is
# clicked on the new.html template
def sandwich_create(request, top_id, middle_id, bottom_id):
    if (request.user):
        sandwich = Sandwich.objects.create(
            top_id=top_id,
            middle_id=middle_id,
            bottom_id=bottom_id,
            user=request.user,
        )
        sandwich.save()
        return redirect('/sandwiches/')
    else:
        return redirect('/accounts/signup/')
    """
        After successful sandwich creation,
        either redirect the user to the new sandwich's detail page,
        or to the full gallery.
        eg: return redirect('/sandwiches/{sandwich.id}')
        or return redirect('/sandwiches/')
    """


def sandwich_detail(request, sandwich_id):
    # get sandwich
    sandwich = Sandwich.objects.filter(id=sandwich_id)
    if (sandwich):
        return render(request, f'/sandwiches/{sandwich_id}', {'sandwich': sandwich})
    else:
        return redirect('/sandwiches/')


@ login_required
def sandwich_update(request, sandwich_id):
    return redirect(f'/sandwiches/{sandwich_id}')


def user_profile(request, user_id):
    if request.user.id == user_id:
        # we queried slices, sandwiches AND user because
        # we assume a gallery for photos and sandwiches
        # would be displayed on the profile
        # get user
        photos = Photo.objects.filter(user_id=user_id)
        sandwiches = Sandwich.objects.filter(user_id=user_id)
        user = User.objects.get(id=user_id)
        return render(request, 'user/profile.html', {'photos': photos, 'sandwiches': sandwiches, 'user': user})
    else:
        raise PermissionDenied


@ login_required
def user_profile_edit(request, user_id):
    if request.user.id == user_id:
        # get user
        return render(request, 'user/profile_edit.html', {})
    else:
        raise PermissionDenied


@ login_required
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
    sandwiches = Sandwich.objects.filter(user_id=user_id)
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches})


@ login_required
def user_photo_gallery(request, user_id):
    if request.user.id == user_id:
        # get all photo slice groups belonging to user
        return render(request, 'user/photo/gallery.html', {})
    else:
        raise PermissionDenied


@ login_required
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
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
