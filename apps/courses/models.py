# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CourseManager(models.Manager):
    def validation(self, postData):
        error = {}
        if len(postData['name']) <= 5:
            error['name'] = "Course name must be greater than 5 characters."
        if len(postData['desc']) <= 10:
            error['desc'] = "Course description must be greater than 10 characters."
        return error
class Course(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CourseManager()