from django.db import models


class Subgenre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=150)
    subgenre = models.ManyToManyField(Subgenre, related_name='subjenre')
    def __str__(self):
        return self.name

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя",
        unique=True,
    )
    name = models.CharField(max_length=150,
                            verbose_name='Имя пользователя')
    genre=models.ManyToManyField(Genre,blank=True)
    subgenre = models.ManyToManyField(Subgenre, related_name='subjenres',blank=True,default=0)
    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'

class Book(models.Model):
    name=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    description=models.TextField()
    poster=models.ImageField(upload_to="books/")
    size=models.PositiveIntegerField()
    date=models.DateField()
    genre=models.ManyToManyField(Subgenre)
    url=models.CharField(max_length=600,default=0)
    def __str__(self):
        return self.name