from django.urls import path
from .views import index,Inbox,Directs,NewConversation,SendDirect,UserSearch

urlpatterns = [
    path('index/',index),
    path('', Inbox, name='inbox'),
   	path('directs/<username>', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<username>', NewConversation, name='newconversation'),
   	path('send/', SendDirect, name='send_direct'),
]