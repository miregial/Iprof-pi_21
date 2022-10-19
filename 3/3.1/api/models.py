from django.db import models

class Prize(models.Model):
    description = models.TextField()



class Result(models.Model):
    winner = models.ForeignKey('User', related_name='winners', on_delete=models.CASCADE)
    prize = models.ForeignKey('Prize', on_delete=models.CASCADE)

class User(models.Model):
    name = models.CharField(max_length=80)


    
class Promo(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    prizes = models.ManyToManyField('Prize', related_name='promos')
    participants = models.ManyToManyField('User', related_name='promos')