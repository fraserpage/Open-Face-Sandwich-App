from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index_redirect),

    # gallery views
    path('sandwiches/', views.sandwich_index, name='sandwich_index'),  # good
    path('sandwiches/<int:sandwich_id>/',
         views.sandwich_detail, name='sandwich_detail'),  # good

    # edit templace
    path('sandwiches/new/', views.sandwich_new, name='sandwich_new'),
    path('sandwiches/<int:top_id>/<int:middle_id>/<int:bottom_id>/edit',
         views.sandwich_edit, name="sandwich_edit"),

    # saving a sandwich
    path('sandwiches/<int:top_id>/<int:middle_id>/<int:bottom_id>/create/',
         views.sandwich_create, name="sandwich_create"),

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
    path('users/<int:user_id>/photos/<int:top_id>/<int:middle_id>/<int:bottom_id>/',
         views.user_photo_detail, name='user_photo_detail'),
    path('accounts/signup/', views.signup, name='signup'),
]
