from rest_framework.routers import DefaultRouter
from django.urls import path
from users.views import UserViewSet
from user_profile.views import ProfileViewSet
from posts.views import PostViewSet
from comments.views import CommentViewSet
from votes.views import VoteViewSet
from friends.views import FriendViewSet
from chat.views import *

router=DefaultRouter()
router.register(r"users",UserViewSet,basename='users')
router.register(r'profiles',ProfileViewSet)
router.register(r'posts',PostViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'votes',VoteViewSet)
router.register(r'friends',FriendViewSet,basename="friends")
router.register(r'Messages',MessageViewSet,basename="messages")
urlpatterns=router.urls

# urlpatterns = [
#     path('api/messages/<int:sender>/<int:receiver',message_list,name="message-detail"),
#     path('api/messages/',message_list,name='message-list'),
#     path("api/users/<int:pk>",user_list,name="user-detail"),
#     path("api/users/",user_list,name='user-list')
# ]


