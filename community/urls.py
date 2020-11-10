from django.urls import path

from . import views
# from tribes.views import CreateCommunityView


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path('post/<uuid:pk>/', views.post_detail, name='post_detail'),
    path('post/create-new/', views.post_new, name='post_new'),
    path('post/<uuid:pk>/edit/', views.post_edit, name='post_edit'),
    # path("create-a-comunity", CreateCommunityView.as_view(), name="create-a-community"),
    path("community/<uuid:pk>", views.community_detail , name="community_detail"),
    path('post/<uuid:pk>/comment', views.add_comment, name="add_comment"),
    path('post/<uuid:pk>/comment/<uuid:parent_pk>/', views.add_comment, name="add_reply_to_comment"),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('signin', views.signin, name='signin'),
    path('content/<uuid:pk>/upvote/', views.vote, {'is_upvote': True}, name="upvote"),
    path('content/<uuid:pk>/downvote/', views.vote, {'is_upvote': False}, name="downvote")
    



]
