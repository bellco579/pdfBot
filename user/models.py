from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    vk_uid = models.IntegerField()
    linked_users = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return "%s,%s,%s" % (self.first_name, self.last_name, self.vk_uid)
