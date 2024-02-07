from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# ! View Funtion for chatting 
@login_required
def chat(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(pk=pk)
    current_user = request.user
 
    # ! Tries to check if the chat with the given user exists or not 
    chat = Chat.objects.filter(
        Q(initiator=user, receiver=current_user) | Q(initiator=current_user, receiver=user)
    ).first()
    
    # ! If not chat is equals to a empty list
    if not chat:
        chat = []
 
    # ! Initialized message variable as empty list
    messages = []
    
    # ! tries to get the message to with the chat object above
    try:
        messages = Message.objects.filter(chat=chat)
    except:
        pass

    # ! Passes  the arguments to the template 
    context = {
        'messages': messages,
        'user_id': pk,
        'user': user,
    }

    return render(request, 'chats/chat.html', context)



# ! View function for showing a users chat 
@login_required
def viewChat(request):
    """ 
    Method that shows the all chat objects of a user 
    """
    messages = []
    chat = []
    user = request.user

    try:
        chat = Chat.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        )
    except:
        pass

    context = {
        'chats': chat
    }

    return render(request, 'chats/view_chat.html', context)
