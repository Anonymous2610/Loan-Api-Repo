# from urllib import request
from urllib import request
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from . import models as api_models
from . import serializers as api_serializers
from rest_framework.views import APIView1
from rest_framework.response import Response
from rest_framework import viewsets
import time
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        user = User.objects.filter(email=request.data.get("email"))
        if user.count() == 0:
            email=request.data.get("email")
            name = request.data.get('first_name') + request.data.get('last_name')
            data = request.data

            email = data.get("email")
            user = User.objects.create( first_name=data.get("first_name"),
                                        last_name=data.get("last_name"),
                                        email=email.lower(),
                                        phone_number=data.get("phone_number"),
                                        user_type=data.get("user_type"),
                                        username=data.get("username"),
                                        address=data.get("address"),
                                        uid=data.get("uid"),
                                        adhar=data.get("adhar"),
                                        pan=data.get("pan"),
                                        )
            if data.get('avatar') is not None:
                user.avatar = data.get('avatar')
            if data.get('user_type') is None:
                user.user_type = 'borrower'
            user.is_active =True
            user.save()
            user.set_password(data.get("password"))
            user.save()
            context = {
                "message": f"{user.first_name} {user.last_name} is successfully registered."}
        else:
            context = {
                "message": "A user with the email already exist!"
            }
        return Response(context)

class GetLoginToken(APIView):
    
    def post(self, request):
        user = User.objects.filter(
            email=request.data.get("email")).first()
        password = request.data.get("password")
        if user is not None and user.check_password(password):
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                context = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(context, status.HTTP_200_OK)
            else:
                context = {
                    "message": "Please verify your email first!"
                }
                return Response(context, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            context = {
                "detail": "No active account found with the given credentials"
            }
            return Response(context, status.HTTP_401_UNAUTHORIZED)

class CreateConversation(generics.CreateAPIView):
    serializer_class = api_serializers.ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AddGroupMembers(APIView):
    def put(self,request,*arg,**kwargs):
        if(request.user.is_authenticated):
            group_id = request.data.get('conversation_id')
            members = request.data.get('members')
            group = api_models.Conversation.objects.get(id=group_id)
            if(group.created_by == request.user):
                for member in members:
                    user = User.objects.get(id=member)
                    group.borrowers.add(user)
            else:
                return Response({'message':'You are not authorized to add members to this group'})         
            group.updated_at = time.timezone.now()
            return Response({'message':'Members added successfully'})
        
        else:
            return Response({'message':'User not authenticated'})


class GetConversations(generics.ListAPIView):
    serializer_class = api_serializers.ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return api_models.Conversation.objects.filter(created_by=self.request.user)

class CreateMessage(APIView):
    def post(self,request,*arg,**kwargs):
        print(request.user)
        if(request.user.is_authenticated):
            print(request.user)
            conversation_id = request.data.get('conversation_id')
            message = request.data.get('message')
            conversation = api_models.Conversation.objects.get(id=conversation_id)
            borrower=api_models.Conversation.objects.filter(borrowers=request.user)
            if(conversation.lenders == request.user or borrower.exists()):
                message = api_models.Message.objects.create(message=message,linked_conversation=conversation,creator=request.user)
                return Response({'message':'Message sent successfully'})
            else:
                return Response({'message':'You are not authorized to send messages to this conversation'})
    
        else:
            return Response({'message':'User not authenticated'})
    

class MessagesOfConversation(generics.ListAPIView):
    serializer_class = api_serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        conversation_id = self.kwargs.get('id')
        # conversation=api_models.Conversation.objects.get(id=conversation_id)
        return api_models.Message.objects.filter(linked_conversation_id=conversation_id).all()


class GetUsers(generics.ListAPIView):
    serializer_class = api_serializers.api_user_serializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        return User.objects.all()

class GetUserById(generics.RetrieveAPIView):
    serializer_class = api_serializers.api_user_serializer
    # permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        return User.objects.get(id=self.kwargs.get('id'))

class UpdateUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=api_serializers.api_user_serializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return User.objects.get(id=self.request.user.id)



class GetMessageView(generics.ListCreateAPIView):
    serializer_class=api_serializers.MessageSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        is_read=self.request.GET.get('is_read','')
        if(self.request.user.is_anonymous):
            return Response({"msg":"No user found"},status.HTTP_404_NOT_FOUND)
        return api_models.Message.objects.filter(creator=self.request.user.id,is_read=is_read).all().order_by('-created_at')


class UpdateMsgView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=api_serializers.MessageSerializer
    permission_classes=[permissions.IsAuthenticated]
    queryset=api_models.Message.objects.all()
    lookup_field='id'

class ChatListView(APIView):
    def get(self,request,*arg,**kwargs):
        user=request.user
        if(user.is_anonymous):
            return Response({'msg':"Invalid User"},status.HTTP_401_UNAUTHORIZED)
        conversations=api_models.Conversation.objects.filter(lenders=user.id).all()
        if conversations is None:
            conversations=api_models.Conversation.objects.filter(borrowers=user.id).all()
        chatlist={}
        for id in conversations:
            msg=api_models.Message.objects.filter(linked_conversation=id.id).order_by("-created_at").first()
            chatlist[id.name]={
                                "Sender":msg.creator.username,
                                "last_msg":msg.message,
                                "created_at":msg.created_at,
                                "read_status":msg.is_read,
                               }
        return Response(chatlist,status.HTTP_200_OK)

    
class ListCallView(generics.ListCreateAPIView):
    serializer_class=api_serializers.CallSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return api_models.Call.objects.filter(created_by=self.request.user).all


class CallDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=api_serializers.CallSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return api_models.Call.objects.filter(created_by=self.request.user).all
    lookup_field='id'
    