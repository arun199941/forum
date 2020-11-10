from django.urls import path,include
from . import views

urlpatterns = [
    path('profile', views.user_profile, name="profile"),
    path("update-profile", views.user_profile_update,name="update-profile")
   

]