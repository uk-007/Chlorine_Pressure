from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import json


class ChlorineData(models.Model):
    Name=models.CharField(max_length=20)
    loginid=models.CharField(max_length=20)
    Pwd=models.CharField(max_length=10)



# creating a Userprofile table which can have extra fields(additional info) which we need for our User. UserProfile and auth_user table have 
# OneToOne realationship with UserTable containing foreignkey as user_id 
class UserProfile(models.Model):                                 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(db_column='id', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=50)
    loginid = models.CharField(db_column='loginid',max_length=50)
    roleid = models.IntegerField(default=1)
    orgid = models.IntegerField(default = 1, blank=True, null=True)
    region = models.IntegerField(default = 1,blank=True, null=True)
    portion = models.IntegerField(default = 1,blank=True, null=True)
    user_group = models.IntegerField(default = 1,blank=True, null=True)
    stock_alltr = models.IntegerField(default = 1,blank=True, null=True)
    #age = models.IntegerField(null=True, blank=True)
    #profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


