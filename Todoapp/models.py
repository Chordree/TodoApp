from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # check the diff btw auto_now and auto_now_add default vals

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['completed']
        # try using the reverse of this to order fetching pics in marketweb by id


# try understanding what all the defalut parameter values in the Task Model do
