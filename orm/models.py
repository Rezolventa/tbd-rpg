from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=34)
    stamina = models.SmallIntegerField()

    class Meta:
        db_table = 'player'
