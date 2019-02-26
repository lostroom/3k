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

class Letter(models.Model):
    letter_from = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="letter_from")
    letter_to = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="letter_to")
    letter_theme = models.TextField()
    letter_message = models.TextField()
    letter_dict = models.TextField(null=True)
    letter_time = models.TimeField()
    letter_date = models.DateField()

    def __str__(self):
        return str(self.letter_from) + '_to_' + str(self.letter_to) + '|' + str(self.letter_date) + ':' + str(self.letter_time)

class Meet(models.Model):
    meet_key = models.IntegerField()
    meet_participant = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="meet_participant")
    meet_theme = models.TextField()
    meet_subject = models.TextField()
    meet_time = models.TimeField()
    meet_date = models.DateField()

    def __str__(self):
        return str(self.meet_key) + '|' + str(self.meet_date) + ':' + str(self.meet_time)

class Stat(models.Model):
    synt_id = models.CharField(max_length=50)
    first_tabnum = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="first_tabnum")
    second_tabnum = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="second_tabnum")
    stat_letters = models.IntegerField()
    stat_calls = models.IntegerField()
    stat_meets = models.IntegerField()
    stat_result = models.IntegerField()

    def __str__(self):
        return str(self.synt_id) + '|' + str(self.first_tabnum) + '<--->' + str(self.second_tabnum)
