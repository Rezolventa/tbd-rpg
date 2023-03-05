from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=32)
    stamina = models.SmallIntegerField()

    class Meta:
        db_table = 'player'


class TileTemplate(models.Model):
    class TileTypes(models.TextChoices):
        SWAMP = 'swamp', 'Болото'
        FOREST = 'forest', 'Лес'
        MOUNTAINS = 'mountains', 'Горы'

    type = models.CharField(choices=TileTypes.choices, null=True, max_length=32)
    tier = models.SmallIntegerField()
    loot_spots = models.IntegerField()
    hidden_loot_spots = models.IntegerField()

    class Meta:
        db_table = 'tile_template'


class TileGeo(models.Model):
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    template = models.ForeignKey(TileTemplate, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'tile_geo'
