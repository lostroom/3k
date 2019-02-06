from django.db import models
from django.utils import timezone


class Worker(models.Model):
    tabnum = models.IntegerField(primary_key=True)
    fio = models.CharField(max_length=50)
    gender = models.TextField()
    birthdate  = models.TextField()
    photo_id  = models.TextField(null=True)

    def __str__(self):
        return self.fio

class Call(models.Model):
    call_from = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="call_from")
    call_to = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="call_to")
    call_duration = models.IntegerField()
    call_time = models.TimeField()
    call_date = models.DateField()

    def __str__(self):
        return str(self.call_from) + '_to_' + str(self.call_to) + '|' + str(self.call_date) + ':' + str(self.call_time)
