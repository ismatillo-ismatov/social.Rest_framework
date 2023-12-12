from rest_framework.routers import DefaultRouter
from django.urls import path
from users.views import UserViewSet
from user_profile.views import ProfileViewSet
from posts.views import PostViewSet,StoryViewSet,StoryMessageViewSet
from comments.views import CommentViewSet
from votes.views import VoteViewSet
from friends.views import FriendViewSet
from chat.views import *

router=DefaultRouter()
router.register(r"users",UserViewSet,basename='users')
router.register(r'profiles',ProfileViewSet)
router.register(r'posts',PostViewSet)
router.register(r'story',StoryViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'votes',VoteViewSet)
router.register(r'friends',FriendViewSet,basename="friends")
router.register(r'Messages',MessageViewSet,basename="messages")
router.register(r'story-message',StoryMessageViewSet)
urlpatterns=router.urls




