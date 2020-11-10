from django.shortcuts import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import auth, User
from .forms import  CreateUserForm, PostForm, CommentForm





# class CreateCommunityView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,"create-community.html")
#     def post(self,request,*args,**kwargs):
#         user = request.user
#         description = request.POST['description']
#         name = request.POST['name']
#         anime = request.POST['anime']
#         communityimage = request.FILES['img']
#         if Community.objects.filter(name=name).exists():
#             messages.error(request,"Community already exists")
#         else:
#             community = Community(name=name, description=description, created_by=user,anime=anime, communityimg=communityimage)
#             community.save()
#             messages.success(request, "Community Created")
#             return redirect("/communitys/"+ name)




def community_detail(request,pk):
    community = get_object_or_404(Community, pk=pk)
    return render(request, 'community_detail.html', {'community': community})



def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)

    return  render(request, 'post_detail.html',{'post': post})


def post_list(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'index.html', {'posts': posts})




def signup(request):
    form =CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup  Sucessfull')
            redirect('signin')
    context = {'form': form }
    return render(request ,'signup.html', context)





def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            redirect('signin')



    return render(request, 'signin.html')


def logout(request):
    """
    logout
    """
    auth.logout(request)

    return redirect('/')










def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.submit_user = request.user
                post.save()
                for community_id  in request.POST.getlist('community'):
                    Community.objects.create(community_id=community_id, post=post)
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
            return render(request, 'post_new.html', {'form': form, 'is_create': True})
    return redirect('signin')





def post_edit(request,pk):
    if request.user.is_authenticated:

        post = get_object_or_404(Post,pk=pk)

        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)

                post.save()
                return redirect('post_detail', pk=post.pk)
            else:
                form = PostForm(instance=post, initial={'communities': post.community.all()})
        return render(request, 'post_edit.html', {'form': form, 'is_create': False})
    return redirect('signin')




def add_comment(request, pk, parent_pk=None):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST or None)

        if request.method == "POST":


            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.parent_id = parent_pk
                comment.save()

                return redirect('post_detail',pk=post.pk)
            else:
                form = CommentForm()
        return render(request,"add_comment.html", {'form': form})
    return redirect('signin')

def vote(request, pk, is_upvote):
    content_obj = Vote.get_object(pk)
    content_obj.toggle_vote(request.user, UserVote.UP_VOTE if is_upvote else UserVote.DOWN_VOTE)
    if isinstance(content_obj,Comment):
        post = content_obj.post
    else:
        post = content_obj

    return redirect('post_detail', pk=post.pk)


