from django.db import models

class User(models.Model):
    name     = models.CharField(max_length = 128)
    email    = models.CharField(max_length = 128)
    password = models.CharField(max_length = 512)
    mobile   = models.CharField(max_length = 32)

    class Meta:
        db_table = 'users'

class Board(models.Model):
    title      = models.CharField(max_length = 128)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    user       = models.ForeignKey('User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'board'
