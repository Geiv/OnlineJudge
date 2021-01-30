from django.db import models


class School(models.Model):
    username = models.TextField(unique=True)

    class Meta:
        db_table = "school"
