from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'client'
