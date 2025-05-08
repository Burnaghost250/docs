from django.db import models
from django.contrib.auth.models import User

class Upload (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    file_choose=models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title    

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.user.username}'s Profile Picture"
