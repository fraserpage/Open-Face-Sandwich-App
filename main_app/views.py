# import re
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# from django.db import models
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
# from datetime import date
from .models import *
import uuid
import boto3
# import datetime
from PIL import Image
import io
# import cv2
# import numpy as np
import random

# Amazon S3 settings
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'open-face-sandwich'

# photo crop lines
crop__mid = 0.4 # top of mid block
crop_low = 0.68 # bottom of mid block

@login_required
def photo_new(request):
    return render(request, 'photo/new.html', {'crop_mid': crop__mid*100, 'crop_low': crop_low*100})

@login_required
def photo_save(request):
    image_file = request.FILES.get('image', None)
    if image_file:
        pil_image = Image.open(image_file)
        width = pil_image.width
        height = pil_image.height

        top_img = crop_image(pil_image,(0, 0, width, height * crop__mid))
        top_url = save_to_s3(top_img, image_file)
        
        middle_img = crop_image(pil_image,(0, height * crop__mid, width, height * crop_low))
        middle_url = save_to_s3(middle_img, image_file)

        bottom_img = crop_image(pil_image,(0, height * crop_low, width, height))
        bottom_url = save_to_s3(bottom_img, image_file)

        photo = Photo(
            top = top_url, 
            middle = middle_url, 
            bottom = bottom_url, 
            is_public = True,
            user = request.user)
        photo.save()
        return JsonResponse({'url':reverse('sandwich_from_photo',kwargs={'photo_id':photo.id})})
    else:
        # Something went wrong
        return JsonResponse({
            'url':reverse('photo_new'),
            'error':'There was an error saving the photo'
        })

# photo saving helper functions
def save_to_s3(image_file, orig_img):
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + orig_img.name[orig_img.name.rfind('.'):]
    s3.upload_fileobj(image_file, BUCKET, key)
    return f"{S3_BASE_URL}{BUCKET}/{key}"

def crop_image(image, crop):
    cropped_img = image.crop(crop)
    if cropped_img.mode != 'RGB':
        cropped_img = cropped_img.convert('RGB')

    in_mem_file = io.BytesIO()
    cropped_img.save(in_mem_file, format="JPEG")
    in_mem_file.seek(0)

    return in_mem_file

def photo_detail(request, id):
    photo = Photo.objects.get(id=id)
    return render(request, 'photo/detail.html', {'photo':photo})

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
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches, 'gallery_title': 'Sandwich Gallery', 'gallery_type': 'public'})


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
    return render(request, 'sandwich/workshop.html', {
        'top_string': top_string, 
        'middle_string': middle_string, 
        'bottom_string': bottom_string
    })

def sandwich_from_photo(request, photo_id):
    (top_string, middle_string, bottom_string) = random_slices()
    photo = Photo.objects.get(id=photo_id)
    return render(request, 'sandwich/workshop.html', {
        'top_string': top_string, 
        'middle_string': middle_string, 
        'bottom_string': bottom_string, 
        'top': photo.top, 
        'middle': photo.middle, 
        'bottom': photo.bottom, 
        'top_id': photo.id, 
        'middle_id': photo.id, 
        'bottom_id': photo.id
    })

def sandwich_edit(request, sandwich_id, top_id, middle_id, bottom_id):
    if (Sandwich.objects.get(id=sandwich_id).user_id == request.user.id):
        (top_string, middle_string, bottom_string) = random_slices()
        sandwich_top = Photo.objects.get(id=top_id).top
        sandwich_middle = Photo.objects.get(id=middle_id).middle
        sandwich_bottom = Photo.objects.get(id=bottom_id).bottom
        return render(request, 'sandwich/workshop.html', {
            'top_string': top_string, 
            'middle_string': middle_string, 
            'bottom_string': bottom_string, 
            'top': sandwich_top, 
            'middle': sandwich_middle, 
            'bottom': sandwich_bottom, 
            'sandwich_id': sandwich_id, 
            'top_id': top_id, 
            'middle_id': middle_id, 
            'bottom_id': bottom_id
        })
    else:
        raise PermissionDenied

@login_required
def sandwich_create(request, top_id, middle_id, bottom_id):
    sandwich = Sandwich.objects.create(
        top_id=top_id,
        middle_id=middle_id,
        bottom_id=bottom_id,
        user=request.user,
    )
    sandwich.save()
    return redirect('/sandwiches/')


