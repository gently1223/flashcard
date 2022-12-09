from pyexpat import model
from django.db import models

# Create your models here.  
class user_info(models.Model):
    user_id = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

class question_book(models.Model):
    uuid = models.CharField(max_length=250)
    file_name = models.CharField(max_length=250)
    image_folder = models.CharField(max_length=250)
    contents = models.JSONField()

class questions_areas(models.Model):
    area_uuid = models.CharField(max_length=36)
    linked_uuid = models.CharField(max_length=36)
    area_number = models.CharField(max_length=128)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    book_uuid = models.CharField(max_length=36)
    page_number = models.CharField(max_length=128)

class questions_pages(models.Model):
    uuid = models.CharField(max_length=36)
    page_number = models.CharField(max_length=128)
    width = models.FloatField()
    height = models.FloatField()

class questions_sub_areas(models.Model):
    sub_area_uuid = models.CharField(max_length=36, primary_key=True)
    sub_area_number = models.CharField(max_length=128)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    book_uuid = models.CharField(max_length=36)
    page_number = models.CharField(max_length=128)
    main_uuid = models.CharField(max_length=36)

class records(models.Model):
    count = models.IntegerField(primary_key=True)
    question_area_uuid = models.CharField(max_length=36)
    datetime = models.DateTimeField(max_length=6)
    result = models.CharField(max_length=32)
    level = models.CharField(max_length=32)
    book_uuid = models.CharField(max_length=36)

class setting(models.Model):
    user_id = models.CharField(max_length=250)
    data = models.JSONField()

class cardapp_answers_areas(models.Model):
    area_uuid = models.CharField(max_length=36, primary_key=True)
    linked_uuid = models.CharField(max_length=36)
    area_number = models.CharField(max_length=128)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    book_uuid = models.CharField(max_length=36)
    page_number = models.CharField(max_length=128)

class cardapp_answers_book(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    file_name = models.CharField(max_length=2048)
    image_folder = models.CharField(max_length=2048)
    contents = models.JSONField()

class cardapp_answers_pages(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    page_number = models.CharField(max_length=128)
    width = models.FloatField()
    height = models.FloatField()

class cardapp_answers_sub_areas(models.Model):
    sub_area_uuid = models.CharField(max_length=36, primary_key=True)
    sub_area_number = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    book_uuid = models.CharField(max_length=36)
    page_number = models.CharField(max_length=128)
    main_uuid = models.CharField(max_length=36)