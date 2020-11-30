from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"
        if len(post_data['email']) < 8:
            errors['length_email'] = "Email must be at least 8 characters long"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Invalid Email. Please try again"
        if len(post_data['password']) < 8:
            errors['length_password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['confirm_password']:
            errors['invalid_password'] = "Password and confirm doesn't match"
        return errors
    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['email']) < 8:
            errors['email_length'] = "Email must be at least 8 characters long"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Invalid email. Please try again"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager ()
    def __repr__(self):
        return f'{self.first_name}-{self.last_name}-{self.email}-'


# Create your models here.
