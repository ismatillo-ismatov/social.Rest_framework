from datetime import timezone
from tokenize import Triple
from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_profile.serializer import ProfileSerializer
from user_profile.models import UserProfile
from .models import FriendsRequest
from .serializers import FriendRequestSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from users.serializer import UserSerializer
from django.http import Http404,request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse


class FriendViewSet(viewsets.ViewSet):
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False,methods=['get'])
    def check_status(self,request):
        sender = self.request.user.profile
        username = request.query_params.get('username',None)
        if not username:
            return Response({"error":"Username required"},status=400)
        try:
            receiver = UserProfile.objects.get(userName__username=username)
        except UserProfile.DoesNotExist:
            return Response({"error":"User not found"},status=404)
        try:
            outgoing_request = FriendsRequest.objects.filter(
                request_from=sender,
                request_to=receiver
            ).first()
            incoming_request = FriendsRequest.objects.filter(
                request_from=receiver,
                request_to=sender
            ).first()
            if outgoing_request:
                return  Response({
                    "status": outgoing_request.status,
                    "direction":"outgoing",
                    'request_id':outgoing_request.id,
                    })
            elif incoming_request:
                return Response({
                    "status": incoming_request.status,
                    "direction":"incoming",
                    "request_id":incoming_request.id
                })
            else:
                return Response({
                    "status":"none",
                    "direction":"none"
                })

        except FriendsRequest.DoesNotExist:
            return Response({"status":"none"})


    @action(detail=False,methods=['post'],url_path='update-online-status')
    def update_online_status(self,request):
        user_profile = request.user.profile
        is_online = request.data.get('is_online',False)
        user_profile.is_online = is_online
        if not is_online:
            user_profile.last_activity = timezone.now()
        user_profile.save()
        return Response({
            'status':'success',
            'is_online':user_profile.is_online,
            'last_activity':user_profile.last_activity
        })


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

    @action(detail=False,methods=['GET'])
    def incoming_pending_requests(self,request):
        if not request.user.is_authenticated:
            return Response({"error":"Authentication required"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_profile = request.user.profile
        except AttributeError:
            return Response({"error":"User profile not found"},status=status.HTTP_400_BAD_REQUEST)
        print(f"Foydalanuvchi profili: {user_profile.id}")
        pending_request = FriendsRequest.objects.filter(
            request_to=user_profile,
            status="Pending"
        )
        print(f"Pending sorovlar: {pending_request}")
        if pending_request.exists():
            request_from_users = [request.request_from.id for request in pending_request]
            pending = UserProfile.objects.filter(id__in=request_from_users)
            serializer = ProfileSerializer(pending,many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"You have no pending requests"})

    @action(detail=False, methods=['GET'])
    def outgoing_pending_requests(self, request):
        user_profile = request.user.profile
        print(f"Foydalanuvchi profili: {user_profile.id}")
        pending_request = FriendsRequest.objects.filter(
            request_from=user_profile,
            status="Pending"
        )
        print(f"Pending sorovlar: {pending_request}")
        if pending_request.exists():
            request_from_users = [request.request_to.id for request in pending_request]
            pending = UserProfile.objects.filter(id__in=request_from_users)

            serializer = ProfileSerializer(pending, many=True,context={'request':request})
            serializer = ProfileSerializer(pending, many=True)

            return Response(serializer.data)
        else:
            return Response({"message": "You have no pending requests"})

    def get_object(self,):
        try:
            pk = self.kwargs.get('pk')
            if pk is None:
                raise Http404("Primary key (pk) is required.")
            user_profile = UserProfile.objects.get(userName=self.request.user)
            friend = FriendsRequest.objects.filter(request_from=user_profile, request_to_id=pk)
            if self.request.method == "GET":
                if friend.exists():
                    friend_id = friend.values()[0]["request_to_id"]
                    return UserProfile.objects.get(pk=friend_id)
                else:
                    raise Http404("Friend request not found.")
            elif self.request.method == ['PUT', 'DELETE']:
                if friend.exists():
                    return friend.first()
                else:
                    raise Http404("friend request not found")
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile not found")

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

        active_requests = FriendsRequest.objects.filter(
            (Q(request_from=request.user.profile, request_to=request_to_profile) |
            Q(request_from=request_to_profile, request_to=request.user.profile)) &
            (Q(status='Pending') | Q(status='Accepted'))
        ).exists()
        if active_requests:
            return  Response({"error":"Friend request already exists or has already been send by the other user"},
                             status=status.HTTP_400_BAD_REQUEST
                             )

        rejected_request = FriendsRequest.objects.filter(
            request_from=request.user.profile,
            request_to=request_to_profile,
            status='Rejected'
        ).first()

        if rejected_request:
            rejected_request.status = 'Pending'
            rejected_request.save()
            serializer = FriendRequestSerializer(rejected_request)
            return Response(serializer.data,status=status.HTTP_200_OK)






        friend_request = FriendsRequest.objects.create(
            request_from=request.user.profile,
            request_to=request_to_profile,
            status='Pending'
        )
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def retrieve(self, request,*args,**kwargs):
        try:
            username = kwargs.get('username')
            if not username:
                return  Response({"error":"Username is required."},status=status.HTTP_400_BAD_REQUEST);
            user_profile = request.user.profile
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
        try:
            friend_request = FriendsRequest.objects.get(id=pk)
            serializer = FriendRequestSerializer(friend_request,data=request.data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        except FriendsRequest.DoesNotExist:
            return Response({"error":"Friend request not found"},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        try:
            current_user_profile = request.user.profile
            friend_request = FriendsRequest.objects.get(
                request_from_id=current_user_profile,
                request_to_id=pk,
                status="Pending"
            )

            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except FriendsRequest.DoesNotExist:
            return Response({"error":"Friend request not found or already processed"},
            status=status.HTTP_404_NOT_FOUND
                            )

    @action(detail=False, methods=["GET"])
    def friend_list(self, request):
        try:
            current_user = request.user
            friends_from = FriendsRequest.objects.filter(
                request_from=current_user,
                status="Accepted"
            ).select_related('request_to')

            friends_to = FriendsRequest.objects.filter(
                request_from=current_user,
                status="Accepted"
            ).select_related('request_from')

            friends = []
            for friend_request in friends_from:
                friends.append(friend_request.request_to)

            for friends_request in friends_to:
                friends.append(friends_request.friends_from)

            serializer = ProfileSerializer(friends,many=True)
            return Response({
                "count":len(friends),
                'results': serializer.data
            })
        except Exception as e:
            return Response(
                {"error":str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @action(detail=True,methods=['GET'])
    def user_friends(self,request,pk=None):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 10)
            target_user_profile = UserProfile.objects.get(id=pk)
            friends_from = FriendsRequest.objects.filter(
                request_from=target_user_profile,
                status="Accepted"
            ).select_related('request_to')

            friends_to = FriendsRequest.objects.filter(
                request_to=target_user_profile,
                status='Accepted',
            ).select_related("request_from")
            friends=[]
            for friends_request in friends_from:
                friends.append(friends_request.request_to)

            for friends_request in friends_to:
                friends.append(friends_request.request_from)

            unique_friends = list({friend.id: friend for friend in friends}.values())
            paginator = Paginator(unique_friends, page_size)
            page_obj = paginator.get_page(page)
            serializer = ProfileSerializer(page_obj, many=True)
            return Response({
                "count": paginator.count,
                "next": page_obj.has_next(),
                "previous": page_obj.has_previous(),
                "results": serializer.data
            })

            serializer = ProfileSerializer(unique_friends,many=True)
            return Response({
                "count": len(unique_friends),
                "results": serializer.data,
            })
        except UserProfile.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)



    @action(detail=False,methods=["GET"],url_path='find-friends')
    def find_friends(self,request):
        user_profile = request.user.profile
        accepted_requests = FriendsRequest.objects.filter(
            Q(request_from=user_profile, status="Accepted") |
            Q(request_to=user_profile, status="Accepted")
        )
        friend_ids = list(accepted_requests.values_list('request_to_id',flat=True)) + \
                     list(accepted_requests.values_list("request_from_id",flat=True))
        friend_ids = list(set(friend_ids))
        friend_ids.append(user_profile.id)

        pending_requests = FriendsRequest.objects.filter(
            Q(request_from=user_profile,status="Pending") |
            Q(request_to=user_profile,status="Pending")
        )
        pending_ids = list(pending_requests.values_list('request_to_id',flat=True)) + \
                      list(pending_requests.values_list('request_from_id',flat=True))
        exclude_ids = list(set(friend_ids + pending_ids))

        non_friends = UserProfile.objects.exclude(id__in=exclude_ids)
        username = request.query_params.get('username',None)
        if username:
            non_friends = non_friends.filter(userName__username__icontains=username)
        if not non_friends.exists():
            return  Response({"message":"No user found"},status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(non_friends,many=True,context={'request':request})
        return Response(serializer.data)


    @action(detail=False, methods=['GET'])
    def incoming_requests(self, request):
        user_profile = request.user.profile
        incoming_requests = FriendsRequest.objects.filter(request_to=user_profile, status="Pending")
        if incoming_requests.exists():
            request_from_users = []
            for request in incoming_requests:
                request_from_users.append(request.request_from.id)
            pending = UserProfile.objects.filter(id__in=request_from_users)

            serializer = ProfileSerializer(pending, many=True,context={'request':request})

            serializer = ProfileSerializer(pending, many=True)

            return Response(serializer.data)
        else:
            return Response({"message": "You have no incoming request"})

    @action(detail=True, methods=["put"], name='Accept Friend Request')
    def accept_friend_request(self,request,pk):
        try:

            incoming_request = FriendsRequest.objects.get(
                request_to=self.request.user.profile,
                request_from__id=pk,
                status='Pending'
            )
            incoming_request.status = 'Accepted'
            incoming_request.save()
            return Response({
                "message":"Friend request accepted",
                "request_id": incoming_request.id,
                "status":"Accepted"
            }, status=status.HTTP_200_OK)
        except FriendsRequest.DoesNotExist:
            return Response({"error":"Friend request not found"},status=404)


    @action(detail=True,methods=['put'])
    def reject_friend_request(self,request,pk=None):
        try:
            friend_request = FriendsRequest.objects.get(
                request_from__id=pk,
                request_to=request.user.profile,
                status="Pending"
            )
            friend_request.status = 'Rejected'
            friend_request.save()
            return Response({"status":"success"}, status=status.HTTP_200_OK)
        except FriendsRequest.DoesNotExist:
            return Response(
                {"error": "Friend request not found"},
                status=status.HTTP_404_NOT_FOUND
            )



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

            serializer = ProfileSerializer(pending, many=True,context={'request':request})

            serializer = ProfileSerializer(pending, many=True)

            return Response(serializer.data)
        else:
            return JsonResponse({"message": "no sent  Requests found!"})


    @action(detail=True,methods=['delete'],url_path='delete-friend')
    def delete_friend(self,request,pk=None):
        try:
            user_profile = request.user.profile
            friend_profile = UserProfile.objects.get(id=pk)
            friendship = FriendsRequest.objects.filter(
                (Q(request_from=user_profile, request_to=friend_profile) |
                 Q(request_from=friend_profile,request_to=user_profile) &
                Q(status='Accepted')
                 )
            ).first()

            if not friendship:
                return Response(
                    {"Error":"Friendship not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            friendship.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except UserProfile.DoesNotExist:
            return Response(
                {"error":"User profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


