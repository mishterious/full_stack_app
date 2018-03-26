from __future__ import unicode_literals
import re, datetime, time
from django.db import models

ALL_LETTERS_REGEX = re.compile(r'[A-Za-z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        errors = {}
        email = postData['email'].lower()
        if len(postData['first_name']) < 2 or (postData['first_name'].isalpha()) != True:
            errors['first_name'] = "Your first name should be at least 2 letters long and should only be letters"
        if len(postData['last_name']) < 2 or (postData['last_name'].isalpha()) != True:
            errors['last_name'] = "Your first name should be at least 2 letters long and should only be letters"
        if len(email) < 1:
            errors['email'] = "Please enter an e-mail address"
        if not EMAIL_REGEX.match(email):
            errors['email2'] = "Please enter a Valid e-mail address"
        if re.search('[0-9]', postData['pw']) is None:
            errors['numpass'] = "You need to enter at least one number to make your password Valid"
        if re.search('[A-Z]', postData['pw']) is None:
            errors['capspass'] = "You will need to enter at least one capital letter"
        if len(postData['pw']) < 8:
            errors['lenpass'] = "Your password needs to be at least 8 character to be Valid"
        elif postData['pw'] != postData['pw_confirm']:
            errors['mispass'] = "Your passwords do not match"
        user = User.objects.filter(email=email)
        if len(user) > 0:
            errors['user'] = "User already exists in the database"

        return errors


class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['author']) == 2: 
            errors['author_name_length'] = "Author's name should be more than 2 characters"
        return errors


class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0: 
            errors['title_blank'] = "Title can't be blank"
        return errors


class MovieManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['movie']) == 0: 
            errors['movie_blank'] = "Movie name can't be blank"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name="books")
    objects = BookManager()


class Review(models.Model):
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='reviews')
    book = models.ForeignKey(Book, related_name='reviews')


class Actor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    movie = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, related_name='movies')
    author = models.ForeignKey(Author, related_name='movies')
    actor = models.ForeignKey(Actor, related_name='movies')
    objects = MovieManager()

