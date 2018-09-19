from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Program(models.Model):
    #program_id = models.AutoField(null=False, primary_key=True)
    program_name = models.CharField(max_length=20, null=False)
    program_start_date = models.DateField(null=False, blank=False)
    program_end_date = models.DateField(null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.program_name)