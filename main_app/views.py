import re
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from datetime import date
from .models import *
import uuid
import boto3
import datetime
from PIL import Image
import io

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
        return JsonResponse({'url':reverse('photo_detail',kwargs={'id':photo.id})})

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