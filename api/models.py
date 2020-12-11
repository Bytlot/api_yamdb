from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    
    def __str__(self): 
       return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    rating = models.ForeignKey(
        Ratings, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="title"
    )
    description = models.TextField()
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="title"
    ) 
    def __str__(self): 
       return self.name


class Genres(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    title = models.ForeignKey(
        Titles, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="genre"
    )

    def __str__(self): 
       return self.name
