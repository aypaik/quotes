from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User


# Create your models here.

class QuoteManager(models.Manager):
    
    def validate(self, postData):
        results = {'status': True, 'errors':[]}

        if len(postData['quoted_by']) < 3:
            results['errors'].append('Field must be at least 3 characters long.')
            results['status'] = False
                    
        if len(postData['quote']) < 10:
            results['errors'].append('Quote must be at least 10 characters long.')
            results['status'] = False

        return results

class Quote(models.Model):
    quoted_by = models.CharField(max_length = 255)
    quote = models.CharField(max_length = 255)
    posted_by = models.ForeignKey(User, related_name = 'posted_by')
    favorites = models.ManyToManyField(User, related_name = 'favorites')
    objects = QuoteManager()
