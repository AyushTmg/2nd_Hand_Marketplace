from django.db import models
from django.conf import settings

class  Category(models.Model):
    titile=models.CharField(max_length=150,unique=True)

    def __str__(self) -> str:
        return self.titile
    
class Item(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='item')
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='item')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    price=models.PositiveIntegerField()
    is_available=models.BooleanField(default=True)
    condition_choices={
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('decent', 'Decent'),
    }
    negotiation_choices={
        ('yes','Yes'),
        ('no','No')
    }
    condition=models.CharField(max_length=20, choices=condition_choices)
    is_negotiable=models.CharField(max_length=20, choices=negotiation_choices)


    def __str__(self):
        return self.title
    
class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f"Image for {self.item.title}"
    

    
