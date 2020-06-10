from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_completed = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title