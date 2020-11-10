from django.shortcuts import render, redirect
from django.contrib import  messages
from .models import Profile
from .forms import ProfileUpdateForm, UserUpdateForm

# Create your views here.


def user_profile(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            obj = Profile.objects.get(user=request.user)
            context = {
                "country": obj.country,
                'phone': obj.phone,
                'profile_image': obj.profile_image,
                'about': obj.about,

            }
            return render(request, 'profile.html', context)
        

   
    return redirect('signin')

def user_profile_update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            u_form  = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Profile Updated Successfully");
           
          
        else:
            u_form  = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
          
        context = {
            'u_form':  u_form,
            "p_form": p_form,
        }


        return render(request,"update-profile.html",context)

    return redirect("signin")
         
