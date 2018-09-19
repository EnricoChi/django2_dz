from django.db import models


class BaseRankModel(models.Model):
    class Meta:
        abstract = True

    is_published = models.BooleanField(
        'Publish', default=False)
    created_date = models.DateTimeField(
        'Create date', auto_now_add=True)
    update_date = models.DateTimeField(
        'Update date', auto_now=True, null=True)
