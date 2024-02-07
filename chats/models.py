from django.db import models
from django.conf import settings

# ! Model For Chat
class Chat(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="initiator"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="receiver"
    )
    start_time = models.DateTimeField(auto_now_add=True)




# ! Model for sending message in a Chat
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender'
    )
    attachment = models.FileField(null=True,blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='chat')

    def __str__(self):
        return f'{self.sender.username}'
