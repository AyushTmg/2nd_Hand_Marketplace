from django.shortcuts import render
from .models import Message
from django.contrib.auth import get_user_model
from django.db.models import Q



       
def chat(request,pk):
    user_model = get_user_model() 
    user = user_model.objects.get(pk=pk)
    messages=[]
    try:
        messages=Message.objects.filter(sender=request.user,receiver=user)
        
    except:
        pass
    context={
        'user_id':pk,
        'messages':messages
    }
    return render(request,'chats/chat.html',context)    

def viewChat(request):
    messages=[]
    try:
        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        
    except:
        pass
    context={
        'messages':messages
    }
    return render(request,'chats/view_chat.html',context)  

    

