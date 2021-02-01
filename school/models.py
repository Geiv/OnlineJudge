from django.db import models


class School(models.Model):
    school_name = models.TextField(unique=True)

    class Meta:
        db_table = "school"
