from django.db import models

# Create your models here.
from user.models import Profile


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    have_attach = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return '%s, %s, %s' % (self.sender, self.text, self.have_attach)


class Docs(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)

    def __str__(self):
        return '%s, %s, %s' % (self.owner, self.name, self.path)


class Photo(models.Model):
    msg = models.ForeignKey(Message, on_delete=models.CASCADE)
    path = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return '%s, %s' % (self.msg, self.path)
