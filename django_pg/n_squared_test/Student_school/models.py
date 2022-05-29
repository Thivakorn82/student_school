from unicodedata import name
import uuid
from django.db import models

# Create your models here.
class Schools(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True,max_length=20)
    school_name = models.CharField(max_length=20)
    max_students = models.IntegerField()

class Students(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True,max_length=20)
    student_firstname = models.CharField(max_length=20)
    student_lastname = models.CharField(max_length=20)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)