from django.db import models

"""
this is the database set up
we have 3 table's
with 2 linked table (using the ManyToManyField)

Movies : for the name and the year
Character : for name and movies using ManyToManyField to linked the Movies table
User : for user name and Character he liked  using ManyToManyField to linked the Character table
"""
class Movies(models.Model):
    movie = models.CharField(max_length=255)
    year = models.IntegerField(null=False)


class Character(models.Model):
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movies)


class User(models.Model):
    userName = models.CharField(max_length=255)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return self.name
