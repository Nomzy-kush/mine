from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.



class Video(models.Model):
    title= models.TextField()
    summary= models.TextField()
    image= models.ImageField()
    file = models.FileField(blank=True,null=True)
    link = models.CharField(max_length=200,blank=True,null=True)
    user=models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)
    slug = models.SlugField()
    paginate_by = 2

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("App:details", kwargs={
            'slug': self.slug
        })

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    private_key = models.TextField()
    typingdna_secured = models.BooleanField(default=False)
