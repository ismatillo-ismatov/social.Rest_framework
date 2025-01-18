from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import UserViewSet, UserSearchAPIView
from user_profile.views import UserProfileView
# from user_profile.views import ProfileViewSet
from posts.views import PostViewSet,StoryViewSet,StoryMessageViewSet
from comments.views import CommentViewSet
# from votes.views import  LikeAPIView
from votes.views import  LikeViewSet
from friends.views import FriendViewSet
from chat.views import *

router=DefaultRouter()
router.register(r"users",UserViewSet,basename='users')
router.register(r'posts',PostViewSet,basename='posts')
router.register(r'story',StoryViewSet)
router.register(r'comments',CommentViewSet,basename="comment")
router.register(r'likes',LikeViewSet,basename="likes")
router.register(r'friends',FriendViewSet,basename="friends")
router.register(r'Messages',MessageViewSet,basename="messages")
router.register(r'story-message',StoryMessageViewSet)
urlpatterns=router.urls

urlpatterns = [
    path('my-profile/',UserProfileView.as_view(),name='my-profile'),
    path('search_users/',UserSearchAPIView.as_view(),name='search_users'),
    path('',include(router.urls)),
]




