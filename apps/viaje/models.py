# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAMES_REGEX = re.compile(r'[a-zA-Z]{4,}')
PSWRD_REGEX = re.compile(r'\w{8,}')

# Create your models here.
class usersManager(models.Manager):
    def createUser(self, data):
        errors = []
        try:
            user = Users.objects.get(email=data['email'])
            errors.append("Email exist in Data Base")
            return [False, errors]
        except ObjectDoesNotExist:
            #Making validations
            if len(data['name']) < 3:
                errors.append("First Name can not be blank!")
            elif not NAMES_REGEX.match(data['name']):
                errors.append("Invalid first name format.")

            if len(data['email']) < 3:
                errors.append("Email cannot be blank!")
            elif not EMAIL_REGEX.match(data['email']):
                errors.append("Invalid Email Address format!")

            if len(data['password']) < 8:
                errors.append("Password can not be blank!")
            elif data['password'] != data['confirm_pswrd']:
                errors.append("Passwords do not match")
            elif not PSWRD_REGEX.match(data['password']):
                errors.append("Invalid password format.")

            if errors:
                return [False, errors]
            else:
                hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
                Users(name=data['name'], email=data['email'], password=hashed).save()
                user = Users.objects.get(email=data['email'])
                return [True, user]

    def checkLogin(self, data):
        errors = []
        try:
            user = Users.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password.encode():
                return [True, user]
            else:
                errors.append("Incorrect password.")
                return [False, errors]
        except ObjectDoesNotExist:
            errors.append("User and/or Password are incorrect. Please, try again.")
            return [False, errors]
class tripsManager(models.Manager):
    def createTrip(self, data):
        errors = []
        #Making validations
        if len(data['destination']) < 1:
            errors.append("Destination field can not be blank!!")
        if len(data['description']) < 1:
            errors.append("Description field can not be blank!!")
        if len(data['start_DT']) < 1:
            errors.append("Travel Date From field can not be blank!!")
        elif datetime.strptime(data['start_DT'], "%Y-%m-%d") < datetime.now():
            errors.append("Travel Date From is not valid. Pick another start date for your travel.")
        if len(data['end_DT']) < 1:
            errors.append("Travel Date To field can not be blank!!")
        elif datetime.strptime(data['end_DT'], "%Y-%m-%d") < datetime.now():
            errors.append("Travel Date To is not valid. Pick another start date for your travel.")
        elif datetime.strptime(data['end_DT'], "%Y-%m-%d") < datetime.strptime(data['start_DT'], "%Y-%m-%d"):
            errors.append("Travel Date To should not be before Travel Date From")

        if errors:
            return [False, errors]
        else:
            try:
                traveler = Users.objects.get(id=data['user_id'])
                trip = Trips.objects.create(destination=data['destination'], description=data['description'], start_DT=data['start_DT'], end_DT=data['end_DT'])
                trip.travelers.add(traveler)
              
                usertrips = Users.objects.get(id=data['user_id']).trips.all()
                return [True, usertrips]
            except ObjectDoesNotExist:
                errors.append("Traveler, your ID is not present in our system")
                return [False, errors]

    def jointravel(self, data):
        errors = []
        try:
            traveler = Users.objects.get(id=data['user_id'])
            trip = Trips.objects.get(id=data['trip_id'])
            if traveler not in trip.travelers.all():
                trip.travelers.add(traveler)
                usertrips = Users.objects.get(id=data['user_id']).trips.all()
                return [True, usertrips]
            else:
                errors.append("You are already joined this trip")
                return [False, errors]
        except ObjectDoesNotExist:
            errors.append("Traveler or Trip ID do not exist in our system")
            return [False, errors]

class Users(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100, unique=True)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '**[User ID: %s | Name: %s | Email: %s]**' % (self.id, self.name, self.email)
    objects = usersManager()

class Trips(models.Model):
    destination = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    start_DT = models.DateTimeField()
    end_DT = models.DateTimeField()
    travelers = models.ManyToManyField(Users, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '**[Destination: %s | Travel Start Date: %s | Travel End Date: %s | Plan: %s]**' % (self.destination, self.start_DT, self.end_DT, self.description)
    objects = tripsManager()