from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)  
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 
    date_of_birth = models.DateField(blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True) 
    joined_at = models.DateTimeField(default=now)  

    def __str__(self):
        return self.username

class Design(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='designs/')  
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name='likes', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'design')  

    def __str__(self):
        return f"{self.user.username} liked {self.design.title}"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} on {self.design.title}: {self.content[:20]}..."

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('follower', 'followed') 

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class OverlayLog(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied {self.design.title} overlay at {self.applied_at}"
