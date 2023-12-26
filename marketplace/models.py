from django.db import models

class  Category(models.Model):
    titile=models.CharField(max_length=150,unique=True)

    def __str__(self) -> str:
        return self.titile
    
class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    condition_choices={
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('decent', 'Decent'),
    }
    location=models.CharField(max_length=100)
    condition=models.CharField(max_length=20, choices=condition_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f"Image for {self.item.title}"
    

    
