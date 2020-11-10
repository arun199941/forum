from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comment,Community


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name' ,'last_name', 'email', 'password1', 'password2']


# Post Form
class PostForm(forms.ModelForm):
    communities = forms.ModelMultipleChoiceField(queryset=Community.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'description','url', 'communities' )


# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


