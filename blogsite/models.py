from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    content = RichTextField()  # Allows rich text formatting
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="blogsite/images/")

    def delete(self, *args, **kwargs):
        # Check if the image file exists and delete it from the filesystem
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        # Call the parent class delete method to remove the model instance
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return f"/post/{self.id}/"
    
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_img/')
    bio = models.CharField(max_length=200 ,blank=False, null=False, default='I am a user at this amazing website')

    def __str__(self):
        return f"{self.user.username} profile"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"