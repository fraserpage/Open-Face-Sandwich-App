from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from datetime import date
from .models import *
# added lines below for sandwich_new controller to help stack
# slices
import cv2
import numpy as np


def index(request):
    return render(request, 'index.html')


def index_redirect(request):
    return redirect('/')


def about(request):
    return render(request, 'about.html')


def sandwich_index(request):
    # get all sandwiches
    sandwiches = Sandwich.objects.get(is_public=True)
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches})


def sandwich_new(request):
    top_slices = Slices.objects.values_list('top')
    middle_slices = Slices.objects.values_list('middle')
    bottom_slices = Slices.objects.values_list('bottom')
    return render(request, 'sandwich/new.html', {'top': top_slices, 'middle': middle_slices, 'bottom': bottom_slices})


def sandwich_next(request, top_id, middle_id, bottom_id):
    top_link = Slices.objects.get(id=top_id)
    middle_link = Slices.objects.get(id=middle_id)
    bottom_link = Slices.objects.get(id=bottom_id)
    top = cv2.imread(top_link)
    middle = cv2.imread(middle_link)
    bottom = cv2.imread(bottom_link)
    h1, w1, c1 = top.shape
    h2, w2, c2 = middle.shape
    h3, w3, c3 = bottom.shape
    h, w = h1+h2+h3, max(w1, w2, w3)
    out_image = np.zeros((h, w, c1))
    out_image[:h1, :w1, ] = top
    out_image[h1:h1+h2, :w2, ] = middle
    out_image[h1+h2:h1+h2+h3, :w3, ] = bottom
    return out_image
    # cv2.imwrite(r"Vertical.jpg", out_image)
    # renders the page that has the top, middle and bottom arrays
    # have to query the top, middle and bottoms then pass them into new.html
    # add event listener to toggle arrow.
    # every time the arrow is clicked, a random id is picked from top,
    # bottom, or middle arrays to make a new slice appear
    # back arrow should not be random, only front arrow.
    # pass


# @login_required
def sandwich_create(request):
    if (request.user.is_authenticated()):
        out_image = sandwich_next(request, top_id, middle_id, bottom_id)
        cv2.imwrite(r"Vertical.jpg", out_image)
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
    # pass


def sandwich_detail(request, sandwich_id):
    # get sandwich
    sandwich = Sandwich.objects.get(id=sandwich_id)
    return render(request, f'/sandwiches/{sandwich_id}', {'sandwich': sandwich})


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


@login_required
def user_profile(request, user_id):
    if request.user.id == user_id:
        # we queried slices, sandwiches AND user because
        # we assume a gallery for photos and sandwiches
        # would be displayed on the profile
        # get user
        slices = Slices.objects.get(user_id=user_id)
        sandwiches = Sandwich.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        return render(request, 'user/profile.html', {'slices': slices, 'sandwiches': sandwiches, 'user': user})
    else:
        raise PermissionDenied


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
    sandwiches = Sandwich.objects.get(user_id=user_id)
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches})


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
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
