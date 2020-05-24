from django.db import models

# Create your models here.
from user.models import Profile


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    have_attach = models.BooleanField(default=False)

    def __str__(self):
        return '%s, %s, %s' % (self.sender, self.text, self.have_attach)


class Docs(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    def __str__(self):
        return '%s, %s, %s' % (self.owner, self.name, self.path)