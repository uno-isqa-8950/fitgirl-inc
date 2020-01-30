from django.db import models


class DefaultModel(models.Model):
    name = models.CharField(max_length=15, unique=True)


class ReplacementModel(models.Model):
    name = models.CharField(max_length=15, unique=True)
