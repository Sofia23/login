# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
# class UsersManager(models.Manager):
#     def validation(self, postData):
#         errors = {}
#         if len(postData['first_name']) < 2:
#             errors['first_name'] = "First name should be more than 2 characters."
#         if len(postData['last_name']) < 2:
#             errors['last_name'] = "Last name should be more than 2 characters."
#         if 5 < postData['age'] < 100:
#             errors['age'] = "You must be between age 6 to 100"
#         return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.age)