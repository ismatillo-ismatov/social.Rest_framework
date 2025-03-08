from django.shortcuts import get_object_or_404
from drf_yasg.inspectors.field import serializer_field_to_basic_type
from rest_framework import generics,viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from user_profile.serializer import ProfileSerializer
from user_profile.models import UserProfile
from .models import FriendsRequest
from .serializers import FriendRequestSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from user_profile.permissions import IsOwnerReadOnly
from users.serializer import UserSerializer
from django.http import Http404,request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import  JsonResponse


class FriendViewSet(viewsets.ViewSet):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False,methods=['get'])
    def check_status(self,request):
        sender = request.user.profile
        username = request.query_params.get('username',None)
        if not username:
            return Response({"error":"Username required"},status=400)
        receiver = get_object_or_404(UserProfile,userName=username)
        try:
            friend_request = FriendsRequest.objects.get(request_from=sender,request_to=receiver)
            return  Response({"status": friend_request.status})
        except FriendsRequest.DoesNotExist:
            return Response({"status":"none"})


    def get_queryset(self):
        user_profile = self.request.user.profile
        q1 = FriendsRequest.objects.filter(request_from=user_profile,status="Accepted")
        q2 = FriendsRequest.objects.filter(request_to=user_profile,status="Accepted")
        result = []

        if q1.exists() and not q2.exists():
            for i in range(len(q1.values())):
                result.extend(q1.values_list('request_to_id',flat=True),)

        elif not q1.exists() and q2.exists():
            result.extend(q2.values_list('request_to_id',flat=True),)
        elif q1.exists and q2.exists:
            result.extend(q1.values_list('request_to_id',flat=True),)
            result.extend(q2.values_list('request_from_id',flat=True),)

        else:
            pass
        friends = UserProfile.objects.filter(id__in=result)
        return friends

    def get_object(self, pk):
        try:
            user_profile = UserProfile.objects.get(userName=self.request.user)
            friend = FriendsRequest.objects.filter(request_from=user_profile, request_to_id=pk)
            if self.request.method == "GET":
                if friend.exists():
                    friend_id = friend.values()[0]["request_to_id"]
                    return UserProfile.objects.get(pk=friend_id)
            elif self.request.method == ['PUT', 'DELETE']:
                return friend

        except UserProfile.DoesNotExist:
            return Response({"error":"userProfile not found"},status=status.HTTP_404_NOT_FOUND)
        except FriendsRequest.DoesNotExist:
            return Response ({"error":"FriendRequest not found"},status=status.HTTP_404_NOT_FOUND)



    def list(self, request):
        friends = self.get_queryset()
        serializer = ProfileSerializer(friends,many=True)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        request_to_username = request.data.get('request_to')
        if not request_to_username:
            return Response({"error":"Missing 'request_to' field"},status=status.HTTP_400_BAD_REQUEST)
        try:
            request_to_profile = UserProfile.objects.get(userName__username=request_to_username)
        except  UserProfile.DoesNotExist:
            return Response({"error":"user not found"},status=status.HTTP_404_NOT_FOUND)

        if request.user.profile == request_to_profile:
            return JsonResponse({"error": "You cannot send a friend request to yourself"},status=status.HTTP_400_BAD_REQUEST)








        already_friend = FriendsRequest.objects.filter(
            request_from=request.user.profile,
            request_to=request_to_profile,
            status='Accepted'
        ).exists()

        if already_friend:
            return Response({"error": "Friend request already exists"}, status=status.HTTP_400_BAD_REQUEST)


        if FriendsRequest.objects.filter(
                request_from=request.user.profile,
                request_to=request_to_profile,
                status='Pending'
            ).exists():
            return Response({"error":"Friend request already sent"},status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendsRequest.objects.create(
            request_from=request.user.profile,
            request_to=request_to_profile,
            status='Pending'
        )
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


    def retrieve(self, request, username=None):
        try:
            user_profile = self.request.user.profile
            friend_profile = UserProfile.objects.get(userName__username=username)

            friend_request = FriendsRequest.objects.filter(
                request_from=user_profile,
                request_to=friend_profile,
                status="Accepted"
            ).exists()
            if friend_request:
                serializer = ProfileSerializer(friend_profile)
                return Response(serializer.data)
            else:
                return Response({"error":"There are no friend requests with this user."},status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)




    def update(self, request, pk=None):
        friend = self.get_object(pk)
        serializer = FriendRequestSerializer(friend,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        friend = self.get_object(pk)
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,methods=["GET"])
    def find_friends(self,request):
        user = self.request.user.pk
        q1 = FriendsRequest.objects.filter(request_from__userName=user,status="Accepted")
        q2 = FriendsRequest.objects.filter(request_to__userName=user,status="Accepted")
        result=[user]
        if q1.exists() and not q2.exists():
            for p in range(len(q1.values())):
                result.append(q1.values()[p]['request_to_id'])
        elif not q1.exists() and q2.exists():
            for p in range(len(q2.values())):
                result.append(q2.values()[p]['request_from_id'])
        elif q1.exists() and q2.exists():
            for p in range(len(q1.values())):
                result.append(q1.values()[p]['request_to_id'])
            for p in range(len(q2.values())):
                result.append(q2.values()[p]['request_from_id'])

        username = request.query_params.get('username',None)
        find_friends = UserProfile.objects.exclude(id__in=result)
        if username:
            find_friends = find_friends.filter(userName__username__icontains=username)
            serializer = ProfileSerializer(find_friends,many=True)
            return Response(serializer.data)

        if not find_friends.exists():
            return  Response({"message":"No users found"},status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def incoming_requests(self, request):
        user_profile = request.user.profile
        incoming_requests = FriendsRequest.objects.filter(request_to=user_profile, status="Pending")
        if incoming_requests.exists():
            request_from_users = []
            for request in incoming_requests:
                request_from_users.append(request.request_from.id)
            pending = UserProfile.objects.filter(id__in=request_from_users)
            serializer = ProfileSerializer(pending, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "You have no incoming request"})

    @action(detail=True, methods=["put"], name='Accept Friend Request')
    # @action(detail=False,methods=['GET'])
    # def incoming_requests(self, request):
    #     incoming_requests = FriendsRequest.objects.filter(request_to__userName=self.request.user,status="pending")
    #     if incoming_requests.exists():
    #         request_from_users = []
    #         for i in range(len(incoming_requests.values())):
    #             request_from_users.append(incoming_requests.values()[i]['request_from_id'])
    #         pending = UserProfile.objects.filter(id__in=request_from_users).values()
    #         serializer = UserSerializer(pending,many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response({"message":"You have any incoming request"})
    # @action(detail=True,methods=["put"],name='Accept Friend Request')
    def friendsrequest(self,request,pk):
        print(pk)
        incoming_request = FriendsRequest.objects.filter(request_to=self.request.user,request_from=pk,status='pending').get()
        print(incoming_request)
        serializer = FriendRequestSerializer(incoming_request,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @friendsrequest.mapping.delete
    def delete_request(self,request,pk):
        print(pk)
        try:
            incoming_request = FriendsRequest.objects.filter(request_to=self.request.user,request_from=pk,status='pending')
            print(incoming_request)
            incoming_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def send_request(self, request):
        sender = request.user.profile
        username = request.data.get('username')

        if not username:
            return  Response({"error":"Username is required"},status=400)

        receiver = get_object_or_404(UserProfile,userName=username)

        if FriendsRequest.objects.filter(request_from=sender,request_to=receiver).exists():
            return Response({"error":"Friend request already sent"},status=400)
        friend_request = FriendsRequest.objects.create(request_from=sender,request_to=receiver,status="Pending")
        return Response({"message":"Friends request sent"},status=201)

    @action(detail=False, methods=['GET'])
    def send_requests(self, request):
        user_profile = request.user.profile
        send_requests = FriendsRequest.objects.filter(
            request_from=user_profile,
            status="Pending"
        )
        print(send_requests)
        if send_requests.exists():
            request_to_users = [request.request_to.id for request in send_requests]

            pending = UserProfile.objects.filter(id__in=request_to_users)
            serializer = ProfileSerializer(pending, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"message": "no sent  Requests found!"})

