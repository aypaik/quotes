from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
import datetime
from datetime import date


# Create your models here.

class UserManager(models.Manager):
    def loginVal(self, postData):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = postData['email'])
        
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results


    def creator(self, postData):
        user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return user
   
    # validate must take (self)
    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        if len(postData['name']) < 3:
            results['errors'].append('Your name is too short.')
            results['status'] = False
        
        # check if first name is valid
        if not re.match("^[A-z][A-z|\.|\s]+$", postData['name']):
            results['errors'].append('Your name is not a valid name.')
            results['status'] = False
            
        if len(postData['alias']) < 3:
            results['errors'].append('Your alias is too short.')
            results['status'] = False

        if not re.match("^[A-z][A-z|\.|\s]+$", postData['alias']):
            results['errors'].append('Your alias is not valid.')
            results['status'] = False


        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False

        if postData['password'] != postData['c_password']:
            results['errors'].append('Your passwords do not match.')
            results['status'] = False

        if len(postData['password']) < 8:
            results['errors'].append('Your password is too short.')
            results['status'] = False

        birthday = postData['bday']
        if len(birthday) == 10:
            byear = int(birthday[:4])
            bmonth = int(birthday[5:7])
            bday = int(birthday[8:])
            if datetime.date.today() < datetime.date(byear, bmonth, bday):
                results['status'] = True
                results['errors'].append('Invalid birthdate')
        else:
            results['status'] = True
            results['errors'].append('Not a valid birthday.')

        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('User already exists.')
            results['status'] = False

        return results


class User(models.Model):
    name = models.CharField(max_length = 200)
    alias = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    objects = UserManager()
    