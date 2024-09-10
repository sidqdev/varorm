from django.db import models


class DBStorage(models.Model):
    key = models.CharField(max_length=255)
    hkey = models.CharField(max_length=255)
    value = models.TextField(null=True)

    class Meta:
        unique_together = ('key', 'hkey')
        db_table = 'varorm_db_storage'
