from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    vk_uid = models.IntegerField()

    def __str__(self):
        return "%s,%s,%s" % (self.first_name, self.last_name, self.vk_uid)


class Linkes(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owner")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "%s,%s" % (self.owner.last_name, self.receiver.last_name)
