from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def chat(request, pk):
    user_model = get_user_model()
    user = user_model.objects.get(pk=pk)
    current_user = request.user

    chat = Chat.objects.filter(
        Q(initiator=user, receiver=current_user) | Q(initiator=current_user, receiver=user)
    ).first()

    if not chat:
        chat = []

    messages = []

    try:
        messages = Message.objects.filter(chat=chat)
    except:
        pass

    context = {
        'messages': messages,
        'user_id': pk,
        'user': user,
    }

    return render(request, 'chats/chat.html', context)



@login_required
def viewChat(request):
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
