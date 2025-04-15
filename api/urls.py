from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from zope.interface import named

from friends.models import FriendsRequest
from users.views import UserViewSet, UserSearchAPIView
from user_profile.views import UserProfileView
from posts.views import PostViewSet,StoryViewSet,StoryMessageViewSet
from comments.views import CommentViewSet
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
router.register(r'messages',MessageViewSet,basename="messages")
router.register(r'story-message',StoryMessageViewSet)
urlpatterns=router.urls

urlpatterns = [
    path('my-profile/',UserProfileView.as_view(),name='my-profile'),
    path('search_users/',UserSearchAPIView.as_view(),name='search_users'),
    path('users/<int:pk>/friends/',FriendViewSet.as_view({'get':'user_friends'}),name='user-friends'),
    path('update-online-status/',FriendViewSet.as_view({'post':'update_online_status'}),name='update-online-status'),
    path('friends/incoming-pending-requests/',FriendViewSet.as_view({'get':'incoming_pending_requests'})),
    path('friends/outgoing-pending-request/',FriendViewSet.as_view({'get':'outgoing_pending_requests'})),
    path('friend-detail/<str:username>/',FriendViewSet.as_view({'get':'retrieve'}),name='friend-detail'),
    path('friends/<int:pk>/accept/',FriendViewSet.as_view({'put':'accept_friend_request'}),name='accept_friend_request'),
    path('friends/<int:pk>/reject/',FriendViewSet.as_view({'put':'reject_friend_request'}),name='reject_friend_request'),
    path('friends/<int:pk>/action-delete-request/',FriendViewSet.as_view({'delete':'delete_request'}),name='friend-delete-request'),
    path('friends/<int:pk>/delete-friend/',FriendViewSet.as_view({'delete':'delete_friend'}),name='friend-delete'),
    path('friends/<int:pk>/',FriendViewSet.as_view({'delete':'destroy'}),name='friend-request-detail'),
    # path('find-friends/',FriendViewSet.as_view({'get':'find_friends'}),name='find-friends'),
    path('',include(router.urls)),
]




