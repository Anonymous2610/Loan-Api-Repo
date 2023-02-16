from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('create/', views.CreateConversation.as_view(), name='create_conversation'),
    path('register/',views.UserViewset.as_view({'create':'list'}),name='user_register'),
    path('get-token/',views.GetLoginToken.as_view(),name='get_token'),
    path('create-conversation/',views.CreateConversation.as_view(),name='create_conversation'),
    path('user-list/',views.GetUsers.as_view(),name='user_list'),
    path('user-list/<int:id>/',views.GetUserById.as_view(),name='user'),
    path('update-profile/',views.UpdateUser.as_view(),name='update_profile'),
    path('add-members/', views.AddGroupMembers.as_view(), name='add_group_members'),
    path('get-conversations/', views.GetConversations.as_view(), name='get_conversations'),
    path('create-message/', views.CreateMessage.as_view(), name='create_message'),
    path('msg/',views.GetMessageView.as_view(),name="get_and_create_messages"),
    path('update-msg/<int:id>/',views.UpdateMsgView.as_view(),name='update-msg'),
    path('conversations/<int:id>/', views.MessagesOfConversation.as_view(), name='conversation_mesages'),
    path("chatlist/",views.ChatListView.as_view(),name="Chat_list"),
    path("call-detail/<int:id>/",views.CallDetailView.as_view(),name="call_detail"),
    path("call-list/",views.ListCallView.as_view(),name="call_list")
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)