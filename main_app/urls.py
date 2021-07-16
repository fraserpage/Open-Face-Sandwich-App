from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index_redirect),

    # photos
    path('photo/new/', views.photo_new, name='photo_new'),
    path('photo/save/', views.photo_save, name='photo_save'),
    path('photo/<int:id>/', views.photo_detail, name='photo_detail'),

    # gallery views
    path('sandwiches/', views.sandwich_index, name='sandwich_index'),
    path('sandwiches/<int:sandwich_id>/',
         views.sandwich_detail, name='sandwich_detail'),

    # sandwich workshop views
    path('sandwiches/new/', views.sandwich_new, name='sandwich_new'),
    path('sandwiches/new/<int:photo_id>', views.sandwich_from_photo, name='sandwich_from_photo'),
    path('sandwiches/<int:sandwich_id>/edit', views.sandwich_edit, name="sandwich_edit"),
    path('sandwiches/<int:sandwich_id>/new_from', views.sandwich_new_from, name="sandwich_new_from"),

    # saving a sandwich
    path('sandwiches/<int:top_id>/<int:middle_id>/<int:bottom_id>/create/',
         views.sandwich_create, name="sandwich_create"),

    # updating a sandwich
    path('sandwiches/<int:sandwich_id>/<int:top_id>/<int:middle_id>/<int:bottom_id>/update/',
         views.sandwich_update, name="sandwich_update"),

    # delete a sandwich
    path('sandwiches/<int:sandwich_id>/delete', views.sandwich_delete),


    # user paths
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('users/<int:user_id>/edit/',
         views.user_profile_edit, name='user_profile_edit'),
    path('users/<int:user_id>/update/',
         views.user_profile_update, name='user_profile_update'),
    path('users/<int:user_id>/sandwiches/',
         views.user_sandwich_gallery, name='user_sandwich_gallery'),
    path('users/<int:user_id>/photos/',
         views.user_photo_gallery, name='user_photo_gallery'),
    path('users/<int:user_id>/photos/<int:photo_id>/',
         views.user_photo_detail, name='user_photo_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('sandwiches/<int:sandwich_id>/profile_photo/', views.set_profile_photo),

    # delete a photo
    path('users/<int:user_id>/photos/<int:photo_id>/delete', views.photo_delete),
]
