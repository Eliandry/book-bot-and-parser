from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
class Book(models.Model):
    name=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    description=models.TextField()
    genre=models.ManyToManyField(Genre)
    url=models.CharField(max_length=600,default=0)
    def __str__(self):
        return self.name
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя",
        unique=True,
    )
    name = models.CharField(max_length=150,null=True)
    genre=models.ManyToManyField(Genre,blank=True,related_name='genre')
    library = models.ManyToManyField(Book, blank=True, related_name='library')
    goodbook=models.ManyToManyField(Book,blank=True,related_name='goodbook')
    badbook = models.ManyToManyField(Book, blank=True, related_name='badbook')
    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'