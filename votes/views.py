from crypt import methods
from venv import create

from allauth.headless.base.views import APIView
# from django.contrib.admin import action
# from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from posts.models import Post
from votes.permissions import VoteReadOnly
from django.shortcuts import get_object_or_404,render
from rest_framework import serializers,status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Like
from .serializers import LikeSerializer

# class LikeAPIView(APIView):
#     def post(self,request,*args,**kwargs):
#         post_id = request.data.get('post')
#         if not post_id:
#             return Response({'post': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
#         post = get_object_or_404(Post,id=post_id)
#         like, created = Like.objects.get_or_create(post=post,user=request.user)
#
#         if create:
#             serializer = LikeSerializer(like)
#             return  Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response ({'detail':'Already liked'},status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,*args,**kwargs):
#         like_id = kwargs.get('pk')
#         like = get_object_or_404(Like,like_id,user=request.user)
#         like.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,VoteReadOnly]

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post,pk=self.request.data["post"])
        already_liked = Like.objects.filter(post=post_instance,user=self.request.user).exists()
        # liked_value = self.request.data.get('liked')

        if already_liked:
            raise serializers.ValidationError({"message": "You have already liked this post."})
        serializer.save(user=self.request.user,post=post_instance)

    def destroy(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")
        post_instance = get_object_or_404(Post,pk=post_id)
        like_instance = Like.objects.filter(post=post_instance,user=self.request.user).first()

        if like_instance:
            like_instance.delete()
            return  Response({"message":"Like removed successfully."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"no like found for this post"},status=status.HTTP_404_NOT_FOUND)



        # post_instance = get_object_or_404(Post,pk=kwargs.get("pk"))
        # like_instance = Like.objects.filter(post=post_instance,user=self.request.user).first()
        #
        # if like_instance:
        #     like_instance.delete()
        #     return Response({"message": "Like removed successfully."},status=status.HTTP_204_NO_CONTENT)
        # else:
        #     return Response({"message": "No like found for this post."},status=status.HTTP_404_NOT_FOUND)




        # else:
        #     like_instance = Like.objects.filter(post=post_instance,user=self.request.user).first()
        #     if like_instance is None:
        #         raise serializers.ValidationError({"message": "No Like found for this post."})
        #     like_instance.delete()

        # if self.request.data['post']:
        #     already_liked = Like.objects.filter(post=post_instance,user=self.request.user).exists()
        #     if already_liked:
        #         raise serializers.ValidationError({"message":"you have already liked this post"})
        #     else:
        #         serializer.save(user=self.request.user,post=post_instance)



    # @action(detail=False, methods=['delete'], url_path='unlike/(?P<post_id>[^/.]+)')
    # def unlike(self,reqeust,post_id=None):
    #     try:
    #         like_instance = Like.objects.get(post_id=post_id,user=reqeust.user)
    #         like_instance.delete()
    #         return Response({"detail":"Like removed successfully."},status=status.HTTP_204_NO_CONTENT)
    #     except Like.DoesNotExists:
    #         return Response({"detail": "No Like matches the given query."},status=status.HTTP_404_NOT_FOUND)
