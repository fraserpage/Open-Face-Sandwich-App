from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import *
import uuid
import boto3
from PIL import Image
import io
import urllib.request


# Static pages
# -------------
def index(request):
    martin = User.objects.get(id=1)
    kir = User.objects.get(id=2)
    david = User.objects.get(id=3)
    fraser = User.objects.get(id=4)
    featured1 = Sandwich.objects.get(id=5)
    featured2 = Sandwich.objects.get(id=20)
    featured3 = Sandwich.objects.get(id=37)
    featured4 = Sandwich.objects.get(id=3)
    return render(request, 'index.html', {
        'martin': martin, 
        'kir': kir, 
        'david': david, 
        'fraser': fraser, 
        'featured1': featured1,
        'featured2': featured2,
        'featured3': featured3,
        'featured4': featured4,
        })

def index_redirect(request):
    return redirect('/')
# Amazon S3 settings
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'open-face-sandwich'

# photo crop lines
crop__mid = 0.4  # top of mid block
crop_low = 0.68  # bottom of mid block


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

        top_img = crop_image(pil_image, (0, 0, width, height * crop__mid))
        top_url = save_to_s3(top_img, image_file)

        middle_img = crop_image(
            pil_image, (0, height * crop__mid, width, height * crop_low))
        middle_url = save_to_s3(middle_img, image_file)

        bottom_img = crop_image(
            pil_image, (0, height * crop_low, width, height))
        bottom_url = save_to_s3(bottom_img, image_file)

        photo = Photo(
            top=top_url,
            middle=middle_url,
            bottom=bottom_url,
            is_public=True,
            user=request.user)
        photo.save()
        return JsonResponse({'url': reverse('sandwich_from_photo', kwargs={'photo_id': photo.id})})
    else:
        # Something went wrong
        return JsonResponse({
            'url': reverse('photo_new'),
            'error': 'There was an error saving the photo'
        })

# photo saving helper functions


def save_to_s3(image_file, orig_img):
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + orig_img.name[orig_img.name.rfind('.'):]
    s3.upload_fileobj(image_file, BUCKET, key)
    return f"{S3_BASE_URL}{BUCKET}/{key}"


def save_file_to_memory(new_img):
    in_mem_file = io.BytesIO()
    new_img.save(in_mem_file, format="JPEG")
    in_mem_file.seek(0)
    return in_mem_file


def crop_image(image, crop):
    cropped_img = image.crop(crop)
    if cropped_img.mode != 'RGB':
        cropped_img = cropped_img.convert('RGB')

    return save_file_to_memory(cropped_img)


def photo_detail(request, id):
    photo = Photo.objects.get(id=id)
    return render(request, 'photo/detail.html', {'photo': photo})


# Sandwich pages
# -------------

def sandwich_index(request):
    # get all sandwiches
    # sandwiches = Sandwich.objects.filter(is_public=True)
    sandwiches = Sandwich.objects.all()
    return render(request, 'sandwich/gallery.html', {'sandwiches': sandwiches, 'gallery_title': 'Sandwich Gallery', 'gallery_type': 'public'})

# Helper function to get all photos
def photos_for_workshop(request):
    return Photo.objects.filter(Q(user_id=request.user.id) | Q(is_public=True))


def sandwich_new(request):
    photos = photos_for_workshop(request)
    return render(request, 'sandwich/workshop.html', { 'photos':photos })


def sandwich_from_photo(request, photo_id):
    photos = photos_for_workshop(request)
    photo = Photo.objects.get(id=photo_id)
    return render(request, 'sandwich/workshop.html', {
        'photos':photos,
        'from_photo': photo
    })


def sandwich_edit(request, sandwich_id):
    sandwich = Sandwich.objects.get(id=sandwich_id)
    if (sandwich.user_id == request.user.id):
        photos = photos_for_workshop(request)
        return render(request, 'sandwich/workshop.html', {
            'photos':photos,
            'edit_sandwich':sandwich
        })
    else:
        raise PermissionDenied


def sandwich_new_from(request, sandwich_id):
    sandwich = Sandwich.objects.get(id=sandwich_id)
    photos = photos_for_workshop(request)
    return render(request, 'sandwich/workshop.html', {
        'photos':photos,
        'from_sandwich':sandwich
    })


# Build thumbnail image from slices
def get_concat_v(im1, im2, im3):
    dst = Image.new('RGB', (im1.width,
                    im1.height + im2.height + im3.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    dst.paste(im3, (0, im1.height + im2.height))
    return dst


def save_sandwich_thumbnail(sandwich_id):
    print("in save sandwich thumbnail")
    sandwich = Sandwich.objects.get(id=sandwich_id)
    urllib.request.urlretrieve(sandwich.top.top, "top.jpg")
    top = Image.open("top.jpg")
    urllib.request.urlretrieve(sandwich.middle.middle, "middle.jpg")
    middle = Image.open("middle.jpg")
    urllib.request.urlretrieve(sandwich.bottom.bottom, "bottom.jpg")
    bottom = Image.open("bottom.jpg")
    sandwich_thumbnail = get_concat_v(top, middle, bottom)
    sandwich_thumbnail = save_file_to_memory(sandwich_thumbnail)
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + str(sandwich_id) + ".jpg"
    # print("key in save_sandwich_thumbnail", key)
    try:
        s3.upload_fileobj(sandwich_thumbnail, BUCKET, key)
        url = f'{S3_BASE_URL}{BUCKET}/{key}'
        print('url',url)
        return url
    except:
        print('An error occurred uploading file to S3')
        return ""


@login_required
def sandwich_create(request, top_id, middle_id, bottom_id):
    sandwich = Sandwich.objects.create(
        top_id=top_id,
        middle_id=middle_id,
        bottom_id=bottom_id,
        user=request.user,
    )
    sandwich.thumbnail = save_sandwich_thumbnail(sandwich.id)
    sandwich.save()
    return redirect(f'/sandwiches/{sandwich.id}')


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
    sandwich.thumbnail = save_sandwich_thumbnail(sandwich_id)
    sandwich.save()
    return redirect(f'/sandwiches/{sandwich_id}')


# User profiles
# --------------

def user_profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    photos = Photo.objects.filter(user_id=user_id)
    sandwiches = Sandwich.objects.filter(user_id=user_id)
    return render(request, 'user/profile.html', {
        'profile_user': profile_user,
        'photos': photos,
        'sandwiches': sandwiches,
        'profile_user': profile_user
    })


@login_required
def set_profile_photo(request, sandwich_id):
    # print("user set profile photo worked")
    sandwich = Sandwich.objects.get(id=sandwich_id)
    try:
        profile_data = Profile.objects.get(user_id=request.user.id)

    except:
        profile_data = Profile()
        profile_data.user_id = request.user.id

    profile_data.img_src = sandwich.thumbnail
    # print("user set profile data after setting img", profile_data.img_src)
    profile_data.save()
    return redirect(f'/users/{request.user.id}/')
    
    
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
    sandwiches = Sandwich.objects.filter(user_id=user_id)
    return render(request, 'sandwich/gallery.html', {
        'gallery_type': 'user',
        'profile_user': profile_user,
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
            if "next" in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
