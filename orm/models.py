from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=34)
    stamina = models.SmallIntegerField()

    class Meta:
        db_table = 'player'


class TileInfo(models.Model):
    loot_spots = models.IntegerField()
    hidden_loot_spots = models.IntegerField()

    class Meta:
        db_table = 'tile_info'