def sandwich_delete(request, sandwich_id):
    Sandwich.objects.filter(id=sandwich_id).delete()
    return redirect('/sandwiches')


def sandwich_detail(request, sandwich_id):
    # get sandwich
    sandwich = Sandwich.objects.get(id=sandwich_id)
    print(f'/sandwiches/{sandwich_id}')
    if (sandwich):
        top_id = sandwich.top_id
        middle_id = sandwich.middle_id
        bottom_id = sandwich.bottom_id
        print("sandwich in detail is", sandwich.id)
        user_id = sandwich.user_id
        return render(request, 'sandwich/detail.html', {
            'sandwich': sandwich, 
            'sandwich_id': sandwich_id, 
            'top_id': top_id, 
            'middle_id': middle_id, 
            'bottom_id': bottom_id, 
            'user_id': user_id
        })
    else:
        return redirect('/sandwiches/')


@login_required
def sandwich_update(request, sandwich_id, top_id, middle_id, bottom_id):
    sandwich = Sandwich.objects.get(id=sandwich_id)
    sandwich.top_id = top_id
    sandwich.middle_id = middle_id
    sandwich.bottom_id = bottom_id
    sandwich.save()
    return redirect(f'/sandwiches/{sandwich_id}')


def user_profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    print("profile_user.id is", profile_user.id)
    try:
        profile_data = Profile.objects.get(user_id=profile_user.id)
        profile_user.bio = profile_data.bio
        profile_user.img_src = profile_data.img_src
    except:
        pass
    photos = Photo.objects.filter(user_id=user_id)
    sandwiches = Sandwich.objects.filter(user_id=user_id)
    user = User.objects.get(id=user_id)
    return render(request, 'user/profile.html', {
        'profile_user': profile_user, 
        'photos': photos, 
        'sandwiches': sandwiches, 
        'user': user
    })


@login_required
def user_profile_edit(request, user_id):
    if request.user.id == user_id:
        profile_user = User.objects.get(id=user_id)
        try:
            profile_data = Profile.objects.get(user_id=profile_user.id)
            profile_user.bio = profile_data.bio
            profile_user.img_src = profile_data.img_src
        except:
            pass

        return render(request, 'user/profile_edit.html', {'profile_user': profile_user})
    else:
        raise PermissionDenied


@login_required
def user_profile_update(request, user_id):
    if request.user.id == user_id:
        profile_user = User.objects.get(id=user_id)
        profile_user.email = request.POST['email']
        profile_user.save()

        profile_data = None

        try:
            profile_data = Profile.objects.get(user_id=profile_user.id)

        except:
            profile_data = Profile()
            profile_data.user_id = profile_user.id

        profile_data.bio = request.POST['bio']
        profile_data.img_src = request.POST['img-src']
        profile_data.save()

        return redirect(f'/users/{user_id}')
    else:
        raise PermissionDenied


def user_sandwich_gallery(request, user_id):
    profile_user = User.objects.get(id=user_id)
    gallery_title = profile_user.username + '\'s Sandwich Gallery'
    sandwiches = Sandwich.objects.filter(user_id=user_id)
    return render(request, 'sandwich/gallery.html', {
        'gallery_title': gallery_title, 
        'gallery_type': 'user', 
        'sandwiches': sandwiches
    })


@login_required
def user_photo_gallery(request, user_id):
    if request.user.id == user_id:
        profile_user = User.objects.get(id=user_id)
        photos = Photo.objects.filter(user_id=user_id)
        print("photos in user_photo_gallery", photos)
        return render(request, 'user/photo/gallery.html', {'profile_user': profile_user, 'photos': photos})
    else:
        raise PermissionDenied


@login_required
def user_photo_detail(request, user_id, photo_id):
    if request.user.id == user_id:
        photo = Photo.objects.get(id=photo_id, user_id=user_id)
        return render(request, 'user/photo/detail.html', {'photo': photo, 'user_id': user_id})
    else:
        raise PermissionDenied


def photo_delete(request, user_id, photo_id):
    Photo.objects.filter(id=photo_id).delete()
    return redirect(f'/users/{user_id}/photos/')

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
